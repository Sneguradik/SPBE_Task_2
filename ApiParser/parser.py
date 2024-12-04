from typing import Any
import aiohttp

async def parse_api(ticker:str,session: aiohttp.ClientSession, key:str) -> dict[str,Any]:
    response = await session.get(
        f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={key}')
    raw_data = await response.json()

    if not 'Global Quote' in raw_data.keys():
        print(raw_data)
        return dict()

    raw_data = raw_data['Global Quote']

    if len(raw_data.keys()) == 0:
        print("No data for "+ticker)
        return dict()

    response_details = await session.get(
        f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={key}')
    raw_data_details = await response_details.json()



    return {"ticker": ticker, "previousClose": float(raw_data["08. previous close"]),
           "volume": float(raw_data["06. volume"]), "open": float(raw_data["02. open"]),
           "dayHigh": float(raw_data["03. high"]), "dayLow": float(raw_data["04. low"]),
           "trailingPE": float(raw_data_details["TrailingPE"]), "forwardPE": float(raw_data_details["ForwardPE"]),
           "pegRatio": float(raw_data_details["PEGRatio"]), "priceToSalesTTM": float(raw_data_details["PriceToSalesRatioTTM"]),
           "priceToBook": float(raw_data_details["PriceToBookRatio"]), "enterpriseToRevenue": float(raw_data_details["EVToRevenue"]),
           "enterpriseToEbitda": float(raw_data_details["EVToEBITDA"])}