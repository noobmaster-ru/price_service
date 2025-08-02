import aiohttp
import math
import asyncio

from parse_module.parse_card import ParseCard

class ParsePrice(ParseCard):
    def __init__(self):
        self.HEADERS_PARSE_PAGE_TEMPLATE = {
            "accept": "*/*",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTM0NTM3NjIsInVzZXIiOiI1NDU3MDMyNiIsInNoYXJkX2tleSI6IjEzIiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiM2Y0MmQ1YTY5MDJiNDhlNjgyYjQwYmE0NDNkOTMwMmMiLCJ2YWxpZGF0aW9uX2tleSI6IjQzZTQxMWM1ZDExODBjZWMzMzFhZGU3Y2ZiNmM1ODM2NzFkYTE0Nzg3ZGYyNWVmNjk3ZjQ0MzU0ODgwOTFlMDEiLCJwaG9uZSI6ImlGenNjbHNSSW5IYWJtSEhuM2JoVGc9PSIsInVzZXJfcmVnaXN0cmF0aW9uX2R0IjoxNjc1MjA3MjY5LCJ2ZXJzaW9uIjoyfQ.Rgsc1kGVk3bDbHZEvt37fIZI2kI2iINfo9KvR7wupxojoqQ507HqKhrEcyIynDAVJ4ivXh66m_cbiH1Li8vXI3DGFEskzAgKLvoPxyRKxbvEqqi3D_6jQUmW2o-Hy4DCm3Ij56guZhVskj0-DL7VM-nx6hOpXWgnp13571FtT0kkG5bG-rYco7_CgmK9w0PPp-ElRLd7xjue3wE8y9XA7Rk-MS4U4ZqlW6H8odC_82Woa3fjEJOYeLlVLBNzH_6JIO4LENeEtNtmyfdv_HTDCfw7X7pHuj-OMIzPnjq5NDCh5vcqqyH4sR7qKTrahFjXm47hC3kLUXPUPUqy4vY7jA",
            "origin": "https://www.wildberries.ru",
            "priority": "u=1, i",
            # required:  'referer': f'https://www.wildberries.ru/catalog/0/search.aspx?page={page_number}&sort=popular&search=%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BA%D0%B0+%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B0%D1%8F',
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
            "x-queryid": "qid127909588174272377820250725142812",
            "x-userid": "54570326",
        }

    # надо переписать будет - иногда может некорректно работать из-за размера/цвета: неизвестно какой у артикула будет
    async def parse_card(
        self, session: aiohttp.ClientSession, nm_id: str, list_of_nm_ids: list
    ) -> int | str:
        try:
            nm = "".join([f"{item};" for item in list_of_nm_ids])
            params = {
                "appType": "1",
                "curr": "rub",
                "dest": "-446115",
                "spp": "30",
                "hide_dtype": "14",
                "ab_testing": "false",
                "lang": "ru",
                "nm": nm,
            }
            async with session.get(
                "https://card.wb.ru/cards/v4/detail", params=params
            ) as resp:
                data = await resp.json()
                products = data["products"]
                for product in products:
                    if int(product["id"]) == int(nm_id):
                        sizes = product["sizes"]
                        for size in sizes:
                            if "price" in size:
                                return size["price"]["product"]
                return "Error in parse_card"
                # return data["products"][0]["sizes"][0]["price"]["product"]
        except Exception:
            return "Нет в наличии"

    async def parse_grade(
        self, session: aiohttp.ClientSession, nm_id: str
    ) -> int | str:
        try:
            params = {"curr": "RUB"}
            headers = self.HEADERS_PARSE_PAGE_TEMPLATE.copy()
            del headers["x-queryid"]
            del headers["x-userid"]
            headers["referer"] = (
                f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx?targetUrl=SP"
            )

            async with session.get(
                "https://user-grade.wildberries.ru/api/v5/grade",
                params=params,
                headers=headers,
            ) as resp:
                data = await resp.json()
                return data["payload"]["payments"][0]["full_discount"]
        except Exception:
            return "Нет в наличии"

    
    async def parse_price(
        self, session: aiohttp.ClientSession, nm_id: int, articles_prices: dict
    ) -> None:
        try:
            list_of_nm_ids = await self.parse_colors(session, nm_id)
            full_discount = await self.parse_grade(session, nm_id)
            price = await self.parse_card(session, nm_id, list_of_nm_ids)
            if isinstance(full_discount, int) and isinstance(price, int):
                wb_wallet_price = math.floor((price / 100) * (1 - full_discount / 100))
                articles_prices[nm_id] = {"wb_wallet_price": wb_wallet_price}
            else:
                articles_prices[nm_id] = {"wb_wallet_price": "Нет в наличии"}
        except Exception as e:
            print("Error in parse_price")