import logging
import threading

from model_service.settings import parse_args

logger = logging.getLogger(__name__)

args = parse_args()

semaphore = threading.Semaphore(value=args.max_concurrent_requests)