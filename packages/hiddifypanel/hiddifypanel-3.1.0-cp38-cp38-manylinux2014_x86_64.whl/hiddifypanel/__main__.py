import click
from flask.cli import FlaskGroup

from . import create_app_wsgi


@click.group(cls=FlaskGroup, create_app=create_app_wsgi)
def main():
    """Management script for the hiddifypanel application."""


if __name__ == "__main__":  # pragma: no cover
    main()
#واقعا برای 5 دلار میخوای کرک میکنی؟ حاجی ارزش وقت خودت بیشتره
#Email hiddify@gmail.com for free permium version. Do not crack this cheap product
