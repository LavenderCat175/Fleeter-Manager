import asyncio
import configparser
import logging
import engineio.exceptions
import socketio
from socketio.exceptions import BadNamespaceError
from pathlib import Path
from wincontrol import is_blocked
from client.namespace import FleetNamespace

config = configparser.ConfigParser()
config.read('res/config.ini')

reconnect_task: asyncio.Task | None = None
heartbeat_task: asyncio.Task | None = None

sio = socketio.AsyncClient()
sio.register_namespace(FleetNamespace('/fleet'))

shutdown_event = asyncio.Event()

async def start_client():
    folder_path = Path('./res/')

    with open(next(folder_path.glob('*.tkn')), 'r') as f:
        token = f.read()
        print(token)
        await start_reconnect(token)
    await shutdown_event.wait()

async def reconnection(token: str):
    logging.info("Attempting reconnection...")
    while True:
        await asyncio.sleep(config.getint("Server", "reconnection_interval"))
        try:
            await sio.connect(config["Server"]["instance"], namespaces=['/fleet'], socketio_path='socket', auth={'token': token})
            break
        except (BadNamespaceError, ConnectionError, engineio.exceptions.ConnectionError) as e:
            logging.debug(f"Connection failed: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during reconnection: {e}")

async def start_reconnect(token: str):
    global reconnect_task
    reconnect_task = asyncio.create_task(reconnection(token))