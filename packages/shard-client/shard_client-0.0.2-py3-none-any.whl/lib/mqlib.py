import asyncio
import logging
import random
import string

import lib.mqtt_queue
from lib import mqtt_queue
from gmqtt import Client as MQTTClient


class MqttClient:
    def __init__(self, host: str, port: int, subscriptions: list, client_id: str, verbosity: int, logger: logging.Logger = None):
        self.host = host
        self.port = port
        self.logger = logger
        self.cid = client_id
        self.subscriptions = subscriptions
        self.client = None
        self.STOP = asyncio.Event()
        self.verbosity = verbosity
        self.outgoing_queue = lib.mqtt_queue.MessageQue('outgoing')
        self.incoming_queue = lib.mqtt_queue.MessageQue('incoming')
        self.running = True

    def _print(self, text, _type='ok'):
        if self.logger is None:
            if _type == 'good':
                print('[+] %s'% text)
            elif _type == 'bad':
                print('[-] %s' % text)
            elif _type == 'ok':
                print('[*] %s' % text)
            else:
                print('[!] %s' % text)
        else:
            if _type in ['ok', 'good']:
                self.logger.info(text)
            elif _type in 'bad':
                self.logger.error(text)

    def on_connect(self,client, flags, rc, properties):
        self._print('Connected')

    def on_message(self, client, topic, payload, qos, properties):
        if self.verbosity > 0:
            self._print(f'RECV MSG: {topic} {payload}')
        self.incoming_queue.add(topic, payload)

    def on_subscribe(self, client, mid, qos, properties):
        self._print('SUBSCRIBED')

    def on_disconnect(self, client, packet, exc=None):
        self._print('Disconnected')

    def ask_exit(self, *args):
        self.STOP.set()

    def subscribe(self, topics: list):
        for topic in topics:
            self._print(f'Subscribing to {topic}')
            self.client.subscribe(topic)

    def publish(self, topic, message, qos=1):
        self._print(f'Publishing ... {message} to {topic}')
        self.client.publish(topic, message, qos=qos)

    async def publish_from_que(self):
        self._print('Start pub from que ..')
        while self.running:
            msg = self.outgoing_queue.get()
            if msg:
                self.publish(topic=msg[0], message=msg[1])
            await asyncio.sleep(1)

    def shutdown(self):
        self.running = False

    async def start_loop(self):
        cid = self.cid + '_' + ''.join(random.sample(string.hexdigits, 6))
        self.client = MQTTClient(client_id=cid)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.on_disconnect = self.on_disconnect

        # Connect to mqtt proxy
        await self.client.connect(host=self.host, port=self.port)
        self.subscribe(self.subscriptions)
        await self.publish_from_que()
        await self.STOP.wait()
        await self.client.disconnect()


async def main(host: str, port: int = 1883, subscriptions: list = None, client_id: str = 'client_0'):
    if not subscriptions:
        subscriptions = ['/test']
    mq = MqttClient(host=host, port=port, subscriptions=subscriptions, client_id=client_id,  verbosity=0)
    # loop.run_until_complete(mq.start_loop())
    tasks = set()
    tasks.add(asyncio.create_task(mq.start_loop()))
    await asyncio.gather(*tasks)

