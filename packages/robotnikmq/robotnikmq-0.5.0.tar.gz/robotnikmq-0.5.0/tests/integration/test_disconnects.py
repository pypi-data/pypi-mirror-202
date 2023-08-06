from itertools import count
from multiprocessing import Process, Event as event
from pprint import pprint
from time import sleep

from pytest_rabbitmq import factories

from robotnikmq.core import Message
from robotnikmq.subscriber import Subscriber
from robotnikmq.topic import Topic

from .utils import META_QUEUE, config_for, initialize_rabbitmq

robotnikmq_proc = factories.rabbitmq_proc(port=8827)


def test_server_disconnect_and_reconnect(robotnikmq_proc):
    initialize_rabbitmq(robotnikmq_proc)
    robotnikmq_config = config_for(robotnikmq_proc, 10, 2, 5)
    msg_received = event()
    rabbitmq_stopped = event()

    def callback(msg: Message) -> None:
        pprint(msg.to_dict())
        msg_received.set()

    def sub():
        Subscriber(config=robotnikmq_config).bind(exchange=META_QUEUE).run(callback)

    def pub():
        medium = Topic(
            exchange=META_QUEUE,
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        for i in count():
            sleep(1)
            medium.broadcast(Message({"stuff": f"Hello world! ({i})"}))
            if msg_received.is_set():
                break

    sub_proc = Process(target=sub)
    pub_proc = Process(target=pub)

    sub_proc.start()
    pub_proc.start()
    print("Stopping RabbitMQ")
    robotnikmq_proc.stop()
    print("RabbitMQ Stopped")
    rabbitmq_stopped.set()
    sleep(2)

    print("Starting RabbitMQ")
    robotnikmq_proc.start()
    assert msg_received.wait(timeout=10)
    pub_proc.terminate()
    sub_proc.terminate()
    pub_proc.join()
    sub_proc.join()
