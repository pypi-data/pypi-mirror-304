
### Redis Server

for voice and face recognition a companion Redis server needs to be running

You can find dedicated redis documentation elsewhere, the easiest way to get started is with docker

`docker run -p 6379:6379 --name redis -d redis`

This is where buffers for mic and camera data are stored, allowing access to remote cameras/mic data from several devices

a OVOS skill can then access a specific camera/microphone by id by retrieving the feed from redis

Redis access is configured globally for all OVOS components in `mycroft.conf`

```json
{
  "redis": {
    "host": "my-redis.cloud.redislabs.com",
    "port": 6379,
    "username": "default",
    "password": "secret",
    "ssl": true,
    "ssl_certfile": "./redis_user.crt",
    "ssl_keyfile": "./redis_user_private.key",
    "ssl_ca_certs": "./redis_ca.pem"
  }
}
```

### Plugin

```json
"listener": {
    "audio_transformers": {
        "ovos-redis-mic-plugin": {}
    }
}
```

### Skills

```python
class RedisMicReader:
    """access mic from https://github.com/OpenVoiceOS/ovos-...-redis-mic"""
    def __init__(self,  device_name: str):
        # Redis connection
        kwargs = Configuration().get("redis", {"host": "127.0.0.1", "port": 6379})
        self.r = redis.Redis(**kwargs)
        self.r.ping()
        self.mic_id = device_name

    def get(self):
        """Retrieve Numpy array from Redis mic 'self.name' """
        return self.r.get(self.mic_id)


# and in a skill/plugin
def my_intent(message):
    mic_id = message.context["mic_id"]
    remote_mic = RedisMicReader(mic_id)
    audio = remote_mic.get()  # last STT audio bytes
    # do stuff
```