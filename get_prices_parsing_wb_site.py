import time
from typing import Optional
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from constants import ARTICLES_WB


def extract_wallet_price(url: str, driver) -> Optional[int]:
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        price_element = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.price-block__wallet-price")
            )
        )
        wallet_price = price_element.text.replace("\xa0", "").replace("₽", "").strip()
        print("✅ OK")
        return str(wallet_price)
    except Exception:
        print(f"❌ Error with parsing {url}")
        return None


def main():
    # Настройка Chrome
    options = Options()
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    results = []

    for article_id in ARTICLES_WB:
        url = f"https://www.wildberries.ru/catalog/{article_id}/detail.aspx"
        price = extract_wallet_price(url, driver)
        results.append({"article_id": article_id, "wallet_price": price})
        time.sleep(1)  # защита от бана

    driver.quit()

    # Преобразуем список в словарь с article_id в качестве ключей
    data_to_save = {item["article_id"]: item["wallet_price"] for item in results}

    # Сохраняем в JSON-файл
    with open("wb_wallet_prices.json", "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

    # # Сохраняем в CSV
    # with open("wallet_prices.csv", "w", newline='', encoding="utf-8") as f:
    #     writer = csv.DictWriter(f, fieldnames=["article_id", "wallet_price"])
    #     writer.writeheader()
    #     writer.writerows(results)

    print("✅ Saved to wallet_prices.csv")


if __name__ == "__main__":
    main()
