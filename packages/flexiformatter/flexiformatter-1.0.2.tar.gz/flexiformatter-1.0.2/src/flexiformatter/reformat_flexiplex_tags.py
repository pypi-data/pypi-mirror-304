import re
import sys
import typer
import simplesam
from flexiformatter import __version__ 

app = typer.Typer(add_completion=False)

@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context, 
    infile: str = typer.Argument(None),
    version: bool = typer.Option(
        None, "--version", "-v", help="Prints the version of the tool.", is_eager=True
    ),
):
    """
    A simple tool for processing BAM/SAM files.
    """
    if version:
        typer.echo(f"flexi_formatter version: {__version__}")
        raise typer.Exit()

    if ctx.invoked_subcommand is None and infile is not None:
        # If no subcommand is invoked and 'infile' is given, call 'main' directly
        main(infile)

@app.command()
def main(infile: str):
    """Process BAM/SAM file."""
    with simplesam.Reader(open(infile)) as in_bam:
        with simplesam.Writer(sys.stdout, in_bam.header) as out_sam:
            for read in in_bam:
                # Get header name and split by "_#"
                bc_umi = read.qname.split("_#")[0]
                
                if len(bc_umi.split("#")) > 1:
                    bc = bc_umi.split("#")[1]
                    umi = bc_umi.split("#")[0].split("_")[1]
                    read.tags['CB'] = bc
                    read.tags['UR'] = umi
                else:
                    bc = bc_umi
                    read.tags['CB'] = bc
                
                # Write new reads
                out_sam.write(read)

if __name__ == "__main__":
    app()
