import logging
import aiohttp

from aiohttp import web

logger = logging.getLogger("simpleproxy")


def log(r, headers):
    logger.debug("")
    logger.debug("~"*50)
    logger.debug(f"{r.method} {r.url}")
    for k,v in headers.items():
        logger.debug(f"{k}: {v}")


async def main(request):

    headers = {k:v for k,v in request.headers.items()}
    headers['SimpleProxyTest'] = "test"

    log(request, headers)

    data = None
    if request.has_body:
        data = await request.read()
        logger.debug(f"data: {data}")

    async with aiohttp.request(
        method=request.method,
        url=request.url,
        params=request.query,
        headers=headers,
        data=data
    ) as resp:
        status = resp.status
        text = await resp.text()
        return web.Response(status=status, text=text)


logging.basicConfig(level=logging.DEBUG)

app = web.Application()
app.add_routes([web.route('*', '/{path:.*}', main)])
web.run_app(app)