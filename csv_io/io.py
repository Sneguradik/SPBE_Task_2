from typing import Sequence

import aiofiles
from aiocsv import AsyncDictReader

async def read_tickers_from_csv(path,csv_sep = ',') -> Sequence[str]:
    result = []

    async with aiofiles.open(path, 'r', newline='') as file:
        async for line in AsyncDictReader(file, delimiter=csv_sep):
            result.append(line['Tickers'])

    return result