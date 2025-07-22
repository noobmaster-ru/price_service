from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def extract_wallet_price(url: str) -> int | None:
    # Настройка headless-режима браузера
    options = Options()
    
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    
    # options.add_argument("--disable-gpu")

    options.add_argument("--disable-infobars") 

    # Инициализация драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(5)  # время  на загрузку (можно заменить на WebDriverWait)

        # Ищем элемент с ценой WB Кошелька 
        # <span class="price-block__wallet-price red-price" data-link="{on 'click' premiumPromoPopup}class{merge: promoWalletSale &amp;&amp; promoWalletSale &gt; 0 &amp;&amp; ~wbSettings.walletTypeCode &gt; 0 &amp;&amp; enabledPremium toggle='price-block__wallet-price--pointer'}" data-jsv="#380^/380^">424&nbsp;₽</span>
        price_element = driver.find_element(By.CSS_SELECTOR, "span.price-block__wallet-price")
        wallet_price = price_element.text.replace('\xa0', '').replace('₽', '').strip()
        return wallet_price
    except Exception as e:
        print(f"Ошибка: {e}")
        return None
    finally:
        driver.quit()

if __name__ == "__main__":
    url = "https://www.wildberries.ru/catalog/418395621/detail.aspx"
    wallet_price = extract_wallet_price(url)
    print("Цена при оплате через WB Кошелёк:", wallet_price, "₽")