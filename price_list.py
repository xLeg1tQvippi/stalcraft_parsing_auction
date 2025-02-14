from stalcraft_data_prices import dataPrice
from main import Main
import time, os, sys

if __name__ == "__main__":
    print("price-list!\n")

    sorted_data = {
        category: {
            str(price): value
            for price, value in sorted(items.items(), key=lambda x: int(x[0]))
        }
        for category, items in dataPrice.items()
    }

    for category, values in sorted_data.items():
        print(category)

        for price, value in values.items():
            price_int = int(price)
            price_formatted = f"{price_int:,}р.".replace(",", " ")

            if "name" in value and isinstance(value["name"], str):
                art_status = value["name"][-2:].isdigit()
            else:
                art_status = False

            if "average" in value and "amount" in value:
                print(
                    f"\n{price_formatted}\n"
                    f"Кол-во: x{value['quantity']}\n"
                    f"Цена за шт: {value['average']:,}р.\n"
                    f"Кол-во лотов: x{value['amount']}"
                )
            else:
                print(f"{price_formatted} - {value['quantity']}шт.", end="")
                print(f" | {value['name']}" if art_status else "")

input("Enter to continue...")
