from constants import WB_TOKEN, URL_GOODS, URL_SALES
import requests


if __name__ == "__main__":
    headers = {
        'Authorization': WB_TOKEN
    }

    params_goods = {
        "limit": 1000 
    }
    params_sales ={
        "dateFrom": "2025-07-17",
        "flag": 1
    }
    response_goods = requests.get(
        URL_GOODS, headers=headers, params=params_goods
    )
    response_sales = requests.get(
        URL_SALES, headers=headers, params=params_sales
    )
    dict = {}
    print("begin of loading")
    data = response_sales.json()
    
    with open("prices.txt", "w", encoding="utf-8") as file:
        file.write("[nm_id, total_price, discount_percent, price with discount_percent(seller approach), price with discount_percent and payment_sale_amount and spp]\n")
        for sale in data:
            date = sale.get("date")
            nm_id = sale.get("nmId")
            total_price = sale.get("totalPrice")
            spp = sale.get("spp")
            payment_sale_amount = sale.get("paymentSaleAmount")
            finished_price = sale.get("finishedPrice")
            discount_percent = sale.get("discountPercent")
            file.write(f"{nm_id}: {total_price:.1f}, {discount_percent:.1f}, {total_price*(1 - discount_percent/100):.1f}, {total_price*(1-discount_percent/100)*(1 - payment_sale_amount/100)*(1-spp/100):.1f}, {total_price*(1-discount_percent/100)*(1 - payment_sale_amount/100)*(1-spp/100)*0.9:.1f}\n")
            
            # print("nm_id = ",nm_id)
            # print("total_price = ",total_price)
            # print("discount_percent = ", discount_percent)
            # print("price with discount_percent(seller approach) = ", total_price*(1 - discount_percent/100))
            # print("price with discount_percent and payment_sale_amount and spp = ",total_price*(1-discount_percent/100)*(1 - payment_sale_amount/100)*(1-spp/100))
            # print("my_price = ", total_price*(1-discount_percent/100)*(1 - payment_sale_amount/100)*(1-spp/100)*0.9, "\n")


    # data = response_goods.json()
    # list_goods = data.get("data", {}).get("listGoods", [])
    # with open("prices.txt", "w", encoding="utf-8") as file:
    #     for product in list_goods:
    #         nm_id = product.get("nmID")
    #         vendor_code = product.get("vendorCode")
    #         currency_iso_code_4217 = product.get("currencyIsoCode4217")
    #         discount = product.get("discount")
    #         club_discount = product.get("clubDiscount")

    #         sizes = product.get("sizes")[0]
    #         clubDiscountedPrice = sizes.get("clubDiscountedPrice")
    #         price = sizes.get("price")
    #         # print([nm_id, clubDiscountedPrice, discount, club_discount])
    #         file.write(f"{nm_id}({vendor_code}): {price}, {clubDiscountedPrice}; current = {currency_iso_code_4217}\n")