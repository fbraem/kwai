"""Module that defines a plugin for MyPy."""
# pylint: skip-file
from mypy.nodes import Var, SymbolTableNode, MDEF
from mypy.plugin import Plugin


class KwaiPlugin(Plugin):
    """Plugin for resolving the table decorator."""

    def get_class_decorator_hook(self, fullname: str):
        """Create the hook."""
        if fullname == "core.db.table":
            return table_decorator_hook
        return None


def table_decorator_hook(ctx):
    """Try to inform mypy about the variables/methods that are available.

    The table decorator creates a dynamic class with some variables and methods.
    Currently, only __table_name__ works. There is still some work to do for adding
    methods (like map_row).
    """
    info = ctx.cls.info
    str_type = ctx.api.named_type_or_none("builtins.str", [])
    assert str_type is not None
    var = Var("__table_name__", str_type)
    var.info = info
    info.names["__table_name__"] = SymbolTableNode(MDEF, var)


def plugin(version: str):
    """Create our plugin."""
    return KwaiPlugin
