from aiohttp.tracing import TraceRequestStartParams



async def on_request_start(session, context, params: TraceRequestStartParams):
    params.headers["Authorization"] = "Token 123123123"
