import os
import click

from flask import Flask  # step one
from knowledge.settings import config
from knowledge.models import User
from knowledge.extensions import db, migrate
from knowledge.apis.v1 import api_v1

import knowledge.fakes as fakes

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('knowledge')
    app.config.from_object(config[config_name])
    register_blueprints(app)
    register_extensions(app)
    register_shell_context(app)
    register_commands(app)
    return app


def register_blueprints(app):
    app.register_blueprint(api_v1, url_prefix='/api/v1')


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(
            db=db,
            User = User,
            fakes = fakes
            )

def register_commands(app):
    @app.cli.command()
    def init():
        """Initialize knowledge."""
        click.echo('Initializing the database...')
        db.create_all()

        click.echo('Done.')

    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize knowledge."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        click.echo('Initializing the database...')
        db.create_all()
        click.echo('Done.')

    @app.cli.command()
    @click.option('--user', default=5)
    def forge(user):
        db.drop_all()
        db.create_all()
        """Generate fake data."""
        click.echo('Generating admin')
        fakes.fake_admin()
        
        click.echo('Generating %s users' % user)
        fakes.fake_user(user)

        click.echo('Done.')