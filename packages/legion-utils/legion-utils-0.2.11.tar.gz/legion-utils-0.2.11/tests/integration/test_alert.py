from pprint import pprint

from legion_utils import broadcast, Priority, broadcast_info, broadcast_activity
from legion_utils import broadcast_alert, broadcast_warning, broadcast_error, broadcast_critical

from tests.integration.utils import vagrant_test, CONFIG, META_QUEUE, broadcast_receive

try:
    from pytest_cov.embed import cleanup_on_sigterm
except ImportError:
    pass
else:
    cleanup_on_sigterm()


@vagrant_test
def test_basic_broadcast_receive():
    def pub():
        broadcast(META_QUEUE, route='legion-utils-vm.test', ttl=3,
                  priority=Priority.ACTIVITY, contents={'stuff': 'Hello world!'},
                  config=CONFIG)

    def sub(msg):
        pprint(msg)

    broadcast_receive(pub, sub)


@vagrant_test
def test_broadcast_info():
    def pub():
        broadcast_info(META_QUEUE, route='legion-utils-vm.test',
                       contents={'stuff': 'Hello world!'},
                       config=CONFIG)

    def sub(msg):
        assert 'ttl' not in msg.contents
        assert msg.contents['priority'] == 0
        assert msg.routing_key == 'legion-utils-vm.test.info'

    broadcast_receive(pub, sub)


@vagrant_test
def test_broadcast_activity():
    def pub():
        broadcast_activity(META_QUEUE, route='legion-utils-vm.test',
                           contents={'stuff': 'Hello world!'},
                           config=CONFIG)

    def sub(msg):
        assert 'ttl' not in msg.contents
        assert msg.contents['priority'] == 1
        assert msg.routing_key == 'legion-utils-vm.test.activity'

    broadcast_receive(pub, sub)


@vagrant_test
def test_broadcast_alert():
    def pub():
        broadcast_alert(META_QUEUE, route='legion-utils-vm.test',
                        description='Testing stuff', alert_key='legion-utils-vm.test',
                        contents={'stuff': 'Hello world!'},
                        config=CONFIG)

    def sub(msg):
        assert msg.contents['ttl'] == 30
        assert msg.contents['priority'] == 2
        assert msg.routing_key == 'legion-utils-vm.test.warning'

    broadcast_receive(pub, sub)


@vagrant_test
def test_broadcast_warning():
    def pub():
        broadcast_warning(META_QUEUE, route='legion-utils-vm.test',
                          desc='Testing stuff', alert_key='legion-utils-vm.test',
                          contents={'stuff': 'Hello world!'},
                          config=CONFIG)

    def sub(msg):
        assert msg.contents['ttl'] == 30
        assert msg.contents['priority'] == 2
        assert msg.routing_key == 'legion-utils-vm.test.warning'

    broadcast_receive(pub, sub)


@vagrant_test
def test_broadcast_error():
    def pub():
        broadcast_error(META_QUEUE, route='legion-utils-vm.test',
                        desc='Testing stuff', alert_key='legion-utils-vm.test',
                        contents={'stuff': 'Hello world!'},
                        config=CONFIG)

    def sub(msg):
        assert msg.contents['ttl'] == 30
        assert msg.contents['priority'] == 3
        assert msg.routing_key == 'legion-utils-vm.test.error'

    broadcast_receive(pub, sub)


@vagrant_test
def test_broadcast_critical():
    def pub():
        broadcast_critical(META_QUEUE, route='legion-utils-vm.test',
                           desc='Testing stuff', alert_key='legion-utils-vm.test',
                           contents={'stuff': 'Hello world!'},
                           config=CONFIG)

    def sub(msg):
        assert msg.contents['ttl'] == 30
        assert msg.contents['priority'] == 4
        assert msg.routing_key == 'legion-utils-vm.test.critical'

    broadcast_receive(pub, sub)
