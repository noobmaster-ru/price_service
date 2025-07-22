from constants import WB_TOKEN, URL_GOODS, URL_SALES
import requests


if __name__ == "__main__":
    headers = {"Authorization": WB_TOKEN}

    params_goods = {"limit": 1000}
    params_sales = {"dateFrom": "2025-07-17", "flag": 1}
    response_goods = requests.get(URL_GOODS, headers=headers, params=params_goods)
    response_sales = requests.get(URL_SALES, headers=headers, params=params_sales)
    dict = {}
    print("begin of loading")
    data = response_sales.json()

    with open("prices.txt", "w", encoding="utf-8") as file:
        file.write(
            "[nm_id, total_price, discount_percent, price with discount_percent(seller approach), price with discount_percent and payment_sale_amount and spp]\n"
        )
        for sale in data:
            date = sale.get("date")
            nm_id = sale.get("nmId")
            total_price = sale.get("totalPrice")
            spp = sale.get("spp")
            payment_sale_amount = sale.get("paymentSaleAmount")
            finished_price = sale.get("finishedPrice")
            discount_percent = sale.get("discountPercent")
            file.write(
                f"{nm_id}: {total_price:.1f}, {discount_percent:.1f}, {total_price * (1 - discount_percent / 100):.1f}, {total_price * (1 - discount_percent / 100) * (1 - payment_sale_amount / 100) * (1 - spp / 100):.1f}, {total_price * (1 - discount_percent / 100) * (1 - payment_sale_amount / 100) * (1 - spp / 100) * 0.98:.1f}\n"
            )
