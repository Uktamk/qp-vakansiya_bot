from aiohttp.tracing import TraceRequestEndParams


async def on_request_end(session, context, params: TraceRequestEndParams):
    pass