import asyncio
import json
import websockets
import hashlib

class SimpleSocket:
    def __init__(self, init):
        self.id = init['project_id']
        self.token = init['project_token']
        self.socket_url = "wss://simplesocket.net/socket/v2"
        self.supports_etf = True
        self.operations = {}
        self.total_messages = 0
        self.remotes = {}
        self.client_id = None
        self.server_id = None
        self.secure_id = None
        self.expect_close = False
        self.default_config = None
        self.disconnect_event = None
        self.show_debug = True
        self.debug_style = True

        asyncio.run(self.connect_socket())

    def debug(self, message, force=False, error=False):
        if self.show_debug or force:
            if self.debug_style:
                if error:
                    print(f"\033[91mSimpleSocket\033[0m {message}")  # Red for errors
                else:
                    print(f"\033[94mSimpleSocket\033[0m {message}")  # Blue for normal messages
            else:
                if error:
                    print(f"Error: {message}")
                else:
                    print(message)

    async def send(self, oper, data, callback=None, use_id=None):
        if use_id is None:
            self.total_messages += 1
            mess_id = int(f"{oper}{self.total_messages}")
        else:
            mess_id = use_id

        send_data = [mess_id] + data

        if oper > 1:
            store_op = [oper, data, callback]
            if oper == 2:
                store_op.append(self.hash(data[0]))
            self.operations[mess_id] = store_op

        if self.socket and self.socket.open and (self.client_id or oper == 1):
            send_str = json.dumps(send_data)[1:-1]  # Remove the outer brackets
            self.debug(f"SENT: {send_str}")

            if self.supports_etf:
                send_str = send_str.encode('utf-8')

            await self.socket.send(send_str)

            if callback is None and mess_id in self.operations and oper < 7:
                del self.operations[mess_id]

        return mess_id

    async def handle_message(self, rec_data):
        if isinstance(rec_data, bytes):
            rec_data = rec_data.decode('utf-8')

        self.debug(f"RECEIVED: {rec_data}")

        data = json.loads(f"[{rec_data}]")

        if data[0] == 2:  # SUBSCRIBE
            if data[4] is None:
                for key in list(self.operations.keys()):
                    oper = self.operations[key]
                    if oper and oper[3] == data[1]:
                        if oper[2]:
                            oper[2](data[2], data[3])
            elif data[4] in self.remotes:
                self.remotes[data[4]](data[2], data[3])
        elif data[0] == 3:  # RESPONSE
            if data[1] in self.operations:
                self.operations[data[1]][2](data[2])
        elif data[0] == 1:  # CONNECT
            self.debug(f"CONNECTED: ClientID: {data[1]}")
            self.client_id = data[1]
            self.server_id = data[2]
            self.secure_id = f"{data[1]}-{data[3]}"
            if hasattr(self, 'onopen'):
                self.onopen()

            # Reconnect Previous Events
            for key in list(self.operations.keys()):
                operation = self.operations[key]
                del self.operations[key]
                await self.send(operation[0], operation[1], operation[2], int(key))
        elif data[0] == 0:  # ERROR
            self.debug(data[2], True, True)
            if data[1] in self.operations:
                del self.operations[data[1]]
            if data[3]:
                self.expect_close = True
            elif data[3] in self.operations:
                self.operations[data[3]][3] = self.hash(data[4])
                self.operations[data[3]][1][0] = data[4]

    async def connect_socket(self):
        while True:
            self.debug("CONNECTING")
            ending = "?en=etf" if self.supports_etf else ""
            self.socket = await websockets.connect(f"{self.socket_url}{ending}")

            try:
                while True:
                    message = await self.socket.recv()
                    await self.handle_message(message)
            except websockets.ConnectionClosed:
                self.closed()
                if not self.expect_close:
                    await asyncio.sleep(10)
            finally:
                await self.socket.close()

    def closed(self):
        self.debug("CONNECTION LOST")
        self.client_id = None
        self.server_id = None
        self.secure_id = None
        if hasattr(self, 'onclose'):
            self.onclose()

    def hash(self, text):
        if isinstance(text, dict):
            text = json.dumps(text)
        hash_object = hashlib.sha256(text.encode('utf-8'))
        return int(hash_object.hexdigest(), 16)

    async def set_default_config(self, new_set):
        self.debug(f"NEW CONFIG: Config: {json.dumps(new_set)}")
        if self.default_config and self.default_config in self.operations:
            del self.operations[self.default_config]
        self.default_config = await self.send(7, [new_set])

    async def set_disconnect_event(self, filter, data, config=None):
        self.debug(f"Setting Disconnect Event: Filter: {json.dumps(filter)} | Data: {json.dumps(data)} | Config: {json.dumps(config)}")
        send_data = [filter, data]
        if config:
            send_data.append(config)
        if self.disconnect_event and self.disconnect_event in self.operations:
            del self.operations[self.disconnect_event]
            self.disconnect_event = None
        if filter:
            self.disconnect_event = await self.send(8, send_data)
        else:
            await self.send(8, [None])

    async def subscribe(self, filter, callback, config=None):
        self.debug(f"SUBSCRIBING: Filter: {json.dumps(filter)}")
        send_data = [filter]
        if config:
            send_data.append(config)
        if len(callback.__code__.co_varnames) < 2:
            if config is None:
                send_data.append(True)
            else:
                send_data.append(True)
        sub_id = await self.send(2, send_data, callback)
        return {
            'id': sub_id,
            'edit': lambda new_filter: self.edit_subscription(sub_id, new_filter),
            'close': lambda: self.close_subscription(sub_id)
        }

    async def edit_subscription(self, sub_id, new_filter):
        if sub_id in self.operations:
            new_hash = self.hash(new_filter)
            if self.operations[sub_id][3] != new_hash:
                self.debug(f"EDITING: Filter: {json.dumps(new_filter)}")
                self.operations[sub_id][1][0] = new_filter
                await self.send(4, [sub_id, self.operations[sub_id][3], new_filter])
                self.operations[sub_id][3] = new_hash

    async def close_subscription(self, sub_id):
        if sub_id in self.operations:
            self.debug(f"CLOSING {sub_id}")
            await self.send(5, [self.operations[sub_id][3]])
            del self.operations[sub_id]

    async def publish(self, filter, data, config=None):
        self.debug(f"PUBLISHING: Filter: {json.dumps(filter)} | Data: {json.dumps(data)}")
        send_data = [filter, data]
        if config:
            send_data.append(config)
        await self.send(3, send_data)

    async def remote(self, secure_id):
        split_id = secure_id.split('-')
        self.debug(f"REMOTING: ClientID: {split_id[0]}")
        return {
            'client_id': split_id[0],
            'secure_id': split_id[1],
            'subscribe': lambda func_name, filter, config=None: self.remote_subscribe(secure_id, func_name, filter, config),
            'close_subscribe': lambda func_name: self.remote_close_subscribe(secure_id, func_name),
            'valid': lambda: self.remote_valid(secure_id)
        }

    async def remote_subscribe(self, secure_id, func_name, filter, config=None):
        self.debug(f"REMOTLY SUBSCRIBING: Name: {func_name}")
        send_data = [secure_id, 2, func_name, filter]
        if config:
            send_data.append(config)
        await self.send(6, send_data)

    async def remote_close_subscribe(self, secure_id, func_name):
        self.debug(f"REMOTLY UNSUBSCRIBING: Name: {func_name}")
        await self.send(6, [secure_id, 5, func_name])

    async def remote_valid(self, secure_id):
        self.debug(f"REMOTLY VALIDATING SecureID: {secure_id}")
        return await self.send(9, [0, secure_id])

asyncio.run(main())