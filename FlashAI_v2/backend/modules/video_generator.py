import logging, subprocess, tempfile
from pathlib import Path
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('flashai.video_generator')

class VideoGenerator:
    def __init__(self, models_dir=None):
        self.models_dir = Path(models_dir) if models_dir else Path('/app/backend/models')  # inside container
        self.tmpdir = Path(tempfile.gettempdir())

    def generate_from_image(self, image_path: str, out_path: str, duration: int = 30, fps: int = 12):
        image_path = Path(image_path)
        out_path = Path(out_path)
        width = 1280
        height = 720
        total_frames = int(duration * fps)
        vf = f"zoompan=z='zoom+0.0008':d={total_frames}:s={width}x{height},framerate={fps}"
        cmd = [
            'ffmpeg', '-y', '-loop', '1', '-i', str(image_path),
            '-vf', vf,
            '-t', str(duration), '-pix_fmt', 'yuv420p', str(out_path)
        ]
        logger.info('Running ffmpeg zoompan (prototype)')
        subprocess.run(cmd, check=True)
        logger.info('Generated prototype video: %s', out_path)
        return str(out_path)

    def mux_audio_video(self, video_path: str, audio_path: str, final_path: str):
        cmd = [
            'ffmpeg', '-y', '-i', video_path, '-i', audio_path,
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
            '-c:a', 'aac', '-b:a', '128k', '-shortest', final_path
        ]
        subprocess.run(cmd, check=True)
        return final_path
