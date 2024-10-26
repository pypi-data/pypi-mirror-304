from setuptools import setup

METADATA_ENTRY_POINT = 'ovos-redis-mic-plugin=ovos_redis_mic_plugin:RedisMicStreamPlugin'


setup(
    name='ovos-redis-mic-plugin',
    version='0.0.0a1',
    packages=['ovos_redis_mic_plugin'],
    url='',
    license='',
    author='jarbasAi',
    author_email='jarbasai@mailfence.com',
    description='',
    entry_points={
        'neon.plugin.audio': METADATA_ENTRY_POINT
    }
)
