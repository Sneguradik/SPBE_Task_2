# This is a sample Python script.
import asyncio
import os
from argparse import Namespace, ArgumentParser
from typing import Sequence
import aiohttp
from pandas import DataFrame
from ApiParser import parse_api
from PageParser import parse_page
from csv_io import read_tickers_from_csv
from dotenv import load_dotenv

def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", required=False, help="Path to tickers table",
        type=str, default='data/tickers.csv')
    parser.add_argument("-o", "--output", dest="output", required=False, help="Path to output folder",
        type=str, default='data/')
    return parser.parse_args()

async def api_main(tickers: Sequence[str], api_key: str) :

    async with aiohttp.ClientSession() as session:
        tasks = [parse_api( ticker, session, api_key) for ticker in tickers]
        return await asyncio.gather(*tasks)

async def page_main(tickers: Sequence[str]):
    async with aiohttp.ClientSession() as session:
        tasks = [parse_page( ticker, session) for ticker in tickers]
        return await asyncio.gather(*tasks)

async def main(args):
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        print(".env file was not found. Create .env with Alpha_Vantage_API_Key=.")

    if not os.path.exists(args.input):
        print("You haven't tickers.csv file in data folder.\nCreate it and try again.")
        return

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    if not os.path.exists(os.path.join(args.output, "stats")):
        os.makedirs("data/stats")

    tickers = await read_tickers_from_csv(args.input)
    print("Fetching data")
    page_data = await page_main(tickers)
    api_data = await api_main(tickers, os.getenv('Alpha_Vantage_API_Key'))
    print("Data fetched")
    df_page = DataFrame(page_data)
    #df_api = DataFrame(api_data)

    df_page.to_csv(os.path.join(args.output, 'stats/page_parse.csv'))
    #df_api.to_csv(os.path.join(args.output, 'stats/page_api.csv'))


if __name__ == '__main__':
    args = parse_args()
    asyncio.run(main(args))

