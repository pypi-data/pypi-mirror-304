import redis
from ovos_bus_client.session import SessionManager
from ovos_config import Configuration
from ovos_plugin_manager.templates.transformers import AudioTransformer


class RedisMicStreamPlugin(AudioTransformer):
    """makes the last STT audio available via redis backend
     `mic_id` becomes available in `message.context`, enables downstream tasks like speaker_recognition
    """

    def __init__(self, config=None):
        config = config or {}
        super().__init__("ovos-redis-mic-plugin", 10, config)
        # Redis connection
        kwargs = Configuration().get("redis", {"host": "127.0.0.1", "port": 6379})
        self.r = redis.Redis(**kwargs)
        self.r.ping()

    def transform(self, audio_data):
        """ return any additional message context to be passed in
        recognize_loop:utterance message
        """
        sess = SessionManager.get()
        mic_id = "mic::" + sess.session_id
        self.r.set(mic_id, audio_data)
        return audio_data, {"mic_id": mic_id}

    def default_shutdown(self):
        self.r.shutdown()
