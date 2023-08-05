import logging
from logging import Logger

from rich.console import Console
from rich.logging import RichHandler
from rich.markdown import Markdown

logging.basicConfig(
    # Configuration options: https://docs.python.org/3/library/logging.html#logrecord-attributes
    format="%(funcName)s() %(message)s",
    level=logging.INFO,
    # Rich markup in console logs! https://rich.readthedocs.io/en/stable/logging.html
    handlers=[RichHandler(rich_tracebacks=True)],
)


def get_logger(name: str | None) -> Logger:
    """Get a logger with our preferred settings.

    Usage:
        from helper.log import get_logger
        log = get_logger(__name__)
    """
    return logging.getLogger(name)


def markdown(spec: str) -> None:
    """Log rich markdown to the console.

    Usage:

        from helper.log import markdown

        markdown('''
    # Header

    - list item 1
    - list item 2

    ```Python
    def hello():
        print("Hello!")
    ```
        ''')
    """
    console = Console(log_time=False, log_path=False)
    console.log(Markdown(spec))
