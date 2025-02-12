from stalcraft_data_prices import dataPrice
import time

if __name__ == "__main__":
    print("price-list!\n")
    for key, values in dataPrice.items():
        print(key)
        for key, value in values.items():
            if type(value) == int:
                print(f"{int(key):,}р. - {value} шт.")
            if type(value) == dict:
                print(
                    f"\n{int(key):,}р.\nКол-во за шт: х{value['amount']}\nЦена за шт: {value["average"]:,}р.\nКол-во лотов: x{value['quantity']}"
                )
stopInstr = False
stop = input("input 'stop' to stop operations.\npress Enter to continue...\n>>>")
if stop == "stop":
    stopInstr = True
    print("stopping iterations..")
with open("instr.py", "w") as file:
    file.write(f"repeatingStatusArg = {stopInstr}")
time.sleep(1)
