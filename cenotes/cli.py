import click
from cenotes import create_app, db, models


@click.command()
@click.option('--cleanup', is_flag=True, default=False,
              help="Cleanup expired notes")
@click.option('--settings', show_default=True, type=click.Choice(
    ["Production", "Development", "Testing"]), default="Production")
@click.option("--host", type=str, default="localhost", show_default=True)
@click.option("--port", type=int, default=8080, show_default=True)
def main(cleanup, settings, host, port):

    app = create_app(app_settings="cenotes.config_backend.{0}"
                     .format(settings))

    if not cleanup:
        app.run(host=host, port=port)
    else:
        db.app = app
        models.get_expired_notes().delete()
        db.session.commit()


if __name__ == '__main__':
    main()
