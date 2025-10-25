import logging, subprocess, os
from pathlib import Path
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('flashai.audio_generator')

class AudioGenerator:
    def __init__(self, provider='coqui'):
        self.provider = provider

    def text_to_speech(self, text: str, voice: str, out_wav_path: Path):
        out_wav_path = Path(out_wav_path)
        out_wav_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            from TTS.api import TTS
            # Note: user must install Coqui TTS models separately
            tts = TTS(list_models()[0])
            tts.tts_to_file(text=text, file_path=str(out_wav_path))
            logger.info('Generated TTS via Coqui: %s', out_wav_path)
            return str(out_wav_path)
        except Exception:
            logger.info('Coqui not available, falling back to gTTS')
        try:
            from gtts import gTTS
            tmp_mp3 = str(out_wav_path) + '.mp3'
            gTTS(text).save(tmp_mp3)
            subprocess.run(['ffmpeg', '-y', '-i', tmp_mp3, str(out_wav_path)], check=True)
            os.remove(tmp_mp3)
            logger.info('Generated TTS via gTTS fallback: %s', out_wav_path)
            return str(out_wav_path)
        except Exception as e:
            logger.exception('TTS generation failed: %s', e)
            raise
