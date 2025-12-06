from httpx_ws import connect_ws


class WebsocketCaller:
    _host: str

    def __init__(self, host: str):
        self._host = host

    def iterate_on_generator_events(self, receive_type="json", timeout=None):
        with connect_ws(self._host + "/events/generators") as ws:
            try:
                while True:
                    if receive_type == "json":
                        event = ws.receive_json(timeout)
                        yield event
                    if receive_type == "text":
                        event = ws.receive_text(timeout)
                        yield event
                    if receive_type == "bytes":
                        event = ws.receive_bytes(timeout)
                        yield event
            except Exception:
                raise
            finally:
                ws.close()
