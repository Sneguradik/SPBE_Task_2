from typing import Sequence, Any

import aiohttp
from bs4 import BeautifulSoup

def parse_float_from_string(s):
    numeric_chars = "0123456789.-"
    filtered = ''.join(c for c in s if c in numeric_chars)
    try:
        return float(filtered)
    except ValueError:
        raise ValueError("No valid float could be parsed.")

async def parse_page(ticker:str, session: aiohttp.ClientSession) -> dict[str, Any]:
    response = await session.get(f'https://finance.yahoo.com/quote/{ticker}/')
    raw_data = await response.text()
    obj = {"ticker" : ticker}

    parser = BeautifulSoup(raw_data, features="html.parser")
    res = parser.find_all("li", class_="yf-11uk5vd")

    for el in res:
        children = el.findChildren(recursive=False)

        match children[0].text.strip():
            case 'Previous Close':
                obj["previousClose"] = float(children[1].text)
            case 'Open':
                obj["open"] = float(children[1].text)
            case 'Bid':
                bid_components = children[1].text.split(' ')
                obj["bid"] = float(bid_components[0])
            case 'Ask':
                ask_components = children[1].text.split(' ')
                obj["ask"] = float(ask_components[0])
            case 'Volume':
                obj["volume"] = int(children[1].text.replace(',', ''))
            case "Day's Range":
                day_components = children[1].text.split(' ')
                obj["dayLow"] = float(day_components[0])
                obj["dayHigh"] = float(day_components[2])
            case 'Market Cap (intraday)':
                cap_index = 0
                if "K" in children[1].text: cap_index = 3
                elif "M" in children[1].text: cap_index = 6
                elif "B" in children[1].text: cap_index = 9
                elif "T" in children[1].text: cap_index = 12
                obj["marketCap"] = parse_float_from_string(children[1].text)  * 10**cap_index
            case _:
                pass
    res2 = parser.find_all("li", class_="yf-i6syij")


    for el in res2:
        children = el.findChildren(recursive=False)

        match children[0].text.strip():
            case 'Enterprise Value':
                cap_index = 0
                if "K" in children[1].text:
                    cap_index = 3
                elif "M" in children[1].text:
                    cap_index = 6
                elif "B" in children[1].text:
                    cap_index = 9
                elif "T" in children[1].text:
                    cap_index = 12
                obj["enterpriseValue"] = parse_float_from_string(children[1].text) * 10**cap_index
            case 'Trailing P/E':
                obj["trailingPE"] = float(children[1].text)
            case 'Forward P/E':
                obj["forwardPE"] = float(children[1].text)
            case 'PEG Ratio (5yr expected)':
                obj["pegRatio"] = float(children[1].text)
            case 'Price/Sales (ttm)':
                obj["priceToSalesTTM"] = float(children[1].text)
            case 'Price/Book (mrq)':
                obj["priceToBook"] = float(children[1].text)
            case 'Enterprise Value/Revenue':
                obj["enterpriseToRevenue"] = float(children[1].text)
            case 'Enterprise Value/EBITDA':
                obj["enterpriseToEbitda"] = float(children[1].text)
            case _:
                pass

    return obj