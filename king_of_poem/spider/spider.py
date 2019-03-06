import asyncio

import aiohttp
import async_timeout
import glom
import motor

from mongo import do_insert

base_url = "https://api.bilibili.com/x/v2/reply?pn={pn}&type=1&oid=19390801"
sem = asyncio.Semaphore(10)


async def fetch(url):
    async with sem:
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                async with session.get(url) as res:
                    data = await res.json()
                    print(data)
                    await asyncio.sleep(2)
                    await do_insert(glom.glom(data, "data.replies"))


def main():
    loop = asyncio.get_event_loop()
    tasks = [fetch(base_url.format(pn=i)) for i in range(1, 1001)]
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == "__main__":
    main()
