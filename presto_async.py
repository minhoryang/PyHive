import asyncio

import os
import sys

sys.path.insert(0, os.path.curdir)

from aiohttp_requests import requests
from pyhive import presto


async def main(query):
    cursor = presto.connect('localhost', requests_session=requests).cursor()
    await cursor.execute(query)
    print(await cursor.fetchone())
    print([i async for i in cursor.async_fetchall()])


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*[
    main('select count(*), count(distinct ss_sold_date_sk) as d from alluxio.store_sales'),
    main('select count(*), count(distinct cs_bill_customer_sk) as e from alluxio.catalog_sales'),
]))
# https://www.alluxio.io/alluxio-presto-sandbox-docker/
