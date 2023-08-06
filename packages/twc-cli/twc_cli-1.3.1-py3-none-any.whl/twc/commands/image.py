"""Image management commands."""

import re
import sys

import click
from click_aliases import ClickAliasedGroup

from twc import fmt
from . import (
    create_client,
    handle_request,
    options,
    debug,
    GLOBAL_OPTIONS,
    OUTPUT_FORMAT_OPTION,
)


@handle_request
def _image_list(client, *args, **kwargs):
    return client.get_images(*args, **kwargs)


@handle_request
def _image_get(client, *args, **kwargs):
    return client.get_image(*args, **kwargs)


@handle_request
def _image_create(client, *args, **kwargs):
    return client.create_image(*args, **kwargs)


@handle_request
def _image_remove(client, *args, **kwargs):
    return client.delete_image(*args, **kwargs)


@handle_request
def _image_set_property(client, *args, **kwargs):
    return client.update_image(*args, **kwargs)


@handle_request
def _image_upload(client, *args, **kwargs):
    return client.upload_image(*args, **kwargs)


# ------------------------------------------------------------- #
# $ twc image                                                   #
# ------------------------------------------------------------- #


@click.group("image", cls=ClickAliasedGroup)
@options(GLOBAL_OPTIONS[:2])
def image():
    """Manage disk images."""


# ------------------------------------------------------------- #
# $ twc image list                                              #
# ------------------------------------------------------------- #


def print_images(response: object, filters: str):
    if filters:
        images = fmt.filter_list(response.json()["images"], filters)
    else:
        images = response.json()["images"]

    table = fmt.Table()
    table.header(
        [
            "UUID",
            "NAME",
            "REGION",
            "STATUS",
            "DISK",
            "SIZE",
        ]
    )
    for img in images:
        table.row(
            [
                img["id"],
                img["name"],
                img["location"],
                img["status"],
                img["disk_id"],
                str(round(img["size"] / 1024)) + "G",
            ]
        )
    table.print()


@image.command("list", aliases=["ls"], help="List images.")
@options(GLOBAL_OPTIONS)
@options(OUTPUT_FORMAT_OPTION)
@click.option(
    "--limit",
    type=int,
    default=500,
    show_default=True,
    help="Items to display.",
)
@click.option("--filter", "-f", "filters", default="", help="Filter output.")
@click.option("--region", help="Use region (location).")
@click.option(
    "--with-deleted",
    is_flag=True,
    help="Show all images including deleted images.",
)
def image_list(
    config,
    profile,
    verbose,
    output_format,
    limit,
    filters,
    region,
    with_deleted,
):
    if filters:
        filters = filters.replace("region", "location")
    if region:
        if filters:
            filters = filters + f",location:{region}"
        else:
            filters = f"location:{region}"

    client = create_client(config, profile)
    response = _image_list(client, limit=limit, with_deleted=with_deleted)
    fmt.printer(
        response,
        output_format=output_format,
        filters=filters,
        func=print_images,
    )


# ------------------------------------------------------------- #
# $ twc image get                                               #
# ------------------------------------------------------------- #


def print_image(response: object):
    table = fmt.Table()
    table.header(
        [
            "UUID",
            "NAME",
            "REGION",
            "STATUS",
            "DISK",
            "SIZE",
        ]
    )
    img = response.json()["image"]
    table.row(
        [
            img["id"],
            img["name"],
            img["location"],
            img["status"],
            img["disk_id"],
            str(round(img["size"] / 1024)) + "G",
        ]
    )
    table.print()


@image.command("get", help="Get image.")
@options(GLOBAL_OPTIONS)
@options(OUTPUT_FORMAT_OPTION)
@click.option("--status", is_flag=True, help="Print image status only.")
@click.argument("image_id", required=True)
def image_get(config, profile, verbose, output_format, status, image_id):
    client = create_client(config, profile)
    response = _image_get(client, image_id)
    if status:
        _status = response.json()["image"]["status"]
        if _status == "created":
            click.echo(_status)
            sys.exit(0)
        else:
            sys.exit(_status)
    fmt.printer(response, output_format=output_format, func=print_image)


# ------------------------------------------------------------- #
# $ twc image create                                            #
# ------------------------------------------------------------- #


@image.command("create", help="Create image.")
@options(GLOBAL_OPTIONS)
@options(OUTPUT_FORMAT_OPTION)
@click.option(
    "--name", type=str, default=None, help="Image human readable name."
)
@click.option("--desc", type=str, default=None, help="Image description.")
@click.argument("disk_id", type=int, required=True)
def image_create(config, profile, verbose, output_format, name, desc, disk_id):
    client = create_client(config, profile)
    response = _image_create(
        client, disk_id=disk_id, name=name, description=desc
    )
    fmt.printer(
        response,
        output_format=output_format,
        func=lambda response: click.echo(response.json()["image"]["id"]),
    )


# ------------------------------------------------------------- #
# $ twc image remove                                            #
# ------------------------------------------------------------- #


@image.command("remove", aliases=["rm"], help="Remove image.")
@options(GLOBAL_OPTIONS)
@click.confirmation_option(
    prompt="This action cannot be undone. Are you sure?"
)
@click.argument("image_id", nargs=-1, required=True)
def image_remove(config, profile, verbose, image_id):
    client = create_client(config, profile)

    for img in image_id:
        response = _image_remove(client, img)
        if response.status_code == 204:
            click.echo(img)
        else:
            fmt.printer(response)


# ------------------------------------------------------------- #
# $ twc image set-property                                      #
# ------------------------------------------------------------- #


@image.command("set-property", help="Change image name and description.")
@options(GLOBAL_OPTIONS)
@options(OUTPUT_FORMAT_OPTION)
@click.option(
    "--name", type=str, default=None, help="Image human readable name."
)
@click.option("--desc", type=str, default=None, help="Image description.")
@click.argument("image_id", required=True)
def image_set_property(
    config, profile, verbose, output_format, name, desc, image_id
):
    client = create_client(config, profile)
    response = _image_set_property(
        client, image_id, name=name, description=desc
    )
    fmt.printer(
        response,
        output_format=output_format,
        func=lambda response: click.echo(response.json()["image"]["id"]),
    )


# ------------------------------------------------------------- #
# $ twc image upload                                            #
# ------------------------------------------------------------- #


def draw_progressbar(monitor):
    print("Bytes:", monitor.bytes_read)


@image.command("upload", help="Upload image from URL.")
@options(GLOBAL_OPTIONS)
@options(OUTPUT_FORMAT_OPTION)
@click.option(
    "--name", type=str, default=None, help="Image human readable name."
)
@click.option("--desc", type=str, default=None, help="Image description.")
@click.option(
    "--os",
    "os_type",
    type=click.Choice(
        [
            "centos",
            "almalinux",
            "debian",
            "bitrix",
            "ubuntu",
            "brainycp",
            "archlinux",
            "astralinux",
            "windows",
            "custom_os",
            "other",
        ]
    ),
    default="other",
    show_default=True,
    help="OS type.",
)
@click.option(
    "--location",
    type=click.Choice(["ru-1", "ru-2", "pl-1", "kz-1", "nl-1"]),
    default="ru-1",
    show_default=True,
    help="Region to upload image.",
)
@click.argument("file", required=True)
def image_upload(
    config,
    profile,
    verbose,
    output_format,
    name,
    desc,
    os_type,
    location,
    file,
):
    client = create_client(config, profile)
    payload = {
        "name": name,
        "description": desc,
        "location": location,
        "os": os_type,
    }

    if re.match(r"https?://", file):
        debug(f"Upload URL: {file}")
        payload["upload_url"] = file
        response = _image_create(client, **payload)
    #    else:
    #        filepath = os.path.realpath(file)
    #        if os.path.exists(filepath):
    #            filesize = os.path.getsize(file)
    #            debug(f"Upload file: {filepath}")
    #            debug(f"File size (bytes): {filesize}")
    #            if filesize > 107374182400:
    #                sys.exit(f"Error: File is too large (>100G): {file}")
    #            image_id = _image_create(client, **payload).json()["image"]["id"]
    #            response = _image_upload(client, image_id, filepath)
    #        else:
    #            sys.exit(f"Error: No such file: {file}")

    fmt.printer(
        response,
        output_format=output_format,
        func=lambda response: click.echo(response.json()["image"]["id"]),
    )
