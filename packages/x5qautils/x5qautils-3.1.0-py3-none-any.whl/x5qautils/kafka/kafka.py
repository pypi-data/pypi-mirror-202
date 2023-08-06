import configparser
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from threading import Thread
from typing import Callable, Union
from uuid import uuid4

import yaml
from confluent_kafka import Producer, Consumer
from confluent_kafka.avro import AvroConsumer, AvroProducer

from api.model import BasePydantic


@dataclass
class MsgList(dict):
    key_id: str = 'id'

    def add(self, obj):
        if isinstance(obj, dict):
            _id = obj.get(self.key_id)
        else:
            _id = getattr(obj, self.key_id, uuid4())

        self[_id] = obj

    def filter(self, key):
        return list(filter(key, self.values()))

    def wait(self, func: Callable, timeout=30):
        time_start = time.time()
        while time.time() - time_start < timeout:
            if result := self.filter(func):
                return result
        else:
            raise TimeoutError(f'Not wait messages for func: {func}')


class QaConsumer(Consumer):
    pass


class QaProducer(Producer):
    def __init__(self, config):
        self.topic = config.get('topic')
        super().__init__(config)

    def send(self, message):
        if isinstance(message, BasePydantic):
            message = message.json()
        elif not isinstance(message, str):
            message = json.dumps(message)
        self.produce(self.topic, message)


class QaAvroConsumer(AvroConsumer):
    pass


class QaAvroProducer(AvroProducer):
    def __init__(self, *args, **kwargs):
        self.scheme = ""
        super().__init__(*args, **kwargs)

    def send(self, message):
        if isinstance(message, BasePydantic):
            message = message.dict()
        self.produce(value=self.scheme, key=message)


@dataclass
class KafkaClient:
    stage: str
    config: dict = None
    config_file: str = ''
    key_id: str = 'id'
    running: bool = True
    consumer: Union[QaConsumer, QaAvroConsumer] = None
    producer: Union[QaProducer, QaAvroProducer] = None
    type = property(lambda self: self.config.get('type', 'avro'))

    def __post_init__(self):
        self.msg_list_put = MsgList(self.key_id)
        self.config = {'type_': 'avro'}

        self._configure(self.config, self.config_file)
        self._create_consumer()
        self._create_producer()

    def _configure(self, config=None, config_file=None):
        if config_file:
            self.config.update(self._load_config_files(config_file))
        if config is not None:
            self.config.update(config)
        self.config['sasl.username'] = os.getenv('KAFKA_LOGIN') or self.config.get('kafka_login')
        self.config['sasl.password'] = os.getenv('KAFKA_PASSWORD') or self.config.get('kafka_password')

    def _load_config_files(self, config_file) -> dict:
        if isinstance(config_file, str):
            config_file = Path(os.getenv('PWD'), config_file)
        with config_file.open() as f:
            if config_file.suffix in ['.yml', 'yaml']:
                config = yaml.safe_load(config_file).get(self.stage, {})
                while any(isinstance(v, dict) for v in config.values()):
                    config = self._convert_dictionaries(config)
                return config

            elif config_file.suffix == '.ini':
                config = configparser.ConfigParser()
                config.read("conf.ini")  # читаем конфиг
                return {s: dict(config.items(s)) for s in config.sections()}.get(self.stage, {})

            elif config_file.suffix == '.json':
                config = json.load(f)
                return config.get('kafka', config).get(self.stage, {})
        return {}

    @staticmethod
    def _convert_dictionaries(obj) -> dict:
        new_dict = {}
        for key, value in obj.items():
            if isinstance(value, dict):
                for new_key, v in value.items():
                    new_dict[f'{key}.{new_key}'] = v
            else:
                new_dict[f'{key}'] = value

        return new_dict

    @staticmethod
    def convert_msg(msg):
        return json.dumps(msg)

    def _polling(self):
        while self.running:
            msg = self.consumer.poll()
            if isinstance(msg, str):
                msg = self.convert_msg(msg)
            self.msg_list_put.add(msg)

    def run(self):
        Thread(target=self._polling, daemon=True)

    def _create_consumer(self):
        if self.type == 'avro':
            self.consumer = QaAvroConsumer(self.config, value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        self.consumer = QaConsumer(self.config)
        self.run()

    def _create_producer(self):
        if self.type == 'avro':
            self.producer = QaAvroProducer(self.config)
        self.producer = QaProducer(self.config)

    def post_message(self, message):
        if isinstance(message, BasePydantic):
            message = message.dict()

        self.producer.send(message)
