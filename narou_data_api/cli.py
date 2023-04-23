import pickle

import click
from api import Novel, User
from utils import output_novel_info, output_user_info


@click.group()
def cmd():
    pass


@cmd.command()
@click.argument("userid")
def user(userid):
    user = User.get_by_userid(userid)
    output_info = output_user_info(user)
    click.echo(output_info)


@cmd.command()
@click.argument("ncode")
def novel(ncode):
    novel = Novel.get_novel(ncode)
    if novel is None:
        click.echo("not exist novel with {}".format(ncode), err=True)
    output_info = output_novel_info(novel)

    click.echo(output_info)


if __name__ == "__main__":
    cmd()
