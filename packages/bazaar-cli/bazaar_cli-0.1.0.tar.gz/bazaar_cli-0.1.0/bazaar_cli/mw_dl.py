import click
import pyzipper
from click_default_group import DefaultGroup

from bazaar_cli.bazaarwrapper import Bazaar
from bazaar_cli.common import get_api_key


@click.group(name="download", cls=DefaultGroup, default="hash", default_if_no_args=True)
def main():
    """Download samples."""


@main.command("hash")
@click.argument("sample_hash", type=click.STRING, required=True)
@click.option("-u", "--unzip", is_flag=True, help="unzip malware sample")
def download_hash(sample_hash: str, unzip: bool):
    """Download sample by hash."""
    if len(sample_hash) != 64:
        print("[!] Hash size mismatch")
        return

    api_key = get_api_key()
    bz = Bazaar(api_key)
    bz.download_sample(sample_hash)

    if unzip:
        do_unzip(f"{sample_hash}.zip")


def do_unzip(zipfile: str) -> None:
    with pyzipper.AESZipFile(zipfile) as f:
        f.pwd = b'infected'
        filename = f.infolist()[0].filename
        content = f.read(f.infolist()[0].filename)
        open(filename, "wb").write(content)
