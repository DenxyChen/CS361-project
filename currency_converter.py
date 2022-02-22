# Course: CS361 - Software Engineering 1
# Student Name: Hongliu Han
# Assignment: Microservice
# Description: This service converts two currencies. It takes an text
#              file named input.txt as input. In input.txt file, users enter
#              the original currency, target currency and amount to convert,
#              example: USD CNY 15. The program will create a file called
#              "output.txt" and write the result in this file.

import time
import os

# cwd = os.getcwd()
# files = os.listdir(cwd)
# print("Files in %r: %s" % (cwd, files))
from forex_python.converter import CurrencyRates


def main():
    while True:
        # Reads input.txt file.
        file1 = open("input.txt", "r")
        content = file1.read()

        # List for parsing user's input
        input_list = []
        input_count = 0

        # Split user's input and store the value in the list
        for value in content.split():
            input_list.append(value)
            input_count += 1

        c = CurrencyRates()

        # Get the original currency, target currency and amount
        original_currency = input_list[0].upper()
        target_currency = input_list[1].upper()
        amount = int(input_list[2])

        # Get the result
        result = c.convert(original_currency, target_currency, amount)

        # Write the result to output.txt
        file2 = open("output.txt", "w")
        file2.write(str(result))

        # Close files
        file1.close()
        file2.close()

if __name__ == "__main__":
    main()