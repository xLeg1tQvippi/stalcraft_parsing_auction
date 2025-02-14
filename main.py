import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Keys
import stalcraft_data_prices
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from stalcraft_items_dict import items
from stalcraft_items_dict import artefacts
from stalcraft_items_dict import rarity_list
from stalcraft_items_dict import rarity_list_coloured
import traceback
import stalcraft_data_prices
import subprocess
import instr
import pygame
import time
import importlib
import sys


class Main:
    def __init__(
        self,
        product_name: str,
        product_price: int,
        repeatingStatus: bool,
        repeatingTime: int,
        removingOneProduct: bool,
        artefactStatus: bool,
        artefactRareness: str,
        artefactTier: int | str,
        artefactRange: list[int, int] | None,
    ):
        self.show_file_product_price_list = "price_list.py"
        self.product_name: str = product_name
        self.repeatingStatus: bool = repeatingStatus
        self.repeatingTime: int = repeatingTime
        self.max_product_price: int = product_price
        self.removingOneProduct: bool = removingOneProduct
        self.artefactStatus = artefactStatus
        self.consoleCloseTime: str = "120"
        self.artefactRareness: str = artefactRareness
        self.artefactTier: int | str = artefactTier
        self.artefactRange: list[int, int] | None = artefactRange
        self.start_options()
        self.launch_website()

    def start_options(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.options.add_argument("--start-maximized")

    def clearStalcraftDataPrices(self):
        time.sleep(2)
        print("cleaning stalcraftData...")
        with open("stalcraft_data_prices.py", "w") as file:
            file.write("dataPrice = {}")
        print("success!")
        traceback.print_stack()
        importlib.reload(stalcraft_data_prices)

    def run_error_notification(self):
        pygame.mixer.init()
        pygame.mixer.music.load("error-notification.mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()

    def show_price_list(self):
        """ """
        importlib.reload(stalcraft_data_prices)
        for key, value in stalcraft_data_prices.dataPrice.items():
            if not value:
                print("nothing found...")
                return
            else:
                break
        print("running notification... - ", end="")
        pygame.mixer.init()
        pygame.mixer.music.load("notification.mp3")
        pygame.mixer.music.play()
        print(" success")
        print("trying to open cmd...")
        subprocess.Popen("cmd.exe /K start /min python price_list.py", shell=True)
        print("success!")

    def save_data(self, product_name: str, product_data_price: dict):
        print(f"function: {self.save_data.__name__}")
        stalcraft_data_prices.dataPrice[product_name] = product_data_price
        with open("stalcraft_data_prices.py", "w", encoding="utf-8") as file:
            file.write(f"dataPrice = {repr(stalcraft_data_prices.dataPrice)}")
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
            print(f"Ошибка в функции: {self.upda.__name__}:", e)
            self.run_error_notification()
        else:
            print("page succesfully updated.")
            print("returning status...")
            return True

    def chooseRarity(self):
        print("headboxContent..")
        try:
            HeadBoxContent = WebDriverWait(
                self.browser, 60, ignored_exceptions=[StaleElementReferenceException]
            ).until(
                EC.presence_of_element_located((By.CLASS_NAME, "texHeadBoxContent"))
            )
            print("headboxLeft..")
            HeadBoxLeft = WebDriverWait(HeadBoxContent, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "texHeadBoxContentLeft"))
            )
            print("dropDown..")
            dropdown_button = WebDriverWait(HeadBoxLeft, 10).until(
                EC.element_to_be_clickable((By.ID, "dropdownMenuButton1"))
            )
            print("clicking on rarity list!")
            dropdown_button.click()
            print("clicked success!")
            getRarityList = HeadBoxLeft.find_element(
                By.CSS_SELECTOR, ".dropdown-menu.dropDonwBoxFilter"
            )
            mainRarityList = getRarityList.find_element(
                By.CSS_SELECTOR, ".form-check.dropDownBoxCheckItem"
            )
        except Exception as e:
            print(f"Ошибка в функции {self.chooseRarity.__name__}:", e)
            self.run_error_notification()
            input("Enter to continue...")
        print("main rarity list found!")
        print("trying to find quality boxes...")
        rarityBoxes = mainRarityList.find_elements(By.CLASS_NAME, "qualityBox")
        print("rarity boxes were found!")
        print("trying to choose rarity...")
        for rarityBox in rarityBoxes:
            text = rarityBox.find_element(By.CLASS_NAME, "form-check-label").text
            artefactRarity = text
            if artefactRarity == self.artefactRareness:
                print("artefact rarity found!")
                print("trying to find rarity checkbox..")
                rarityCheckBox = rarityBox.find_element(
                    By.CLASS_NAME, "form-check-input"
                )
                print("checkbox found, trying to click..")
                try:
                    WebDriverWait(rarityCheckBox, 20).until(
                        EC.element_to_be_clickable((rarityCheckBox))
                    ).click()
                except Exception as e:
                    print(f"Ошибка в функции {self.chooseRarity.__name__}", e)
                else:
                    print("successfully clicked!")
                    break
        print("trying to close rarity dropdown list...")
        dropdown_button.click()
        print("success!")

    def get_main_prices(self) -> WebElement:
        return WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.ID, "content"))
        )

    def check_and_choose_rarity(self):
        if self.artefactStatus:
            print("artefactStatus:", self.artefactStatus)
            print("choosing rarity!")
            self.chooseRarity()
        else:
            print("artefactStatus:", self.artefactStatus)

    def get_item_data(self) -> WebElement:
        return WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "contentHalfBlock"))
        )

    def get_product_descriptions(self, itemData: WebElement):
        print(f"\033[31mstarting {self.get_product_descriptions.__name__}!\033[0m")
        time.sleep(2)
        DetailedLoot = WebDriverWait(itemData, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "detailsLoots"))
        )
        return DetailedLoot.find_elements(By.CLASS_NAME, "itemLoot")

    def extract_price(self, product):
        price_box = product.find_element(By.CLASS_NAME, "priceItemBox")
        item_price = price_box.find_element(By.CLASS_NAME, "itemLootByuOut").text
        text_to_buy = "Цена выкупа: "
        text_to_buy_len = len(text_to_buy)

        try:
            product_price = float(
                item_price[text_to_buy_len:-2].replace(" ", "").replace(",", ".")
            )
            return int(product_price)
        except Exception as e:
            print(f"Ошибка при извлечении цены: {e}")
            return None

    def create_stats(self, quantity, average_price=None, name=None, amount=None):
        stats = {"quantity": quantity}
        if name is not None:
            stats["name"] = name
        if average_price:
            stats["average"] = average_price
        if amount:
            stats["amount"] = amount
        return stats

    def process_product(
        self,
        product_price,
        shorted_product_quantity,
        product_full_name,
        product_price_list,
    ):
        if self.removingOneProduct:
            condition = int(shorted_product_quantity) > 1
        else:
            condition = (
                int(product_price) <= self.max_product_price
                and int(product_price) > 0
                and int(shorted_product_quantity) == 1
            )
            if condition:
                if str(product_price) in product_price_list.keys():
                    product_price_list[str(product_price)]["quantity"] = int(
                        shorted_product_quantity
                    )
                else:
                    product_price_list[str(product_price)] = self.create_stats(
                        quantity=int(shorted_product_quantity),
                        name=product_full_name if self.artefactStatus else None,
                    )

        if int(shorted_product_quantity) > 1:
            average_price = product_price // int(shorted_product_quantity)
            condition = (
                average_price <= self.max_product_price
                and int(product_price) > 0
                and int(shorted_product_quantity) > 1
            )
            if condition:
                if str(product_price) in product_price_list.keys():
                    product_price_list[str(product_price)]["amount"] += 1
                    product_price_list[str(product_price)]["quantity"] = int(
                        shorted_product_quantity
                    )
                else:
                    product_price_list[str(product_price)] = self.create_stats(
                        quantity=int(shorted_product_quantity),
                        average_price=average_price,
                        name=product_full_name if self.artefactStatus else None,
                        amount=1,
                    )

    def get_prices(self):
        try:
            self.main_prices = self.get_main_prices()
            self.check_and_choose_rarity()
            itemData = self.get_item_data()
            print("item data found")

            product_description = self.get_product_descriptions(itemData)
            print("searching products!")

            product_price_list = {}
            print("launching cycle")
            for product in product_description:
                product_quantity = product.find_element(
                    By.CLASS_NAME, "itemLootCount"
                ).text
                shorted_product_quantity = product_quantity[-1:]
                product_full_name = product.find_element(
                    By.CLASS_NAME, "itemLootName"
                ).text
                product_price = self.extract_price(product)
                print(
                    "product_price:",
                    product_price,
                    "-",
                    shorted_product_quantity,
                    end="\r",
                )
                if product_price is not None:
                    if self.artefactStatus:
                        tier = product_full_name[-2:]
                        try:
                            tier = int(tier)
                            artTier = str(tier).isdigit()
                        except:
                            artTier = False
                        else:
                            if artTier:
                                if self.artefactRange is not None:
                                    if (
                                        int(tier) >= self.artefactRange[0]
                                        and int(tier) <= self.artefactRange[1]
                                    ):
                                        self.process_product(
                                            product_price,
                                            shorted_product_quantity,
                                            product_full_name,
                                            product_price_list,
                                        )
                                else:
                                    if self.artefactTier != "":
                                        if int(self.artefactTier) == int(tier):
                                            self.process_product(
                                                product_price,
                                                shorted_product_quantity,
                                                product_full_name,
                                                product_price_list,
                                            )
                                    else:
                                        if self.artefactTier == "":
                                            self.process_product(
                                                product_price,
                                                shorted_product_quantity,
                                                product_full_name,
                                                product_price_list,
                                            )
                            else:
                                continue
                    else:
                        self.process_product(
                            product_price,
                            shorted_product_quantity,
                            product_full_name,
                            product_price_list,
                        )

            print("\nfull list!")
            print(product_price_list)
            print("product searching status: Done!")

        except Exception as e:
            print(f"Ошибка в функции: {self.get_prices.__name__}:", e)
            traceback.print_exc()
            self.run_error_notification()
            input("...")
        else:
            print("saving data")
            self.save_data(
                product_name=self.product_name, product_data_price=product_price_list
            )
            if self.repeatingStatus:
                return self.update_product_page()
            return False

    def find_and_click_product(self):
        """Находит элемент введенный в поиске и нажимает на него"""
        try:
            print("trying to find element...")
            items = WebDriverWait(self.main, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "contentItems"))
            )
            item_list = items.find_elements(By.CLASS_NAME, "contentItem")
        except Exception as e:
            print(f"Ошибка в функции {self.find_and_click_product.__name__}:", e)
            self.run_error_notification()
        else:
            print("element found!")
            print("searching items!")
            count = 0

            for item in item_list:
                count += 1
                item_text = (
                    WebDriverWait(item, 20)
                    .until(
                        EC.presence_of_element_located((By.CLASS_NAME, "nameItemText"))
                    )
                    .text
                )
                print(count, "- item:", item_text)
                product_name = item_text
                if product_name == self.product_name:
                    print("trying to click on element!")
                    item.click()
                    print("succesfully clicked!")
                    return

    def get_search_input(self):
        """Ищет поле ввода поиска товара."""
        try:
            return self.search_line.find_element(By.ID, "searchItem")
        except Exception as e:
            print(f"Ошибка в get_search_input: {e}")
            return None

    def send_search_keys(self, input_element):
        """Вводит название товара в строку поиска."""
        try:
            time.sleep(2)  # Возможно, стоит заменить явную задержку на WebDriverWait
            print("sending item in searchline...")
            input_element.send_keys(self.product_name)
            print("sent successfully!")
            return True
        except Exception as e:
            print(f"Ошибка при вводе текста: {e}")
            self.run_error_notification()
            return False

    def repeat_search(self):
        """Обрабатывает повторный поиск с ожиданием."""
        print("Initialized repeated product searching!")
        cycles = 0
        while self.repeatingStatus:
            cycles += 1
            get_prices_status = self.get_prices()
            if get_prices_status:
                print(f"showing price list... Cycle: №{cycles}")
                self.show_price_list()
                print(f"starting {self.clearStalcraftDataPrices.__name__} function!")
                self.clearStalcraftDataPrices()
                clear_line = " " * 50
                for i in range(self.repeatingTime, 0, -1):
                    print(f"\r{clear_line}", end="\r")  # Очистка строки
                    print(f"until repeat: {i} sec...", end="\r")
                    time.sleep(1)
                print()  # Перенос строки после таймера
        print(f"cycles finished, total cycles: {cycles}")

    def search_InputItem(self):
        """Находит строку поиска, вводит название товара и запускает процесс получения цен."""
        input_search = self.get_search_input()
        if not input_search:
            return  # Если поле ввода не найдено, дальше идти не имеет смысла

        if not self.send_search_keys(input_search):
            return  # Если не удалось ввести текст, выходим

        self.find_and_click_product()
        print(f"We are on: {self.browser.current_url}")
        new_pageStatus = self.browser.execute_script("return document.readyState;")
        if new_pageStatus == "complete":
            time.sleep(3)
            print("page_status:", new_pageStatus)
            print(f"launching function: {self.get_prices.__name__}!")

            if self.repeatingStatus:
                self.repeat_search()
            else:
                print("search mode: (without repeating).")
                if not self.get_prices():
                    print("showing price list...")
                    self.show_price_list()
                    print(
                        f"starting {self.clearStalcraftDataPrices.__name__} function!"
                    )
                    self.clearStalcraftDataPrices()

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
            self.run_error_notification()
        else:
            self.search_InputItem()

    def launch_website(self):
        with webdriver.Chrome(options=self.options) as browser:
            self.browser: webdriver = browser
            browser.get(url="https://stalcraft-monitor.ru/auction")
            website_loaded = browser.execute_script("return document.readyState;")
            if website_loaded == "complete":
                print("website loading: complete")
                self.search_line_arguments()


def input_int(text: str):
    while True:
        try:
            text = int(input(text))
        except:
            print("введите число")
            continue
        else:
            return text


def get_artefact_range(text: list):
    try:
        artefactRange = [int(range) for range in text]
    except Exception as e:
        print(e)
        input()
    else:
        print(
            f"\033[31m(!)\033[0m Радиус поиска: {artefactRange[0]} - {artefactRange[1]}"
        )
        return artefactRange


if __name__ == "__main__":
    while True:
        removeOneProductStatus = False
        buyingArtefact = False
        defaultItems = WordCompleter(items)
        rarityList = WordCompleter(rarity_list)
        print()
        product_name = prompt("Введите название товара: ", completer=defaultItems)
        if product_name in artefacts:
            buyingArtefact = True
            print("-" * len(rarity_list_coloured[0]))
            for i in rarity_list_coloured:
                print(i)
            print("-" * len(rarity_list_coloured[0]))
            rarity = prompt("Введите редкость товара: ", completer=rarityList)
            while True:
                artefactTier = input(
                    "Введите заточку артефакта (0-15), (0-15)-(0-15) для диапазона артефактов.\n Enter чтобы пропустить\n>>>"
                )
                try:
                    if "-" in artefactTier:
                        range = artefactTier.split("-")
                    else:
                        raise ValueError
                except:
                    pass
                else:
                    artefactRange = get_artefact_range(range)
                    break
                if artefactTier != "":
                    artefactTier = int(artefactTier)
                    if artefactTier >= 0 and artefactTier <= 15:
                        artefactRange = None
                        break
                    else:
                        continue
                else:
                    print("\033[31m(!)\033[0m Установлен поиск на все тиры артефактов")
                    artefactRange = None
                    break
        else:
            rarity = ""
            artefactTier = ""
            artefactRange = None
        max_price = input_int("Введите максимальную цену товара:\n>>>")
        repeatingStatus = input_int("Зациклить поиск товаров?\n1 - Да\n2 - Нет\n>>>")
        if repeatingStatus == 1:
            repeatingStatus = True
            repeatingTime = input_int(
                "Введите время между повторами поиска (секунды)\n>>>"
            )
        if repeatingStatus == 2:
            repeatingStatus = False
            repeatingTime = 10

        if buyingArtefact == False:
            removeOneProductItem = input_int(
                "Убрать вывод одиночных товаров?\n1 - Да\n2 - Нет\n>>>"
            )
            if removeOneProductItem == 1:
                removeOneProductStatus = True
        start = Main(
            product_name=product_name,
            product_price=max_price,
            repeatingStatus=repeatingStatus,
            repeatingTime=repeatingTime,
            removingOneProduct=removeOneProductStatus,
            artefactStatus=buyingArtefact,
            artefactRareness=rarity,
            artefactTier=artefactTier,
            artefactRange=artefactRange,
        )
