# pylint: disable=redefined-outer-name
from functools import partial
import json
from multiprocessing import Process, Event
from pprint import pprint
from time import sleep

from pytest import raises
from typeguard import typechecked

from robotnikmq.config import server_config, RobotnikConfig
from robotnikmq.core import Message
from robotnikmq.error import UnableToConnect
from robotnikmq.log import log
from robotnikmq.subscriber import Subscriber
from robotnikmq.topic import Topic

from tests.integration.utils import META_QUEUE
from tests.integration.utils import (
    conn_config,
    robotnikmq_config,
)  # pylint: disable=W0611


try:
    from pytest_cov.embed import cleanup_on_sigterm  # type: ignore
except ImportError:
    pass
else:
    cleanup_on_sigterm()


def test_basic_broadcast(robotnikmq_config):
    medium = Topic(
        META_QUEUE,
        robotnikmq_config,
        on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
    )
    medium.broadcast(Message({"stuff": "Hello world!"}))


def test_unable_to_connect():
    config = RobotnikConfig(
        connection=conn_config(1, 1, 2),
        tiers=[
            [
                server_config("127.0.0.1", 1, "", "", ""),
                server_config("127.0.0.2", 1, "1", "1", "1"),
            ]
        ],
    )
    with raises(UnableToConnect):
        medium = Topic(
            META_QUEUE,
            config,
            on_conn_error=lambda a: print(f"Could not connect (callback): {a.args}"),
        )
        medium.broadcast(Message({"stuff": "Hello world!"}))


def test_unable_to_connect_without_callback():
    config = RobotnikConfig(
        connection=conn_config(1, 1, 2),
        tiers=[
            [
                server_config("127.0.0.1", 1, "", "", ""),
                server_config("127.0.0.2", 1, "1", "1", "1"),
            ]
        ],
    )
    with raises(UnableToConnect) as exc:
        medium = Topic(META_QUEUE, config)
        medium.broadcast(Message({"stuff": "Hello world!"}))
    log.debug(str(exc))
    log.debug(str(exc.value.__str__()))


def test_basic_broadcast_receive(robotnikmq_config):
    msg_received = Event()

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
        sleep(0.2)
        medium.broadcast(Message({"stuff": "Hello world!"}))

    sub_proc = Process(target=sub)
    sub_proc.start()
    pub_proc = Process(target=pub)
    pub_proc.start()
    assert msg_received.wait(timeout=5)
    pub_proc.terminate()
    sub_proc.terminate()
    pub_proc.join()
    sub_proc.join()


def test_broadcast_malformed_message(robotnikmq_config):
    msg_received = Event()

    def callback(msg: Message) -> None:
        pprint(msg.to_dict())
        msg_received.set()

    def sub():
        Subscriber(
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        ).bind(exchange=META_QUEUE).run(callback)

    def pub():
        medium = Topic(
            exchange=META_QUEUE,
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.channel.basic_publish(
            exchange=META_QUEUE,
            routing_key="",
            body=json.dumps({"stuff": "Hello world!"}),
        )

    sub_proc = Process(target=sub)
    sub_proc.start()
    pub_proc = Process(target=pub)
    pub_proc.start()
    assert not msg_received.wait(timeout=1)
    pub_proc.terminate()
    sub_proc.terminate()
    pub_proc.join()
    sub_proc.join()


def test_subscriber_stop(robotnikmq_config):
    first_msg_received = Event()
    second_msg_received = Event()

    @typechecked
    def callback(sub: Subscriber, msg: Message) -> None:
        pprint(msg.to_dict())
        if not first_msg_received.is_set():
            first_msg_received.set()
        else:
            second_msg_received.set()
        sub.stop()

    def sub():
        sub = Subscriber(
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sub.bind(exchange=META_QUEUE).run(
            partial(callback, sub), inactivity_timeout=0.1
        )

    def pub():
        medium = Topic(
            exchange=META_QUEUE,
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(Message({"stuff": "first message"}))
        sleep(0.2)
        medium.broadcast(
            Message({"stuff": "second message"})
        )  # this message should not be received

    sub_proc = Process(target=sub)
    sub_proc.start()
    pub_proc = Process(target=pub)
    pub_proc.start()
    assert first_msg_received.wait(timeout=1)
    assert not second_msg_received.wait(timeout=1)
    pub_proc.terminate()  # note that the subscriber should NOT need to be terminated after stop was called
    pub_proc.join()
    sub_proc.join()


def test_basic_broadcast_consume(robotnikmq_config):
    def pub():
        medium = Topic(
            exchange=META_QUEUE,
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(Message({"stuff": "Hello world!"}))

    pub_proc = Process(target=pub)
    pub_proc.start()
    stream = (
        Subscriber(config=robotnikmq_config)
        .bind(exchange=META_QUEUE)
        .consume(inactivity_timeout=0.1)
    )
    for msg in stream:
        if msg is not None:
            assert msg["stuff"] == "Hello world!"
            log.debug("Break")
            break
    pub_proc.terminate()
    pub_proc.join()


def test_consume_malformed_message(robotnikmq_config):
    def pub():
        medium = Topic(
            exchange=META_QUEUE,
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.channel.basic_publish(
            exchange=META_QUEUE, routing_key="", body=json.dumps({"stuff": "MALFORMED"})
        )
        medium.broadcast(Message({"stuff": "Hello world!"}))

    pub_proc = Process(target=pub)
    pub_proc.start()
    for msg in (
        Subscriber(config=robotnikmq_config)
        .bind(exchange=META_QUEUE)
        .consume(inactivity_timeout=0.1)
    ):
        if msg is not None:
            assert msg["stuff"] == "Hello world!"
            break
    pub_proc.terminate()
    pub_proc.join()


def test_multiple_broadcast_single_receive(robotnikmq_config):
    msg_received = Event()

    def callback(msg: Message) -> None:
        pprint(msg.to_dict())
        assert msg.contents["stuff"] != "Bad"
        assert (
            msg.routing_key == "stuff.something" or msg.routing_key == "stuff.nothing"
        )
        msg_received.set()

    def sub():
        Subscriber(
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        ).bind(exchange="stuff", binding_key="stuff.*").run(callback)

    def pub1():
        medium = Topic(
            exchange="stuff",
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(
            Message({"stuff": "Hello world! (1)"}), routing_key="stuff.something"
        )

    def pub2():
        medium = Topic(
            exchange="stuff.something",
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(
            Message({"stuff": "Hello world! (2)"}), routing_key="stuff.nothing"
        )

    def pub3():
        medium = Topic(
            exchange="stuff.something",
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(Message({"stuff": "Bad"}), routing_key="bad.stuff.nothing")

    sub_proc = Process(target=sub)
    sub_proc.start()
    pub_proc1 = Process(target=pub1)
    pub_proc1.start()
    pub_proc2 = Process(target=pub2)
    pub_proc2.start()
    pub_proc3 = Process(target=pub3)
    pub_proc3.start()
    assert msg_received.wait(timeout=5)
    pub_proc1.terminate()
    pub_proc2.terminate()
    pub_proc3.terminate()
    sub_proc.terminate()
    pub_proc1.join()
    pub_proc2.join()
    pub_proc3.join()
    sub_proc.join()


def test_multiple_route_receive(robotnikmq_config):
    msg1_received = Event()
    msg2_received = Event()
    msg3_received = Event()

    def callback(msg: Message) -> None:
        pprint(msg.to_dict())
        assert msg.contents["stuff"] != "Bad"
        if msg.route == "message.1":
            msg1_received.set()
        if msg.route == "message.2":
            msg2_received.set()
        if msg.route == "message.3":
            msg3_received.set()

    def sub():
        Subscriber(
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        ).bind("stuff", "message.1").bind("stuff", "message.2").bind(
            "stuff", "message.3"
        ).run(
            callback
        )

    def pub1():
        medium = Topic(
            exchange="stuff",
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(
            Message({"stuff": "Hello world! (1)"}), routing_key="message.1"
        )

    def pub2():
        medium = Topic(
            exchange="stuff",
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(
            Message({"stuff": "Hello world! (2)"}), routing_key="message.2"
        )

    def pub3():
        medium = Topic(
            exchange="stuff",
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(
            Message({"stuff": "Hello world! (3)"}), routing_key="message.3"
        )

    def pub_bad():
        medium = Topic(
            exchange="stuff.something",
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(Message({"stuff": "Bad"}), routing_key="bad.stuff.nothing")

    sub_proc = Process(target=sub)
    sub_proc.start()
    pub_proc1 = Process(target=pub1)
    pub_proc1.start()
    pub_proc2 = Process(target=pub2)
    pub_proc2.start()
    pub_proc3 = Process(target=pub3)
    pub_proc3.start()
    pub_proc_bad = Process(target=pub_bad)
    pub_proc_bad.start()
    assert msg1_received.wait(timeout=5)
    assert msg2_received.wait(timeout=5)
    assert msg3_received.wait(timeout=5)
    pub_proc1.terminate()
    pub_proc2.terminate()
    pub_proc3.terminate()
    pub_proc_bad.terminate()
    sub_proc.terminate()
    pub_proc1.join()
    pub_proc2.join()
    pub_proc3.join()
    pub_proc_bad.join()
    sub_proc.join()


def test_multiple_queue_receive(robotnikmq_config):
    msg1_received = Event()
    msg2_received = Event()
    msg3_received = Event()

    def callback(msg: Message) -> None:
        pprint(msg.to_dict())
        assert msg.contents["stuff"] != "Bad"
        if msg.route == "message.1":
            msg1_received.set()
        if msg.route == "message.2":
            msg2_received.set()
        if msg.route == "message.3":
            msg3_received.set()

    def sub():
        Subscriber(
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        ).bind("stuff.1", "message.1").bind("stuff.2", "message.2").bind(
            "stuff.3", "message.3"
        ).run(
            callback
        )

    def pub1():
        medium = Topic(
            exchange="stuff.1",
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(
            Message({"stuff": "Hello world! (1)"}), routing_key="message.1"
        )

    def pub2():
        medium = Topic(
            exchange="stuff.2",
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(
            Message({"stuff": "Hello world! (2)"}), routing_key="message.2"
        )

    def pub3():
        medium = Topic(
            exchange="stuff.3",
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(
            Message({"stuff": "Hello world! (3)"}), routing_key="message.3"
        )

    def pub_bad():
        medium = Topic(
            exchange="stuff.1",
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(Message({"stuff": "Bad"}), routing_key="bad.stuff.nothing")

    sub_proc = Process(target=sub)
    sub_proc.start()
    pub_proc1 = Process(target=pub1)
    pub_proc1.start()
    pub_proc2 = Process(target=pub2)
    pub_proc2.start()
    pub_proc3 = Process(target=pub3)
    pub_proc3.start()
    pub_proc_bad = Process(target=pub_bad)
    pub_proc_bad.start()
    assert msg1_received.wait(timeout=5)
    assert msg2_received.wait(timeout=5)
    assert msg3_received.wait(timeout=5)
    pub_proc1.terminate()
    pub_proc2.terminate()
    pub_proc3.terminate()
    pub_proc_bad.terminate()
    sub_proc.terminate()
    pub_proc1.join()
    pub_proc2.join()
    pub_proc3.join()
    pub_proc_bad.join()
    sub_proc.join()


def test_multiple_broadcast_single_receive_msg_routing(robotnikmq_config):
    msg_received = Event()

    def callback(msg: Message) -> None:
        pprint(msg.to_dict())
        assert msg.contents["stuff"] != "Bad"
        assert (
            msg.routing_key == "stuff.something" or msg.routing_key == "stuff.nothing"
        )
        msg_received.set()

    def sub():
        Subscriber(
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        ).bind(exchange="stuff", binding_key="stuff.*").run(callback)

    def pub1():
        medium = Topic(
            exchange="stuff",
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(
            Message({"stuff": "Hello world! (1)"}, routing_key="stuff.something")
        )

    def pub2():
        medium = Topic(
            exchange="stuff.something",
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(
            Message({"stuff": "Hello world! (2)"}, routing_key="stuff.nothing")
        )

    def pub3():
        medium = Topic(
            exchange="stuff.something",
            config=robotnikmq_config,
            on_conn_error=lambda a: print(f"Could not connect: {a.args}"),
        )
        sleep(0.2)
        medium.broadcast(Message({"stuff": "Bad"}, routing_key="bad.stuff.nothing"))

    sub_proc = Process(target=sub)
    sub_proc.start()
    pub_proc1 = Process(target=pub1)
    pub_proc1.start()
    pub_proc2 = Process(target=pub2)
    pub_proc2.start()
    pub_proc3 = Process(target=pub3)
    pub_proc3.start()
    assert msg_received.wait(timeout=5)
    pub_proc1.terminate()
    pub_proc2.terminate()
    pub_proc3.terminate()
    sub_proc.terminate()
    pub_proc1.join()
    pub_proc2.join()
    pub_proc3.join()
    sub_proc.join()
