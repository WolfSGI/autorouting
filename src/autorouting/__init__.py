from autoroutes import Routes as Autoroutes
from collections import UserDict
from collections.abc import Iterable
from typing import NamedTuple, Any, ClassVar
from autorouting.url import RouteURL
from frozendict import frozendict


class ImmutabilityError(Exception):
    pass


class Routes(Autoroutes):

    def __init__(self):
        self._byname: dict[str, RouteURL] = {}
        super().__init__()


class Route(NamedTuple):
    component: Any
    requirements: frozendict
    priority: int = 0


class MatchedRoute(NamedTuple):
    path: str | None
    namespace: str
    component: Any
    params: dict


class RouteGroup(UserDict[str, list[Route]]):
    name: str | None

    def __init__(self, name: str | None, *args, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)

    def add(self, namespace: str, route: Route, append: bool = True):
        if namespace in self:
            if not append:
                raise KeyError("Route already populated.")
            if route in self[namespace]:
                raise ValueError('Route already exists.')
            for existing in self[namespace]:
                if existing == route:
                    raise ValueError('Equivalent route already exists.')
            self[namespace].append(route)
        else:
            self[namespace] = [route]
        self[namespace].sort(
            key=lambda r: (-r.priority, -len(r.requirements))
        )


class Router(dict[str, RouteGroup]):

    allowed_namespaces: ClassVar[Iterable | None] = None

    def __init__(self, *args, **kwargs):
        self._names = set()
        self._routes = None
        super().__init__(*args, **kwargs)

    def add(self,
            path: str,
            namespace: str,
            component: Any,
            name: str | None = None,
            requirements: dict | None = None,
            priority: int = 0):

        if self._routes is not None:
            raise ImmutabilityError('Router is already finalized.')

        if (self.allowed_namespaces and
            namespace not in self.allowed_namespaces):
            raise ValueError(
                f"Unknown namespace: {namespace}. "
                f"Expected one of {self.allowed_namespaces!r}"
            )

        if requirements is None:
            requirements = {}
        route = Route(component, frozendict(requirements), priority=priority)

        if path not in self:
            if name:
                if name in self._names:
                    raise NameError(f"Name {name!r} is already in use.")
                self._names.add(name)
            group = self[path] = RouteGroup(name)
            group.add(namespace, route)
        else:
            if self[path].name is None:
                if name:
                    if name in self._names:
                        raise NameError(f"Name {name!r} is already in use.")
                    self._names.add(name)
                self[path].name = name
            elif self[path].name != name:
                raise NameError(
                    f'Conflict: Path of route {name!r} already '
                    f'belongs to a group named {self[path].name!r}.'
                )
            self[path].add(namespace, route)
        return route

    def match(self, path: str, namespace: str, extra: dict | None = None):
        if self._routes is None:
            raise NotImplementedError('Router was not finalized.')
        group, params = self._routes.match(path)
        if group and namespace in group:
            for route in group[namespace]:
                if not route.requirements:
                    yield MatchedRoute(
                        component=route.component,
                        params=params,
                        path=path,
                        namespace=namespace
                    )
                elif extra:
                    if set(route.requirements.keys()) <= set(extra.keys()):
                        for name, requirement in route.requirements.items():
                            if not requirement.matches(extra[name]):
                                break
                        else:
                            yield MatchedRoute(
                                component=route.component,
                                params=params,
                                path=path,
                                namespace=namespace
                            )

    def get(self,
            path: str,
            namespace: str,
            extra: dict | None = None) -> MatchedRoute | None:

        routes = self.match(path, namespace, extra)
        try:
            return next(routes)
        except StopIteration:
            return None
        finally:
            routes.close()

    def get_by_name(self, name: str) -> RouteURL | None:
        if self._routes is None:
            raise NotImplementedError('Router was not finalized.')
        return self._routes._byname.get(name)

    def finalize(self):
        if self._routes is not None:
            return
        self._routes = Routes()
        for path, group in self.items():
            if group.name:
                self._routes._byname[group.name] = RouteURL.from_path(path)
            self._routes.add(
                path, **{
                    namespace: tuple(routes)
                    for namespace, routes in group.items()
                    if (not self.allowed_namespaces or
                        namespace in self.allowed_namespaces)
                }
            )

    def __or__(self, other) -> 'Router':
        router = self.__class__()
        for merger in (self, other):
            for path, group in merger.items():
                for namespace, routes in group.items():
                    for route in routes:
                        router.add(
                            path,
                            namespace,
                            route.component,
                            name=group.name,
                            requirements=route.requirements,
                            priority=route.priority
                        )
        return router

    def __ior__(self, other: 'Router') -> 'Router':
        if self._routes is not None:
            raise ImmutabilityError('Router is finalized.')
        for path, group in other.items():
            for namespace, routes in group.items():
                for route in routes:
                    self.add(
                        path,
                        namespace,
                        route.component,
                        name=group.name,
                        requirements=route.requirements,
                        priority=route.priority
                    )
        return self
