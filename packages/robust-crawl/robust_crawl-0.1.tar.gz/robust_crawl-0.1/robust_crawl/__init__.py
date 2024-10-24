import json

try:
    with open('./config/robust_crawl_config.json', "r") as f:
        ROBUST_CRAWL_CONFIG = json.load(f)
except FileNotFoundError:
    ROBUST_CRAWL_CONFIG = {}
    
from .request_pool import RequestPool
import page_func

__all__ = [
    "RequestPool",
    "page_func"
]