import click
from cenotes import create_app


@click.command()
@click.option('--settings', show_default=True, type=click.Choice(
    ["Production", "Development", "Testing"]), default="Production")
@click.option("--host", type=str, default="localhost", show_default=True)
@click.option("--port", type=int, default=8080, show_default=True)
def main(settings, host, port):
    create_app(app_settings="cenotes.config_backend.{0}"
               .format(settings)).run(host=host, port=port)


if __name__ == '__main__':
    main()
