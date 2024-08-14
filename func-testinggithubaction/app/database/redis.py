# import os
# from dotenv import load_dotenv
# import redis
# from urllib.parse import urlparse
# from app.util.logger import logger

# # Load environment variables from .env file
# load_dotenv()

# class RedisClient:
#     def __init__(self):
#         redis_url = os.getenv('REDIS_CONFIG')
#         if not redis_url:
#             raise ValueError("REDIS_CONFIG environment variable is not set")
        
#         parsed_url = urlparse(redis_url)
#         if not all([parsed_url.hostname, parsed_url.port, parsed_url.path[1:]]):
#             raise ValueError("Invalid REDIS_CONFIG format")
        
#         self.host = parsed_url.hostname
#         self.port = parsed_url.port
#         self.db = int(parsed_url.path[1:])  # Skip the leading '/'
#         self.password = parsed_url.password
        
#         try:
#             self.client = redis.StrictRedis(
#                 host=self.host,
#                 port=self.port,
#                 db=self.db,
#                 password=self.password,
#                 decode_responses=True
#             )
#             logger.info(f"Successfully connected to Redis at {self.host}:{self.port} (DB: {self.db})")
#         except Exception as e:
#             raise RuntimeError(f"Failed to connect to Redis: {e}")

#     def get_client(self):
#         return self.client

# redis_client = RedisClient().get_client()
