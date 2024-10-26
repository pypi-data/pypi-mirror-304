import click
import asyncio
from treelib import Tree

import joule.api
from joule import errors
from joule.cli.config import Config, pass_config
from joule.api import BaseNode
from joule.api.folder import Folder
from joule.api.data_stream import DataStream
from joule.api.event_stream import EventStream


@click.command(name="move")
@click.argument("source")
@click.argument("destination")
@pass_config
def move(config: Config, source: str, destination: str):
    """Move a folder to a new location."""

    try:
        asyncio.run(
            config.node.folder_move(source, destination))
    except errors.ApiError as e:
        raise click.ClickException(str(e)) from e
    finally:
        asyncio.run(
            config.close_node())

    click.echo("OK")


@click.command(name="rename")
@click.argument("folder")
@click.argument("name")
@pass_config
def rename(config: Config, folder, name):
    """Rename a folder."""

    try:
        asyncio.run(
            _run_rename(config.node, folder, name))
    except errors.ApiError as e:
        raise click.ClickException(str(e)) from e
    finally:
        asyncio.run(
            config.close_node())

    click.echo("OK")


async def _run_rename(node: BaseNode, folder_path: str, name: str):
    folder = await node.folder_get(folder_path)
    folder.name = name
    await node.folder_update(folder)


@click.command(name="delete")
@click.option("--recursive", "-r", is_flag=True)
@click.argument("folder")
@pass_config
def delete(config, folder, recursive):
    """Delete a folder and all contents."""

    try:
        asyncio.run(
            config.node.folder_delete(folder, recursive))
        click.echo("OK")
    except errors.ApiError as e:
        raise click.ClickException(str(e))
    finally:
        asyncio.run(
            config.close_node())


@click.command(name="list")
@click.argument("path", default="/")
@click.option("--layout", "-l", is_flag=True, help="include stream layout")
@click.option("--status", "-s", is_flag=True, help="include stream status")
@click.option("--id", "-i", is_flag=True, help="show ID's")
@pass_config
def list(config, path, layout, status, id):
    """Display folder hierarchy (directory layout)."""

    try:
        asyncio.run(
            _run_list(config.node, path, layout, status, id))
    except errors.ApiError as e:
        raise click.ClickException(str(e)) from e
    finally:
        asyncio.run(
            config.close_node())


async def _run_list(node: BaseNode, path: str, layout: bool, status: bool, showid: bool):
    tree = Tree()
    if path == "/":
        root = await node.folder_root()
        root.name = ""  # omit root name
        if len(root.children) == 0:
            click.echo("No folders, this node is empty.")
            return
    else:
        root = await node.folder_get(path)
    _process_folder(tree, root, None, layout, status, showid)
    click.echo("Legend: [" + click.style("Folder", bold=True) + "] [Data Stream] ["
               + click.style("Event Stream", fg='cyan') + "]")
    if status:
        click.echo("\t" + click.style("\u25CF ", fg="green") + "active  " +
                   click.style("\u25CF ", fg="cyan") + "configured")
    click.echo(tree.show(stdout=False))


def _process_folder(tree: Tree, folder: Folder, parent_id,
                    layout: bool, status: bool, showid: bool):
    tag = click.style(folder.name, bold=True)
    if showid:
        tag += " (%d)" % folder.id
    identifier = "f%d" % folder.id
    tree.create_node(tag, identifier, parent_id)
    for stream in folder.data_streams:
        _process_data_stream(tree, stream, identifier, layout, status, showid)
    for stream in folder.event_streams:
        _process_event_stream(tree, stream, identifier, showid)
    for child in folder.children:
        _process_folder(tree, child, identifier, layout, status, showid)


def _process_data_stream(tree: Tree, stream: DataStream, parent_id,
                         layout: bool, status: bool, showid: bool):
    tag = stream.name
    if showid:
        tag += " (%d)" % stream.id
    if layout:
        tag += " (%s)" % stream.layout
    if status:
        if stream.active:
            tag = click.style("\u25CF ", fg="green") + tag
        elif stream.locked:
            tag = click.style("\u25CF ", fg="cyan") + tag

    identifier = "s%d" % stream.id
    tree.create_node(tag, identifier, parent_id)


def _process_event_stream(tree: Tree, stream: EventStream, parent_id, showid: bool):
    tag = stream.name
    if showid:
        tag += " (%d)" % stream.id
    tag = click.style(tag, fg="cyan")
    identifier = "e%d" % stream.id
    tree.create_node(tag, identifier, parent_id)


action_on_event_conflict = None

@click.command(name="copy")
@click.argument("source")
@click.argument("destination")
@click.option('-s', "--start", help="timestamp or descriptive string")
@click.option('-e', "--end", help="timestamp or descriptive string")
@click.option('-n', '--new', help="copy starts at the last timestamp of the destination", is_flag=True)
@click.option('-a', '--action', help="action to take if events already exist in the destination",
              type=click.Choice(['skip', 'ignore', 'replace', 'prompt']), default='prompt')
@click.option("-d", "--destination-node")
@pass_config
def copy(config, source, destination, start, end, new, action, destination_node):
    """Recursively copy a folder to a new location"""
    global action_on_event_conflict
    action_on_event_conflict = action
    try:
        if destination_node is not None:
            destination_node = joule.api.get_node(destination_node)
        else:
            destination_node = config.node
        asyncio.run(
            _run_copy(config.node, source, destination, start, end, new, destination_node))
    except errors.ApiError as e:
        raise click.ClickException(str(e)) from e
    finally:
        asyncio.run(
            config.close_node())

async def _run_copy(source_node, source, destination, start, end, new, destination_node) -> None:
    from joule.cli.data.copy import _run as run_data_copy # lazy import
    from joule.cli.event.copy import _run as run_event_copy # lazy import
    from joule.cli.event.copy import has_existing_events # lazy import

    global action_on_event_conflict
    if type(source) is str:
        source_folder = await source_node.folder_get(source)
    else:
        source_folder = source
    for child in source_folder.children:
        await _run_copy(source_node, child, f"{destination}/{child.name}", start, end, new,
                        destination_node)
    for data_stream in source_folder.data_streams:
        click.echo(f"Writing Data Stream {destination}/{data_stream.name}")
        try:
            await run_data_copy(source_node, start, end, new, destination_node, data_stream,
                                f"{destination}/{data_stream.name}")
        except errors.ApiError as e:
            if "has no data" in str(e):
                print("\t skipping, this stream has no data")
            else:
                raise e
    replace = False  # appease the typechecker
    for source_stream in source_folder.event_streams:
        destination_stream = f"{destination}/{source_stream.name}"
        click.echo(f"Writing Event Stream {destination_stream}")
        # handle potential event conflicts
        if await has_existing_events(destination_node, destination_stream, start, end):
            if action_on_event_conflict == 'prompt':
                print("""
There are already events in this destination, select how you want to proceed:
[s]kip: skip this event stream
[i]gnore: ignore existing destination events, add source events. This may result in duplicate events
[r]eplace: remove all destination events, then add source events. This may result in data loss
Select an option (use a captial letter to use this action for all event streams):""")
                action = click.getchar()
                if action == 's':
                    print("\t skipping this event stream")
                    current_action = 'skip'
                elif action == 'S':
                    print("\t skipping all event streams with conflicts")
                    current_action = 'skip'
                    action_on_event_conflict = 'skip'
                elif action == 'i':
                    print("\t ignoring existing events, running copy anyway")
                    current_action = 'ignore'
                elif action == 'I':
                    print("\t ignoring existing events, running copy anyway on all event streams with conflicts")
                    current_action = 'ignore'
                    action_on_event_conflict = 'ignore'
                elif action == 'r':
                    print("\t removing events in destination before running copy")
                    current_action = 'replace'
                elif action == 'R':
                    print("\t removing events in destination before running copy on all event streams with conflicts")
                    current_action = 'replace'
                    action_on_event_conflict = 'replace'
                else:
                    raise click.ClickException("\t invalid option, cancelling copy")
            else:
                current_action = action_on_event_conflict
            if current_action == 'skip':
                continue
            elif current_action == 'ignore':
                replace = False
            elif current_action == 'replace':
                replace = True
            else:
                raise click.ClickException(f"Invalid choice [{action_on_event_conflict}]")

        await run_event_copy(source_node, destination_node, start, end, new, replace, source_stream,
                             destination_stream)


@click.group(name="folder")
def folders():
    """Manage folders."""
    pass  


folders.add_command(copy)
folders.add_command(move)
folders.add_command(delete)
folders.add_command(rename)
folders.add_command(list)
