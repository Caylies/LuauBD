import asyncio
from inspect import iscoroutinefunction
from types import FunctionType, MethodType
from typing import Any, Callable

import pluau

__all__ = ("LuauRuntime",)


def async_to_lua_function(lua: pluau.Lua, function, on_complete: Callable) -> pluau.Function:
    def wrapper(callback_lua: pluau.Lua, arguments: list):
        thread = callback_lua.current_thread()

        async def run():
            try:
                result = await function(*arguments)
                on_complete(thread, result)
            except Exception as exc:
                thread.resume_error(str(exc))

        asyncio.get_running_loop().create_task(run())
        callback_lua.yield_with()

    return lua.create_function(wrapper)


class LuauRuntime:
    def __init__(self):
        self.lua = pluau.Lua()
        self.lua.sandbox(True)
        self.lua.set_memory_limit(1 * 1024 * 1024)
        self.env = {}

    def to_lua(self, value: Any):
        transformed = value

        if value is None or isinstance(value, (bool, int, float, pluau.Table, pluau.String)):
            return value

        if isinstance(value, str):
            transformed = self.lua.create_string(transformed)
        elif isinstance(value, (list, dict)):
            new_table = self.lua.create_table()

            if isinstance(transformed, list):
                for item in transformed:
                    new_table.push(self.to_lua(item))
            else:
                for key, item in transformed.items():
                    new_table.set(self.to_lua(key), self.to_lua(item))

            transformed = new_table
        elif iscoroutinefunction(value):

            def on_complete(thread: pluau.Thread, result: Any):
                lua_result = self.to_lua(result) if result is not None else None

                if lua_result is None:
                    thread.resume()
                elif isinstance(lua_result, (list, tuple)):
                    thread.resume(*lua_result)
                else:
                    thread.resume(lua_result)

            transformed = async_to_lua_function(self.lua, value, on_complete)
        elif isinstance(value, (FunctionType, MethodType)):
            transformed = self.lua.create_function(lambda _, arguments, function=value: function(*arguments))
        else:
            raise TypeError(f"Invalid type '{type(value).__name__}' ({value})")

        return transformed

    async def exec(self, content: str):
        chunk = self.lua.load_chunk(content, env=self.to_lua(self.env))
        thread = self.lua.create_thread(chunk)

        thread.resume()

        while thread.status == pluau.ThreadState.Resumable:
            await asyncio.sleep(0)
