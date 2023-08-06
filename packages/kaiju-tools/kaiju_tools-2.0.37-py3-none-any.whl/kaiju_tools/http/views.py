from typing import cast

from aiohttp.web import Request, Response, View, json_response, WebSocketResponse, WSMsgType
from aiohttp.http_websocket import WSMessage
from aiohttp_cors import CorsViewMixin

from kaiju_tools.http.middlewares import handle_exception
from kaiju_tools.serialization import dumps, loads
from kaiju_tools.services import Scope, Session
from kaiju_tools.rpc.services import JSONRPCServer
from kaiju_tools.rpc.etc import JSONRPCHeaders

__all__ = ['JSONRPCView', 'jsonrpc_websocket_handler']


async def jsonrpc_websocket_handler(request: Request):
    """Read from websocket."""
    ws = WebSocketResponse()
    counter = 0
    rpc: JSONRPCServer = request.app.services.rpc  # noqa
    session: Session = request.get('session', None)
    scope: Scope = session.scope if session else Scope.GUEST
    headers = dict(request.headers)

    async def _send_response(_session: Session, headers: dict, result):
        nonlocal session, scope, request
        session = request['session'] = _session
        scope = session.scope
        await ws.send_json(result.repr(), dumps=dumps)

    await ws.prepare(request)

    async for msg in ws:
        msg = cast(WSMessage, msg)
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                data = loads(msg.data)
                counter += 1
                if 'id' not in data:
                    data['id'] = counter
                await rpc.call(
                    data, headers=headers, session=session, scope=scope, nowait=True, callback=_send_response
                )
        elif msg.type == WSMsgType.ERROR:
            request.app.logger.error('Websocket error: %s', ws.exception())

    if session:
        ws._headers[JSONRPCHeaders.SESSION_ID_HEADER] = session.id  # noqa

    return ws


class JSONRPCView(CorsViewMixin, View):
    """JSON RPC server endpoint."""

    route = '/public/rpc'

    async def post(self):
        """Make an RPC request."""
        if not self.request.can_read_body:
            return Response()
        data = await self.request.text()
        session: Session = self.request.get('session', None)
        scope: Scope = session.scope if session else Scope.GUEST
        rpc: JSONRPCServer = self.request.app.services.rpc  # noqa
        headers, data = await rpc.call(loads(data), headers=dict(self.request.headers), session=session, scope=scope)
        return json_response(data, headers=headers, dumps=dumps)
