import asyncio
import time
import aiohttp
from aiohttp.client import ClientSession
import json
from influxdb import InfluxDBClient
from datetime import datetime
from dotenv import load_dotenv

chains = {
    "umee": "https://api.umee.huginn.tech/umee/oracle/v1/validators",
    "kujira" : "https://lcd.kaiyo.kujira.setten.io/oracle/validators"
    }


load_dotenv()

INFLUXDBNAME=os.getenv("INFLUXDB")
INFLUXDB_USERNAME=os.getenv("INFLUXDB_USERNAME")
INFLUXDB_PASSWORD=os.getenv("INFLUXDB_PASSWoRD")

def dbrecord(chain, moniker, addr, missing):
    datestr = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    json_body = [
        {
            "measurement": "miss",
            "tags": {
                "address": addr,
                "chain" : chain,
                "moniker" : moniker
            },
            "time": datestr,
            "fields": {
                "missing": missing
            }
        }
    ]

    return json_body
    
dbclient = InfluxDBClient(host='127.0.0.1',
                          port=8086,
                          username=INFLUXDB_USERNAME,
                          password=INFLUXDB_PASSWORD)
dbclient.switch_database(INFLUXDBNAME)


async def download_link(chain:str, url:str, 
                        addr:str, moniker:str, 
                        session:ClientSession):
    
    full_url = f"{url}/{addr}/miss"
    async with session.get(full_url) as response:
        result = await response.text()
        r = json.loads(result)
        missing = int(r["miss_counter"])
        dbclient.write_points(dbrecord(chain, moniker, addr, missing))

async def download_all(urls:list):
    my_conn = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=my_conn) as session:
        tasks = []
        for chainname, url, addr, moniker in urls:
            task = asyncio.ensure_future(
                download_link(chain=chainname, url=url, 
                addr=addr, moniker=moniker, session=session))
            tasks.append(task)
        await asyncio.gather(*tasks,return_exceptions=True) # the await must be nest inside of the session                                                                                                                                                                                                                   

temp = []

for chainname, url in chains.items():
    lines = open(f"/home/kujiracheck/cosmos/chain_{chainname}.txt").readlines()
    for line in lines:
    
        addr, moniker = line.strip().split("|||")
        temp.append((chainname, url, addr, moniker))

asyncio.run(download_all(temp))
