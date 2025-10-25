import logging, subprocess, shutil
from pathlib import Path
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('flashai.lipsync')

class LipSyncer:
    def __init__(self, wav2lip_repo_dir='/opt/wav2lip'):
        self.wav2lip_repo = Path(wav2lip_repo_dir)

    def has_face(self, video_path: str) -> bool:
        try:
            import cv2
            vid = cv2.VideoCapture(video_path)
            ret, frame = vid.read()
            vid.release()
            if not ret:
                return False
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            return len(faces) > 0
        except Exception:
            return False

    def apply_lip_sync(self, video_path: str, audio_path: str, out_path: str):
        video_path = Path(video_path)
        out_path = Path(out_path)
        if not self.has_face(str(video_path)):
            logger.info('No face detected; skipping lip-sync.')
            return None
        wav2lip_script = self.wav2lip_repo / 'inference.py'
        if wav2lip_script.exists():
            cmd = [
                'python', str(wav2lip_script),
                '--checkpoint_path', str(self.wav2lip_repo / 'checkpoints' / 'wav2lip_gan.pth'),
                '--face', str(video_path),
                '--audio', str(audio_path),
                '--outfile', str(out_path)
            ]
            subprocess.run(cmd, check=True)
            logger.info('Wav2Lip produced %s', out_path)
            return str(out_path)
        else:
            logger.info('Wav2Lip not found; copying original video.')
            shutil.copy(str(video_path), str(out_path))
            return str(out_path)
