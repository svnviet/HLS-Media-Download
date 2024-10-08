import os
import shutil
import subprocess

import requests

from app.dtos import HLSConvert, HLSDownload

# current_path = os.path.dirname(os.path.abspath(__file__))


class HLSService:

    hls_save = '/var/www/movie/'
    video_save = '~/root/downloads/'
    # hls_save = current_path
    # video_save = current_path
    hls_segment_duration = 10

    async def video_download_to_hls(self, video: HLSConvert):
        hls_dir = os.path.join(self.hls_save, video.uuid)
        os.makedirs(hls_dir, exist_ok=True)

        video_dir = os.path.join(self.video_save, video.uuid)
        os.makedirs(video_dir, exist_ok=True)

        video_path = await self._video_download_by_url(video=video, video_dir=video_dir)

        image_path = os.path.join(hls_dir, "{}.jpg".format(video.uuid))
        await self._picture_download_by_url(url=video.pic_url, save_path=image_path)

        hls_path = os.path.join(hls_dir, video.uuid + '.m3u8')
        is_converted = await self._video_to_hls(input_video_path=video_path, output_hls_path=hls_path)
        if not is_converted:
            raise EOFError

    async def hls_content_download(self, hls: HLSDownload) -> None:
        hls_dir = os.path.join(self.hls_save, hls.uuid)
        os.makedirs(hls_dir, exist_ok=True)

        video_dir = os.path.join(self.video_save, hls.uuid)
        os.makedirs(video_dir, exist_ok=True)

        video_path = await self._video_download_by_m3u8_url(hls, video_dir)

        save_dir = os.path.join(self.hls_save, hls.uuid)
        os.makedirs(save_dir, exist_ok=True)
        image_path = os.path.join(save_dir, "{}.jpg".format(hls.uuid))
        await self._picture_download_by_url(url=hls.pic_url, save_path=image_path)

        hls_path = os.path.join(hls_dir, hls.uuid + '.m3u8')
        is_converted = await self._video_to_hls(input_video_path=video_path, output_hls_path=hls_path)
        if not is_converted:
            raise EOFError

    async def _video_download_by_url(self, video: HLSConvert, video_dir: str) -> str:
        video_path = os.path.join(video_dir, video.uuid + '.mp4')

        response = requests.get(video.url, stream=True)
        response.raise_for_status()
        with open(video_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return video_path

    async def _video_download_by_m3u8_url(self, hls: HLSDownload, video_dir):
        video_path = os.path.join(video_dir, hls.uuid + '.mp4')
        command = [
            "ffmpeg",
            "-i", f"{hls.url}",
            "-c", "copy",  # Copy the video stream
            f"{video_path}",
        ]
        try:
            print(f"Downloading {hls.url}")
            subprocess.run(command, check=True)
            print(f"Finished downloading save to {video_path}")
            return video_path
        except subprocess.CalledProcessError as e:
            return False

    @staticmethod
    async def _picture_download_by_url(url: str, save_path: str) -> None:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)

    @staticmethod
    async def _segment_part_download(line_content, save_dir, base_url) -> None:
        if line_content and line_content.startswith("#"):  # Ignore comments and metadata
            return None
        segment_url = line_content
        if not segment_url.startswith("http"):
            segment_url = f"{base_url}/{segment_url}"

        segment_name = segment_url.split("/")[-1]
        segment_path = os.path.join(save_dir, segment_name)

        segment_data = requests.get(segment_url)
        with open(segment_path, "wb") as f:
            f.write(segment_data.content)

    async def _video_to_hls(self, input_video_path, output_hls_path) -> bool:
        command = [
            "ffmpeg",
            "-i", f"{input_video_path}",
            "-codec:v", "copy",  # Copy the video stream
            "-codec:a", "copy",  # Copy the audio stream
            "-start_number", "0",
            "-hls_time", str(self.hls_segment_duration),
            "-hls_list_size", "0",
            "-f", "hls", f"{output_hls_path}",
        ]
        try:
            print(f"Convert to hls {input_video_path}")
            subprocess.run(command, check=True)
            print(f"Save hls to {output_hls_path}")
            return True
        except subprocess.CalledProcessError as e:
            return False
