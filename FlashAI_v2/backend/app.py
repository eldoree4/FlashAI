import os, uuid, logging, time
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from redis import Redis
from rq import Queue
from pathlib import Path
from dotenv import load_dotenv
from modules.jobs import job_status

load_dotenv()
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
STORAGE_DIR = Path(os.getenv('STORAGE_DIR', '/data/storage'))
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

redis_conn = Redis.from_url(REDIS_URL)
q = Queue(connection=redis_conn)

app = FastAPI(title='FlashAI API')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('flashai.app')

@app.get('/', response_class=HTMLResponse)
def index():
    html = Path(__file__).parent.joinpath('static', 'index.html').read_text()
    return HTMLResponse(content=html)

@app.post('/api/generate')
async def generate(image: UploadFile = File(...), dubbing_text: str = Form(''), voice: str = Form('default')):
    job_id = str(uuid.uuid4())
    job_dir = STORAGE_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    input_path = job_dir / 'input.png'
    with open(input_path, 'wb') as f:
        f.write(await image.read())
    job = q.enqueue('modules.jobs.process_job', str(job_dir), dubbing_text, voice, job_timeout=60*60*6)
    logger.info('Enqueued job %s', job.id)
    return {'job_id': job.id, 'job_uuid': job_id}

@app.get('/api/status/{job_id}')
def status(job_id: str):
    return job_status(job_id)

@app.get('/api/download/{job_uuid}')
def download(job_uuid: str):
    out = STORAGE_DIR / job_uuid / 'final.mp4'
    if not out.exists():
        raise HTTPException(status_code=404, detail='Output not ready')
    return FileResponse(out, media_type='video/mp4', filename='flashai_output.mp4')

@app.get('/health')
def health():
    return {'status':'ok', 'time': time.time()}
