import logging, traceback
from pathlib import Path
from .video_generator import VideoGenerator
from .audio_generator import AudioGenerator
from .lip_sync import LipSyncer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('flashai.jobs')

JOBS_DIR = Path('/data/storage') if '/data/storage' else Path('/tmp/flashai_storage')

def job_status(job_id: str):
    job_dir = JOBS_DIR / job_id
    if not job_dir.exists():
        return {'status':'not_found'}
    if (job_dir / 'final.mp4').exists():
        return {'status':'finished', 'output':'/api/download/' + job_id}
    if (job_dir / 'error.txt').exists():
        return {'status':'failed', 'error': (job_dir / 'error.txt').read_text()}
    return {'status':'processing'}

def process_job(job_dir: str, dubbing_text: str, voice: str):
    job_dir = Path(job_dir)
    logger.info('Processing job %s', job_dir)
    try:
        image_path = job_dir / 'input.png'
        out_video = job_dir / 'video.mp4'
        final_output = job_dir / 'final.mp4'
        vg = VideoGenerator()
        vg.generate_from_image(str(image_path), str(out_video), duration=30, fps=12)
        ag = AudioGenerator()
        wav = ag.text_to_speech(dubbing_text, voice, job_dir / 'audio.wav')
        ls = LipSyncer()
        video_with_lips = job_dir / 'video_lips.mp4'
        ls.apply_lip_sync(str(out_video), str(wav), str(video_with_lips))
        final_source = video_with_lips if video_with_lips.exists() else out_video
        vg.mux_audio_video(str(final_source), str(wav), str(final_output))
        logger.info('Job completed: %s', final_output)
        return True
    except Exception as e:
        tb = traceback.format_exc()
        (job_dir / 'error.txt').write_text(tb)
        logger.exception('Job failed')
        return False
