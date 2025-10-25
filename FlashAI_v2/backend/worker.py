import os, logging
from redis import Redis
from rq import Worker, Queue, Connection
from dotenv import load_dotenv
load_dotenv()
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
redis_conn = Redis.from_url(REDIS_URL)
listen = ['default']
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('flashai.worker')
if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        logger.info('Starting worker...')
        worker.work(with_scheduler=True)
