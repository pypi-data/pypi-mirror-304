import os
import click
from .store import add_to_store, recreate_from_store, prune_store
from .sync import sync_metadata_and_files

DEFAULT_STORE_PATH = os.path.expanduser("~/.titanic_store")


@click.group()
@click.option('--store-dir', type=click.Path(), default=DEFAULT_STORE_PATH, help="Path to the store directory (default: ~/.titanic_store).")
@click.pass_context
def cli(ctx, store_dir):
    ctx.ensure_object(dict)
    ctx.obj['STORE_DIR'] = store_dir


@cli.command()
@click.argument('app_dir', type=click.Path(exists=True))
@click.option('--ignore-file', type=click.Path(exists=True), help="Path to a custom ignore file.")
@click.pass_context
def add(ctx, app_dir, ignore_file):
    store_dir = ctx.obj['STORE_DIR']
    add_to_store(app_dir, store_dir, ignore_file)
    click.echo(f"Added files from {app_dir} to titanic store and generated titanic-metadata.json.")


@cli.command()
@click.argument('metadata_path', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=False))
@click.pass_context
def recreate(ctx, metadata_path, output_dir):
    store_dir = ctx.obj['STORE_DIR']
    recreate_from_store(metadata_path, output_dir, store_dir)
    click.echo(f"Recreated files in {output_dir} using {metadata_path}.")


@cli.command()
@click.argument('remote_server')
@click.argument('remote_metadata_path', type=click.Path())
@click.argument('output_dir')
@click.option(
    '--remote-store-dir',
    type=click.Path(),
    default="~/.titanic_store",
    help="Path to the remote server's store directory (default: ~/.titanic_store)."
)
@click.pass_context
def sync(ctx, remote_server, output_dir, remote_metadata_path, remote_store_dir):
    store_dir = ctx.obj['STORE_DIR']

    sync_metadata_and_files(remote_server, output_dir, remote_metadata_path, store_dir, remote_store_dir)
    recreate_from_store('titanic-metadata.json', output_dir, store_dir)
    click.echo(f"Synced and recreated {output_dir} from {remote_server} using {remote_metadata_path}.")


@cli.command()
@click.argument('metadata_paths', type=click.Path(exists=True), nargs=-1)
@click.pass_context
def prune(ctx, metadata_paths):
    store_dir = ctx.obj['STORE_DIR']
    if not metadata_paths:
        click.echo("No metadata paths provided.")
        return
    deleted_size = prune_store(metadata_paths, store_dir)
    click.echo(f"Pruned {deleted_size} bytes from the store.")
