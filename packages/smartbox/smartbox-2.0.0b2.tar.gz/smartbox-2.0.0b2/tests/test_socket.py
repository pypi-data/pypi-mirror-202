from aiohttp import web
import asyncio
import logging
import pytest
import socketio

from smartbox import SocketSession

from const import MOCK_ACCESS_TOKEN, MOCK_DEV_ID

_MOCK_API_NAME = "myapi"
_MOCK_BASIC_AUTH_CREDS = "sldjfls93r2lkj"
_MOCK_USERNAME = "xxxxx"
_MOCK_PASSWORD = "yyyyy"
_MOCK_TOKEN_TYPE = "bearer"
_MOCK_ACCESS_TOKEN_2 = "j323jf3202"
_MOCK_REFRESH_TOKEN = "23ij2oij324j3423"
_MOCK_EXPIRES_IN = 14400

_LOGGER = logging.getLogger(__name__)

_TEST_DEV_DATA = {
    "connected": True,
    "nodes": [{"addr": 1, "name": "My Heater", "type": "htr"}],
}
_TEST_UPDATE_1 = {
    "path": "/htr/1/status",
    "body": {"mode": "auto", "stemp": "15.5", "mtemp": "10.7", "units": "C"},
}
_TEST_UPDATE_2 = {
    "path": "/htr/1/status",
    "body": {"mode": "auto", "stemp": "15.5", "mtemp": "11.1", "units": "C"},
}
_TEST_PING_INTERVAL = 1  # don't wait too long for pings in tests


class MockServer(object):
    class TestAPIV2Namespace(socketio.AsyncNamespace):
        def __init__(self, namespace, connect_event, ping_event):
            super().__init__(namespace)
            self._connect_event = connect_event
            self._ping_event = ping_event
            self._sent_first_update = False
            self._sent_dev_data = asyncio.Event()

        async def send_update(self):
            # send an update immediately (which should be ignored), then wait
            # for us to send dev_data and send another (which should be
            # processed)
            _LOGGER.debug("Sending update #1")
            await self.emit("update", _TEST_UPDATE_1)
            self._sent_first_update = True

            await self._sent_dev_data.wait()
            _LOGGER.debug("Sending update #2")
            await self.emit("update", _TEST_UPDATE_2)

        async def on_connect(self, sid, environ):
            _LOGGER.debug(f"{sid} connected to namespace")
            self._query_string = environ["QUERY_STRING"]

            # reset state
            self._sent_first_update = False
            self._sent_dev_data.clear()

            if self._connect_event is not None:
                self._connect_event.set()
            self._update_task = self.server.start_background_task(self.send_update)

        async def on_disconnect(self, sid):
            _LOGGER.debug(f"{sid} disconnected from namespace")
            self._update_task.cancel()

        async def on_message(self, sid, data):
            _LOGGER.debug(f"Message from {sid}: {data}")
            if data == "ping" and self._ping_event is not None:
                self._ping_event.set()

        # TODO: why no data arg?
        async def on_dev_data(self, sid):
            _LOGGER.debug("dev_data")
            # this should have been sent in response to the first update
            assert self._sent_first_update
            await self.emit("dev_data", _TEST_DEV_DATA)
            self._sent_dev_data.set()

    def __init__(self, port, connect_event=None, ping_event=None):
        self._port = port
        self._sio = socketio.AsyncServer()

        self._namespace = self.TestAPIV2Namespace(
            "/api/v2/socket_io", connect_event, ping_event
        )
        self._sio.register_namespace(self._namespace)

        self._sid = None

        @self._sio.event
        async def connect(sid, environ):
            _LOGGER.debug(f"{sid} connected")
            assert self._sid is None  # only one client
            self._sid = sid

        @self._sio.event
        async def disconnect(sid):
            _LOGGER.debug(f"{sid} disconnected")
            self._sid = None

    async def initialise(self):
        self._app = web.Application()
        self._sio.attach(self._app)
        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        _LOGGER.info(f"Starting mock server on port {self._port}")
        self._site = web.TCPSite(self._runner, "localhost", self._port)
        await self._site.start()

    async def cleanup(self):
        _LOGGER.info("Cleaning up server")
        await self._runner.cleanup()

        # engineio leaves a service task around
        _LOGGER.info("Cancelling remaining tasks")
        for task in asyncio.all_tasks():
            if task != asyncio.current_task():
                task.cancel()

    @property
    def site(self):
        return self._site

    @property
    def query_string(self):
        return self._namespace._query_string

    async def disconnect_client(self):
        _LOGGER.debug("Disconnecting client {self._sid}")
        assert self._sid is not None
        await self._sio.disconnect(self._sid)


@pytest.mark.asyncio
async def test_basic(mock_session, unused_tcp_port):
    got_dev_data = asyncio.Event()
    got_update = asyncio.Event()

    dev_data = None

    def dev_data_cb(data):
        _LOGGER.debug(f"Received dev_data callback {data}")
        nonlocal dev_data
        dev_data = data
        got_dev_data.set()

    update_data = None

    def update_cb(data):
        _LOGGER.debug(f"Received update callback {data}")
        nonlocal update_data
        update_data = data
        got_update.set()

    test_received_ping = asyncio.Event()

    mock_server = MockServer(unused_tcp_port, ping_event=test_received_ping)
    await mock_server.initialise()

    mock_session._api_host = f"http://localhost:{unused_tcp_port}"
    socket_session = SocketSession(
        mock_session,
        MOCK_DEV_ID,
        dev_data_cb,
        update_cb,
        add_sigint_handler=True,
        ping_interval=_TEST_PING_INTERVAL,
    )
    client_task = asyncio.create_task(socket_session.run())

    await got_dev_data.wait()
    assert dev_data == _TEST_DEV_DATA

    # check we connected with the right query string
    assert f"token={MOCK_ACCESS_TOKEN}" in mock_server.query_string.split("&")
    assert f"dev_id={MOCK_DEV_ID}" in mock_server.query_string.split("&")

    await got_update.wait()
    assert update_data == _TEST_UPDATE_2
    await test_received_ping.wait()

    _LOGGER.info("Stopping client")
    await socket_session.cancel()
    await client_task

    await mock_server.cleanup()


@pytest.mark.asyncio
async def test_reconnect(mock_session, unused_tcp_port):
    got_update = asyncio.Event()

    def dev_data_cb(data):
        _LOGGER.debug(f"Received dev_data callback {data}")

    def update_cb(data):
        _LOGGER.debug(f"Received update callback {data}")
        got_update.set()

    test_connected = asyncio.Event()

    mock_server = MockServer(unused_tcp_port, connect_event=test_connected)
    await mock_server.initialise()

    mock_session._api_host = f"http://localhost:{unused_tcp_port}"
    socket_session = SocketSession(
        mock_session,
        MOCK_DEV_ID,
        dev_data_cb,
        update_cb,
        add_sigint_handler=True,
        ping_interval=_TEST_PING_INTERVAL,
    )
    client_task = asyncio.create_task(socket_session.run())

    await test_connected.wait()
    test_connected.clear()

    # check we connected with the right access_token
    assert f"token={MOCK_ACCESS_TOKEN}" in mock_server.query_string.split("&")

    await got_update.wait()
    got_update.clear()

    # force a reconnect
    _LOGGER.debug("Forcing reconnect")
    await mock_server.disconnect_client()
    _LOGGER.debug("Stopping site")
    await mock_server.site.stop()

    # change the access token
    mock_session._access_token = _MOCK_ACCESS_TOKEN_2

    _LOGGER.debug("Restarting site")
    await mock_server.site.start()

    # should now reconnect
    await test_connected.wait()

    # check we connected with the new access_token
    assert f"token={_MOCK_ACCESS_TOKEN_2}" in mock_server.query_string.split("&")

    # should get another update
    await got_update.wait()

    _LOGGER.info("Stopping client")
    await socket_session.cancel()
    await client_task

    await mock_server.cleanup()

    # engineio leaves a service task around
    _LOGGER.info("Cancelling remaining tasks")
    for task in asyncio.all_tasks():
        if task != asyncio.current_task():
            _LOGGER.info(f"Task: {task}")
            _LOGGER.info(task.cancel())


@pytest.mark.asyncio
async def test_connect_retry_success(mock_session, mocker):
    mock_async_client = mocker.MagicMock()
    exception_attempts = 2

    async def connect_side_effect(*args, **kwargs):
        nonlocal exception_attempts
        if exception_attempts > 0:
            exception_attempts -= 1
            raise socketio.exceptions.ConnectionError("Test connection error")

    class TestFinishedException(Exception):
        pass

    async def disconnect_side_effect(*args, **kwargs):
        raise TestFinishedException()

    mock_async_client.connect = mocker.AsyncMock(side_effect=connect_side_effect)
    mock_async_client.wait = mocker.AsyncMock()
    mock_async_client.disconnect = mocker.AsyncMock(side_effect=disconnect_side_effect)
    mocker.patch("socketio.AsyncClient", return_value=mock_async_client)
    socket_session = SocketSession(
        mock_session,
        MOCK_DEV_ID,
        add_sigint_handler=True,
    )

    with pytest.raises(TestFinishedException):
        client_task = asyncio.create_task(socket_session.run())
        await client_task

    mock_async_client.connect.assert_awaited()
    mock_async_client.disconnect.assert_awaited()
    mock_async_client.wait.assert_awaited()


@pytest.mark.asyncio
async def test_connect_retry_failure(mock_session, mocker):
    mock_async_client = mocker.MagicMock()

    # always fails
    async def connect_side_effect(*args, **kwargs):
        raise socketio.exceptions.ConnectionError("Test connection error")

    class TestFinishedException(Exception):
        pass

    def check_refresh_side_effect(*args, **kwargs):
        raise TestFinishedException()

    mock_session._check_refresh = mocker.MagicMock(
        side_effect=check_refresh_side_effect
    )
    mock_async_client.connect = mocker.AsyncMock(side_effect=connect_side_effect)
    mock_async_client.disconnect = mocker.AsyncMock()
    mock_async_client.wait = mocker.AsyncMock()
    mocker.patch("socketio.AsyncClient", return_value=mock_async_client)
    socket_session = SocketSession(
        mock_session,
        MOCK_DEV_ID,
        add_sigint_handler=True,
    )

    with pytest.raises(TestFinishedException):
        client_task = asyncio.create_task(socket_session.run())
        await client_task

    mock_async_client.connect.assert_awaited()
    mock_async_client.disconnect.assert_not_awaited()
    mock_async_client.wait.assert_not_awaited()
