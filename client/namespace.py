import configparser
import socketio
import wincontrol
import asyncio
from wincontrol import is_blocked

config = configparser.ConfigParser()
config.read('res/config.ini')

class FleetNamespace(socketio.AsyncClientNamespace):
    heartbeat_task: asyncio.Task | None = None

    connected = asyncio.Event()

    async def on_connect(self):
        print("connect")

        if self.heartbeat_task is None:
            self.start_heartbeat()

        print("connected")

        self.connected.set()

    async def on_disconnect(self):
        self.connected.clear()

    async def on_control(self, data):
        if "blocked" in data.keys():
            wincontrol.disable() if data.get("blocked") else wincontrol.enable()

    def start_heartbeat(self):
        async def heartbeat():
            while True:
                await self.connected.wait()
                await self.emit("heartbeat", data={"blocked": is_blocked()})
                print("hello")
                await asyncio.sleep(config.getint("Server", "heartbeat_interval"))

        self.heartbeat_task = asyncio.create_task(heartbeat())