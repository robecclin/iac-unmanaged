from boto3 import Session
from rich.console import Console
from rich.table import Table
from typer import Exit

from iac_index.aws import index as index_aws
from iac_index.error import IacIndexError
from iac_unmanaged.app import app

console = Console()
err_console = Console(stderr=True)


@app.command(help="Discover resources using AWS Resource Explorer")
def index() -> None:
    session = Session()

    table = Table()
    table.add_column("Account")
    table.add_column("Region")
    table.add_column("Type")
    table.add_column("ID")

    try:
        for resource in index_aws(session):
            table.add_row(
                resource.account,
                resource.region,
                str(resource.type),
                resource.identifier,
            )
    except IacIndexError as error:
        err_console.print(str(error), style="red", markup=False)
        raise Exit(1) from error

    if table.row_count == 0:
        console.print("No resources found")
        raise Exit()

    console.print(table)
