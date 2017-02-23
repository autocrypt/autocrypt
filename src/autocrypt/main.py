# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab

"""Autocrypt Command line implementation.
"""

import os
import six
import click
from .account import Account
from .bingpg import find_executable
from . import mime


def out_red(msg):
    click.secho(msg, fg="red")


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


class MyCommand(click.Command):
    def invoke(self, ctx):
        try:
            return super(MyCommand, self).invoke(ctx)
        except Account.NotInitialized as e:
            out_red(str(e))
            ctx.exit(1)


def mycommand(*args):
    return click.command(*args, cls=MyCommand)


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


@mycommand()
@click.option("--replace", default=False, is_flag=True,
              help="delete autocrypt account directory before attempting init")
@click.option("--use-existing-key", default=None, type=str,
              help="use specified secret key from system's gnupg keyring "
                   "and don't create own keyrings or gpghome dir")
@click.option("--gpgbin", default="gpg", type=str,
              help="use specified gpg binary. if it is a simple name it "
                   "is looked up on demand through the system's PATH.")
@click.pass_context
def init(ctx, replace, use_existing_key, gpgbin):
    """init autocrypt account state.

    By default this command creates account state in a directory which
    contains an own key ring in which it will create a new secret key to
    be used for this account.

    If you specify "--use-existing-key <keyhandle>" this account will rather
    use the specified secret key and the system's gpg keyrings.  All incoming
    autocrypt keys will thus be stored in the system key ring intead of
    an own keyring.
    """
    account = ctx.parent.account
    if account.exists():
        if not replace:
            out_red("account {} exists at {} and --replace was not specified".format(
                    account.config.uuid, account.dir))
            ctx.exit(1)
        else:
            out_red("deleting account directory: {}".format(account.dir))
            account.remove()
    if not os.path.exists(account.dir):
        os.mkdir(account.dir)
    if use_existing_key:
        account.init_with_existing(keyhandle=use_existing_key, gpgbin=gpgbin)
    else:
        account.init(gpgbin=gpgbin)
    click.echo("{}: account {} created".format(account.dir, account.config.uuid))
    _status(account)


def get_account(ctx):
    ctx.parent.account.bingpg  # to raise NotInitialized
    return ctx.parent.account


@mycommand("make-header")
@click.argument("emailadr", type=click.STRING)
@click.pass_context
def make_header(ctx, emailadr):
    """print autocrypt header for an emailadr. """
    account = get_account(ctx)
    click.echo(account.make_header(emailadr))


@mycommand("set-prefer-encrypt")
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


@mycommand("process-incoming")
@click.argument("mail", type=click.File())
@click.pass_context
def process_incoming(ctx, mail):
    """process incoming mail from file/stdin."""
    account = get_account(ctx)
    msg = mime.parse_message_from_file(mail)
    peerinfo = account.process_incoming(msg)
    if peerinfo:
        click.echo("processed mail, found: {}".format(peerinfo))
    else:
        click.echo("processed mail, found nothing")


@mycommand("export-public-key")
@click.argument("keyhandle_or_email", default=None, required=False)
@click.pass_context
def export_public_key(ctx, keyhandle_or_email):
    """print public key of own or peer account."""
    account = get_account(ctx)
    kh = keyhandle_or_email
    if kh is not None:
        if "@" in kh:
            kh = account.get_peerinfo(kh).keyhandle
    click.echo(account.export_public_key(keyhandle=kh))


@mycommand("export-secret-key")
@click.pass_context
def export_secret_key(ctx):
    """print secret key of own autocrypt account. """
    account = get_account(ctx)
    click.echo(account.export_secret_key())


@mycommand()
@click.pass_context
def status(ctx):
    """print account state including those of peers. """
    account = get_account(ctx)
    _status(account)


def _status(account):
    click.echo("account-dir: " + account.dir)
    click.echo("uuid: " + account.config.uuid)
    click.echo("own-keyhandle: " + account.config.own_keyhandle)
    click.echo("prefer-encrypt: " + account.config.prefer_encrypt)

    gpgbin = account.config.gpgbin
    if os.sep not in gpgbin:
        click.echo("gpgbin: {} [currently resolves to: {}]".format(
                   gpgbin, find_executable(gpgbin)))
    else:
        click.echo("gpgbin: {}".format(gpgbin))

    click.echo("gpgmode: " + account.config.gpgmode)
    peers = account.config.peers
    if peers:
        click.echo("----peers-----")
        for name, ac_dict in peers.items():
            d = ac_dict.copy()
            click.echo("{to}: key {keyhandle} [{bytes:d} bytes] {attrs}".format(
                       to=d.pop("to"), keyhandle=d.pop("*keyhandle"),
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
