from typing import TYPE_CHECKING, Any, Protocol, final

import pluau
from pluau.utils import Argument

if TYPE_CHECKING:
    from bd_models.models import Manager

    from .runtime import LuauRuntime

__all__ = ("LuauClass", "LuauModel", "luaumethod")


def luaumethod(name: str | None = None):
    def decorator(function):
        function._name = name or function.__name__
        return function

    return decorator


class ManagerModel(Protocol):
    objects: "Manager"


class LuauClass:
    name: str

    def __init__(self, runtime: "LuauRuntime"):
        self.runtime = runtime
        self.metatable = self.runtime.lua.create_table()
        self.metatable.set("__class", self.runtime.lua.create_string(self.name))

        for attribute_name in dir(self):
            attribute = getattr(self, attribute_name, None)

            if not attribute or not hasattr(attribute, "_name"):
                continue

            self.metatable.set(attribute._name, self.runtime.to_lua(attribute))

    @final
    def construct(self, **kwargs):
        self.instance = self.runtime.lua.create_table()

        for key, value in kwargs.items():
            self.instance.set(key, value)

        self.instance.set_metatable(self.metatable)
        return self.instance

    def _to_lua(self, value: Any) -> dict[str, Any]:
        raise NotImplementedError

    def _to_python(self, value: pluau.Table) -> Any:
        raise NotImplementedError


class LuauModel(LuauClass):
    model: ManagerModel

    @luaumethod("get")
    async def model_get(self, key: pluau.String, value: Argument):
        model_instance = await self.model.objects.aget(**{str(key): value})
        return self._to_lua(model_instance)

    @luaumethod("filter")
    async def model_filter(self, filter_table: pluau.Table):
        filtered = []

        async for model_instance in self.model.objects.filter(**{str(key): value for key, value in filter_table}):
            filtered.append(self._to_lua(model_instance))

        return filtered

    @luaumethod("all")
    async def model_all(self):
        all_instances = []

        async for model_instance in self.model.objects.all():
            all_instances.append(self._to_lua(model_instance))

        return all_instances

    def _to_lua(self, value):
        raise NotImplementedError
