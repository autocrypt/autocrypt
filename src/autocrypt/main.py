import os
import shutil
import click
from .account import Account

class CmdlineState:
    pass


class MyGroup(click.Group):
    """ small click group to enforce order of subcommands in help. """
    def add_command(self, cmd):
        self.__dict__.setdefault("_cmdlist", [])
        self._cmdlist.append(cmd.name)
        return super(MyGroup, self).add_command(cmd)

    def list_commands(self, ctx):
        commands = super(MyGroup, self).list_commands(ctx)
        assert sorted(commands) == sorted(self._cmdlist)
        return self._cmdlist


@click.command(cls=MyGroup)
@click.option("--basedir", type=click.Path(),
              default=click.get_app_dir("autocrypt"),
              envvar="AUTOCRYPT_BASEDIR",
              help="directory where autocrypt account state is stored")
@click.version_option()
@click.pass_context
def autocrypt_main(context, basedir):
    """access Autocrypt info and run bot."""
    basedir = os.path.abspath(os.path.expanduser(basedir))
    context.account = Account(basedir)


@click.command()
@click.option("--replace", default=False, is_flag=True,
              help="delete autocrypt account directory before init")
@click.pass_context
def init(ctx, replace):
    """generate autocrypt account."""
    account = ctx.parent.account
    if account.exists():
        if not replace:
            click.echo("account {} exists at {} and --replace was not specified".format(
                       account.uuid, account.dir))
            ctx.exit(1)
        else:
            click.echo("deleting account directory: {}".format(account.dir))
            account.remove()
    account.init()
    click.echo("{}: account {} created".format(account.dir, account.uuid))


@click.command("make-header")
@click.argument("emailadr", type=click.STRING)
@click.pass_context
def make_header(ctx, emailadr):
    """print autocrypt header for an emailadr. """
    account = ctx.parent.account
    try:
        click.echo(account.make_header(emailadr))
    except account.NotInitialized as e:
        click.secho(str(e), fg='red')
        ctx.exit(1)


@click.command("export-public-key")
@click.pass_context
def export_public_key(ctx):
    """print armored public key associated with this autocrypt account. """
    account = ctx.parent.account
    try:
        click.echo(account.export_public_key())
    except account.NotInitialized as e:
        click.secho(str(e), fg='red')
        ctx.exit(1)


@click.command("export-private-key")
@click.pass_context
def export_private_key(ctx):
    """print armored private key associated with this autocrypt account. """
    account = ctx.parent.account
    try:
        click.echo(account.export_private_key())
    except account.NotInitialized as e:
        click.secho(str(e), fg='red')
        ctx.exit(1)


autocrypt_main.add_command(init)
autocrypt_main.add_command(make_header)
autocrypt_main.add_command(export_public_key)
autocrypt_main.add_command(export_private_key)


#@click.command()
#@click.pass_obj
#def bot(ctx):
#    """Bot invocation and account generation commands. """
##    assert 0, obj.account_dir
