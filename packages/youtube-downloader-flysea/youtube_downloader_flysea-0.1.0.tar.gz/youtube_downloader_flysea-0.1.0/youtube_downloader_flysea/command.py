import os.path
import pathlib
import shutil
import subprocess

import click
import pytubefix


# noinspection PyBroadException
def download(url: str, target_dir: str, target_filename: str = None):
    yt = pytubefix.YouTube(url)
    res_137 = [item for item in yt.streams if item.itag == 137]
    res_251 = [item for item in yt.streams if item.itag == 251]

    if len(res_137) is None or len(res_251) is None:
        click.echo("1080p not found")
        exit(1)

    caption = None
    if yt.captions.get('en') is not None:
        caption = yt.captions['en']
        click.echo("Using english captions")
    elif yt.captions.get('a.en') is not None:
        caption = yt.captions['a.en']
        click.echo("Using auto-generated english captions")
    else:
        click.echo("No captions found")

    target_path = pathlib.Path(target_dir)
    # mkdir tmp work dir
    target_tmp_path = target_path.joinpath('tmp')
    target_tmp_path.mkdir(parents=True, exist_ok=True)

    video = res_137[0]
    audio = res_251[0]

    video_name = video.default_filename
    video_name_without_ext, video_ext = os.path.splitext(video_name)

    # target video path
    if target_filename is None:
        target_filename = video_name_without_ext
    target_video_path = target_path.joinpath(
        f'{target_filename}{video_ext}')

    try:
        video_path = video.download(output_path=target_tmp_path)
        click.secho(f"Downloaded tmp video success!", fg='green')
        click.echo(f"\tvideo_path: {video_path}")
        audio_path = audio.download(output_path=target_tmp_path)
        click.secho(f"Downloaded tmp audio success! {audio_path}", fg='green')
        click.echo(f"\taudio_path: {audio_path}")
        caption_path = None
        if caption is not None:
            caption_path = pathlib.Path(target_path).joinpath(f'{target_filename}.srt')
            with open(pathlib.Path(target_path).joinpath(f'{target_filename}.srt'), 'w', encoding='utf-8') as f:
                f.write(caption.generate_srt_captions())
                click.secho(f"Downloaded caption success!", fg='green')
                click.echo(f"\tcaption_path: {caption_path}")

        # merge video、audio and caption
        if caption is not None:
            commands = [r'E:\program\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe', '-i',
                        video_path, '-i',
                        audio_path, '-i',
                        caption_path, '-c:v', 'copy', '-c:a', 'copy',
                        '-c:s', 'mov_text', '-metadata:s:s:0', 'language=eng', '-disposition:s:0', 'default',
                        target_video_path, '-y']
        else:
            commands = [r'E:\program\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe', '-i',
                        video_path, '-i',
                        audio_path, '-c:v', 'copy', '-c:a', 'copy',
                        target_video_path, '-y']
        click.secho("Start merging video、audio and caption", fg='green')
        result = subprocess.run(commands, shell=True, capture_output=True, text=True, encoding='utf-8')
    except Exception as ex:
        click.secho(f"Error occurred exception: {ex}", fg='red')
        exit(1)

    if result.returncode != 0:
        click.secho(f"Error occurred! result: {result.returncode}", fg='red')
        exit(1)

    # clear tmp directory
    os.remove(video_path)
    os.remove(audio_path)
    os.rmdir(target_tmp_path)

    click.secho(f"Download Success!", fg='green')
    click.echo(f"\tFinal video: {click.style({target_video_path.as_posix()}, fg='yellow')}")
    click.launch(target_path.as_posix())


if __name__ == '__main__':
    download('https://www.youtube.com/watch?v=44FTAS-qT8Q', r'D:\youtube\1')
