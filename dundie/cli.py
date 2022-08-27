"""The command line interface (also known as CLI)."""
# is a means to interact with a command line script.
import json

import pkg_resources
import rich_click as click
from rich.console import Console
from rich.table import Table

from dundie import core
from dundie.core import load as core_load

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True


@click.group()
@click.version_option(pkg_resources.get_distribution("dundie").version)
def main():
    """Dundie Mifflin Rewards System.
    This cli application controls Dunder Mifflin rewards.

    . admins can load information tot he people database and
    points.
    . users can view reports and transfer points.


    """


@main.command()
@click.argument("filepath", type=click.Path(exists=True))
def load(filepath):
    """Load the file to the database."""
    """
    ## Features

    . Validadores
    . Parses the file
    . Loads to database

    """
    table = Table(title="[blue]Dundie Mifflin Associates[/]")
    headers = ["nome", "dept", "role", "created", "e-mail"]
    for header in headers:
        table.add_column(header, style="magenta")

    result = core_load(filepath)

    for person in result:
        table.add_row(*[str(value) for value in person.values()])

    console = Console()
    console.print(table)


@main.command()
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.option("--output", default=None)
def show(output, **query):
    """Show the informations about users."""
    result = core.read(**query)
    if output:
        with open(output, "w") as output_file:
            output_file.write(json.dumps(result))

    if not result:
        print("Nothing to show")

    table = Table(title="[blue]Dundie Mifflin Report[/]")
    for key in result[0]:
        table.add_column(key.title(), style="magenta")
    for person in result:
        table.add_row(*[str(value) for value in person.values()])

    console = Console()
    console.print(table)


@main.command()
@click.pass_context
@click.argument("value", type=click.INT, required=True)
@click.option("--dept", required=False)
@click.option("--email", required=False)
def add(ctx, value, **query):
    """Add news users in database."""
    core.add(value, **query)
    ctx.invoke(show, **query)


@main.command()
@click.pass_context
@click.argument("value", type=click.INT, required=True)
@click.option("--dept", required=False)
@click.option("--email", required=False)
def remove(ctx, value, **query):
    """Add news users in database."""
    core.add(-value, **query)
    ctx.invoke(show, **query)
