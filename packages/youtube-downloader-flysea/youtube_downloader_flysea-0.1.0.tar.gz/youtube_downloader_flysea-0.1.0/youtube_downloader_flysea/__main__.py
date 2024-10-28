import click

# import .command as yt_command
import youtube_downloader_flysea.command as yt_command


@click.command('yt')
@click.option('--url', '-u', required=True, help='Youtube video url')
@click.option('--target_dir', '-t', required=True, help='Target directory')
@click.option('--target_filename', '-f', help='Target filename')
def cli(url: str, target_dir: str, target_filename: str = None):
    """
    A youtube downloader
    """
    yt_command.download(url, target_dir, target_filename)


def main():
    cli()


if __name__ == '__main__':
    cli()
