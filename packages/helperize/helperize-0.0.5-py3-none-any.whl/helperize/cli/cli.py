import typer

from helperize.log import get_logger

log = get_logger(__name__)

app = typer.Typer(
    no_args_is_help=True,
    help="Helper's gonna help.",
    context_settings={"help_option_names": ["-h", "--help"]},
    add_completion=False,
)


@app.command()
def ask(
    prompt: str = typer.Argument(..., help="Provide a text prompt to the model."),
) -> str | None | int:
    """🐧 Ask a question."""
    log.info(f"You asked: {prompt}")
    response = "Hello World!"
    log.info(f"Response: {response}")
    return response


if __name__ == "__main__":
    app()
