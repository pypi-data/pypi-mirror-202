import typer

is_verbose = False


def drclient(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose mode")
):
    if verbose:
        print("Running in verbose mode")
        global is_verbose
        is_verbose = True
