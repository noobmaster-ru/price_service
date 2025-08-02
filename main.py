import asyncio
import aiohttp
import json
import os
import shutil

from constants import ARTICLES_WB
from parse_module.parse_price_class import ParsePrice

async def main() -> None:
    parser = ParsePrice()

    tasks = []
    articles_prices = {}
    async with aiohttp.ClientSession() as session:
        for article in ARTICLES_WB:
            tasks.append(parser.parse_price(session, article, articles_prices))
        await asyncio.gather(*tasks)

    shutil.rmtree(".data")
    os.makedirs(".data",exist_ok = True)
    with open(".data/wb_wallet_prices.json", "w", encoding="utf-8") as f:
        json.dump(articles_prices, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    
    asyncio.run(main())