import uuid
from redis._compat import b

class MockRedisLock(object):

    """
    Poorly imitate a Redis lock object from redis-py
    to allow testing without a real redis server.
    """

    def __init__(self, redis, name, timeout=None, sleep=0.1):
        """Initialize the object."""
        self.redis = redis
        self.name = name
        self.acquired_until = None
        self.timeout = timeout
        self.sleep = sleep

    def acquire(self, blocking=True):  # pylint: disable=R0201,W0613
        """Emulate acquire."""
        token = b(uuid.uuid1().hex)
        if self.redis.setnx(self.name, token):
            return True
        return False

    def release(self):   # pylint: disable=R0201
        """Emulate release."""
        self.redis.delete(self.name)
        return

    def __enter__(self):
        return self.acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
