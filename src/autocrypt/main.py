# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab

"""Autocrypt Command line implementation.
"""

import os
import six
import click
from .account import Account
from . import mime


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


@click.command(cls=MyGroup, context_settings=dict(help_option_names=["-h", "--help"]))
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
    """init autocrypt account state. """
    account = ctx.parent.account
    if account.exists():
        if not replace:
            click.echo("account {} exists at {} and --replace was not specified".format(
                       account.config.uuid, account.dir))
            ctx.exit(1)
        else:
            click.echo("deleting account directory: {}".format(account.dir))
            account.remove()
    if not os.path.exists(account.dir):
        os.mkdir(account.dir)
    account.init()
    click.echo("{}: account {} created".format(account.dir, account.config.uuid))


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
        click.echo(account.config.prefer_encrypt)
    else:
        value = six.text_type(value)
        account.set_prefer_encrypt(value)
        click.echo("set prefer-encrypt to %r" % value)


@click.command("process-incoming")
@click.argument("mail", type=click.File())
@click.pass_context
def process_incoming(ctx, mail):
    """process incoming mail from file/stdin."""
    account = get_account(ctx)
    msg = mime.parse_message_from_file(mail)
    adr = account.process_incoming(msg)
    keyhandle = account.get_latest_public_keyhandle(adr)
    click.echo("processed mail from %s, found key: %s" % (adr, keyhandle))


@click.command("export-public-key")
@click.argument("keyhandle_or_email", default=None, required=False)
@click.pass_context
def export_public_key(ctx, keyhandle_or_email):
    """print public key of own or peer account."""
    account = get_account(ctx)
    if keyhandle_or_email is not None:
        if "@" in keyhandle_or_email:
            keyhandle_or_email = account.get_latest_public_keyhandle(keyhandle_or_email)
    click.echo(account.export_public_key(keyhandle=keyhandle_or_email))


@click.command("export-secret-key")
@click.pass_context
def export_secret_key(ctx):
    """print secret key of own autocrypt account. """
    account = get_account(ctx)
    click.echo(account.export_secret_key())


@click.command()
@click.pass_context
def status(ctx):
    """print account state including those of peers. """
    account = get_account(ctx)
    click.echo("account-dir: " + account.dir)
    click.echo("uuid: " + account.config.uuid)
    click.echo("own-keyhandle: " + account.config.own_keyhandle)
    click.echo("prefer-encrypt: " + account.config.prefer_encrypt)
    peers = account.config.peers
    if peers:
        click.echo("----peers-----")
        for name, ac_dict in peers.items():
            d = ac_dict.copy()
            keyhandle = account.get_latest_public_keyhandle(name)
            click.echo("{to}: key {keyhandle} [{bytes:d} bytes] {attrs}".format(
                       to=d.pop("to"), keyhandle=keyhandle,
                       bytes=len(d.pop("key")),
                       attrs="; ".join(["%s=%s" % x for x in d.items()])))


autocrypt_main.add_command(init)
autocrypt_main.add_command(status)
autocrypt_main.add_command(make_header)
autocrypt_main.add_command(set_prefer_encrypt)
autocrypt_main.add_command(process_incoming)
autocrypt_main.add_command(export_public_key)
autocrypt_main.add_command(export_secret_key)


# @click.command()
# @click.pass_obj
# def bot(ctx):
#     """Bot invocation and account generation commands. """
#     assert 0, obj.account_dir
