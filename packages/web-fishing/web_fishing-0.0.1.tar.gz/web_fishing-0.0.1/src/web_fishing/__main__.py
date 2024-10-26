"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """Web Fishing."""


if __name__ == "__main__":
    main(prog_name="web-fishing")  # pragma: no cover
