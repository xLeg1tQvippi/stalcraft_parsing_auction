import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Keys
from stalcraft_data_prices import dataPrice
import time, pyperclip


class Main:
    def __init__(self):
        self.product_name = "Пси-маячок"
        self.repeatingStatus = True
        self.repeatingTime = 15
        self.max_product_price = 22000
        self.launch_website()

    def save_data(self, product_name: str, product_data_price: list):
        dataPrice[product_name] = sorted(product_data_price)
        with open("stalcraft_data_prices.py", "w", encoding="utf-8") as file:
            file.write(f"dataPrice = {repr(dataPrice)}")
        print("Успешно сохранено!")

    def update_product_page(self):
        try:
            print("trying to update...")
            HeadBoxContent = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "texHeadBoxContent"))
            )
            HeadBoxLeft = HeadBoxContent.find_element(
                By.CLASS_NAME, "texHeadBoxContentLeft"
            )
            button = HeadBoxLeft.find_element(
                By.XPATH, '//button[contains(text(), "Обновить")]'
            )
            button.click()
        except Exception as e:
            print(f"Ошибка в функции: {self.get_prices.__name__}:", e)
        else:
            print("page succesfully updated.")
            print("returning status...")
            return True

    def get_prices(self):
        try:
            self.main_prices: WebElement = self.browser.find_element(By.ID, "content")
            itemData: WebElement = WebDriverWait(self.browser, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "contentHalfBlock"))
            )
            print("item data found")
            DetailedLoot: WebElement = itemData.find_element(
                By.CLASS_NAME, "detailsLoots"
            )
            print("detailed loot found")
            time.sleep(4)
            product_description = DetailedLoot.find_elements(By.CLASS_NAME, "itemLoot")
            print("searching products!")
            text_to_buy = "Цена выкупа: "
            text_to_buy_len = len(text_to_buy)
            product_price_list = []
            for product in product_description:
                price_box = product.find_element(By.CLASS_NAME, "priceItemBox")
                item_price = price_box.find_element(
                    By.CLASS_NAME, "itemLootByuOut"
                ).text
                product_price_full = str(item_price)
                try:
                    product_price = float(
                        product_price_full[text_to_buy_len:-2]
                        .replace(" ", "")
                        .replace(",", ".")
                    )
                    print("trying to int!:", int(product_price))
                    product_price = int(product_price)
                    if (
                        int(product_price) < self.max_product_price
                        and int(product_price) > 0
                    ):
                        product_price_list.append(float(product_price))
                except:
                    print("int not success!")
            print("full list!")
            print(sorted(product_price_list))
        except Exception as e:
            print(f"Ошибка в функции: {self.get_prices.__name__}:", e)
        else:
            print("saving data")
            self.save_data(
                product_name=self.product_name, product_data_price=product_price_list
            )
            if self.repeatingStatus == True:
                pageStatusUpdate = self.update_product_page()
                if pageStatusUpdate == True:
                    return True
                else:
                    return False

    def find_and_click_product(self):
        try:
            print("trying to find element...")
            items = self.main.find_element(By.CLASS_NAME, "contentItems")
            time.sleep(3)
            item_list = items.find_elements(By.CLASS_NAME, "contentItem")
        except Exception as e:
            print(f"Ошибка в функции {self.find_and_click_product.__name__}:", e)
        else:
            print("element found!")
            print("searching items!")
            time.sleep(1)
            count = 0
            for item in item_list:
                count += 1
                item_text = item.find_element(By.CLASS_NAME, "nameItemText").text
                print(count, "- item:", item_text)
                product_name = item_text
                if product_name == self.product_name:
                    print("trying to click on element!")
                    item.click()
                    print("succesfully clicked!")
                    return

    def search_InputItem(self):
        try:
            inputSearch = self.search_line.find_element(By.ID, "searchItem")
        except Exception as e:
            print(f"Ошибка в функции {self.search_InputItem.__name__}:", e)
        else:
            print("trying to send keys...")
            try:
                inputSearch.send_keys(
                    self.product_name
                )  #! Добавить отправку элемента по поиску.
            except Exception as e:
                print(e)
            else:
                # TODO main branch!
                print("keys was succesfully sent!")
                self.find_and_click_product()
                print(f"we are on '{self.browser.current_url}'!")
                print(f"running: {self.get_prices.__name__}!")
                print(f"repeatingStatus:", self.repeatingStatus)
                cycles = 0
                if self.repeatingStatus == True:
                    while self.repeatingStatus == True:
                        cycles += 1
                        get_prices_status = self.get_prices()
                        if get_prices_status == True:
                            time.sleep(self.repeatingTime)
                            print("cycles:", cycles)
                        if get_prices_status == False:
                            break
                else:
                    self.get_prices()

    def search_line_arguments(self):
        try:
            self.main: WebElement = WebDriverWait(self.browser, 20).until(
                EC.presence_of_element_located((By.ID, "content"))
            )
            if self.main:
                print("main found!")
            self.search_line: WebElement = WebDriverWait(self.browser, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "contentsearch"))
            )
        except Exception as e:
            print("Ошибка в функции search_arguments:", e)
        else:
            self.search_InputItem()

    def launch_website(self):
        with webdriver.Chrome() as browser:
            self.browser: webdriver = browser
            browser.get(url="https://stalcraft-monitor.ru/auction")
            website_loaded = browser.execute_script("return document.readyState;")
            if website_loaded == "complete":
                print("website loading: complete")
                self.search_line_arguments()


if __name__ == "__main__":
    Main()
