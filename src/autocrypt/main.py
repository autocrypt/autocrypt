import os
import shutil
import six
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
    """access and manage Autocrypt keys, options, headers."""
    basedir = os.path.abspath(os.path.expanduser(basedir))
    context.account = Account(basedir)


@click.command()
@click.option("--replace", default=False, is_flag=True,
              help="delete autocrypt account directory before init")
@click.pass_context
def init(ctx, replace):
    """initialize new autocrypt key and default options."""
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


def get_account(ctx):
    account = ctx.parent.account
    try:
        account._ensure_exists()
    except account.NotInitialized as e:
        click.secho(str(e), fg='red')
        ctx.exit(1)
    return account


@click.command("make-header")
@click.argument("emailadr", type=click.STRING)
@click.pass_context
def make_header(ctx, emailadr):
    """print autocrypt header for an emailadr. """
    account = get_account(ctx)
    click.echo(account.make_header(emailadr))


@click.command("set-prefer-encrypt")
@click.argument("value", default=None, required=False,
                type=click.Choice(["notset", "yes", "no"]))
@click.pass_context
def set_prefer_encrypt(ctx, value):
    """print or set prefer-encrypted setting."""
    account = get_account(ctx)
    if value is None:
        click.echo(account._prefer_encrypt)
    else:
        value = six.text_type(value)
        account.set_prefer_encrypt(value)
        click.echo("set prefer-encrypt to %r" % value)


@click.command("export-public-key")
@click.pass_context
def export_public_key(ctx):
    """print armored public key associated with this autocrypt account. """
    account = get_account(ctx)
    click.echo(account.export_public_key())


@click.command("export-private-key")
@click.pass_context
def export_private_key(ctx):
    """print armored private key associated with this autocrypt account. """
    account = get_account(ctx)
    click.echo(account.export_private_key())


autocrypt_main.add_command(init)
autocrypt_main.add_command(make_header)
autocrypt_main.add_command(set_prefer_encrypt)
autocrypt_main.add_command(export_public_key)
autocrypt_main.add_command(export_private_key)


#@click.command()
#@click.pass_obj
#def bot(ctx):
#    """Bot invocation and account generation commands. """
##    assert 0, obj.account_dir
