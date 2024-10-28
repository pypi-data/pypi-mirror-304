# Modified from https://github.com/fastapi/typer/issues/428 (iameskild: Sep 6, 2022 )
"""Order typer commands in the appearance of a file instead of alphabetically"""
from click import Context
from typer.core import TyperGroup


class MtaxOrder(TyperGroup):
    def list_commands(self, ctx: Context):
        return list(self.commands)
