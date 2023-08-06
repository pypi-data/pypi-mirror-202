import os
from pathlib import Path

import pyarrow.csv as pc
import pyarrow.parquet as pq
import typer
from rich import print

from ._app import app


@app.command()
def csv(
    directory: Path,
    compression: str = typer.Option("zstd", help="compression algorithm"),
    compression_level: int = typer.Option(9, help="compression level"),
    clean: bool = typer.Option(
        False, help="remove uncompressed files after successful wringing"
    ),
):
    """Crawl a directory and compress csv files into parquet."""
    if not directory.exists():
        raise FileNotFoundError(directory)
    print(f"wringing {directory} [{compression=}, {compression_level=}]")
    print(f"[{compression=}, {compression_level=}]")
    for dirpath, _dirnames, filenames in os.walk(directory):
        for f in filenames:
            source = os.path.join(dirpath, f)
            target = None
            if source.endswith(".csv"):
                target = source[:-4] + ".parquet"
            elif source.endswith(".csv.gz"):
                target = source[:-7] + ".parquet"
            if target is not None:
                if not os.path.exists(target):
                    print(f"[green]converting[/green] {source}")
                    try:
                        t = pc.read_csv(source)
                        pq.write_table(
                            t,
                            target,
                            compression=compression,
                            compression_level=compression_level,
                        )
                    except Exception as err:
                        print(f"[bold red]{err}[/bold red]")
                    else:
                        if clean and os.path.exists(target):
                            if pq.read_table(target).equals(t, check_metadata=True):
                                os.unlink(source)
                else:
                    print(
                        f"[red]not converting[/red] {source} "
                        "[red](parquet already exists)[/red]"
                    )
