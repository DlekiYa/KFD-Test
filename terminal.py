import json
from random import random


with open('config.json') as f:
    config = json.load(f)
    pairs = config['pairs']
    values = config['default-values']
    stored = config['default-stored']


def exit_terminal(*params):
    print("Exiting terminal gracefully!")
    raise SystemExit


def help(*params):
    print("The following is the list of possible commands:")
    print("help - shows this list")
    print("exit - exits the program")
    print("convert <currency you give> <currency you need> <deposited amount> - withdraws the input amount of " +
          "currency and deposits it's equivalents into storage")
    print("rates - prints currency rates")
    print("pairs - prints supported exchange pairs")


def update_rates():
    for value in values:
        if value == "USD":
            continue
        # random() - 0.5 returns values from -0.5 to 0.5, dividing it by 10 gives the range from -5% to 5%, add 1 to
        # adjust to percentage in number form and just apply this change to value by multiplication
        values[value] *= 1 + (random() - 0.5) / 10


def convert(currency_in, currency_out, deposited):
    if deposited.find('.') > 1 or not deposited.replace(".", "").isnumeric():
        print("Please, input a number")
        return
    deposited = float(deposited)

    if f"{currency_in} / {currency_out}" not in pairs and f"{currency_out} / {currency_in}" not in pairs:
        print(f"Sorry, we don't support the [{currency_in} / {currency_out}] exchange pair")
        return

    # this formula in the next line calculates how much of the output currency we try to withdraw and if there's not
    # enough in terminal, we apologize and cancel operation
    exchange_out = values[currency_in] / values[currency_out] * deposited
    if exchange_out > stored[currency_out]:
        print(f"Sorry, there's not enough {currency_out} in the machine, please try again later")
        return

    print(f"Success! Exchanged {deposited} {currency_in} for {exchange_out} {currency_out}!")
    stored[currency_in] += deposited
    stored[currency_out] -= exchange_out

    update_rates()


def rates(*params):
    print("Currency rates in USD:")
    for value in values:
        print(f"{value}: {values[value]}$", end='')
        if values[value] < 1:
            print(f" ({1 / values[value]} {value} is 1$)", end='')
        print()

def pairs_command(*params):
    print("Exchange pairs and their rates:")
    for pair in pairs:
        currency_in, currency_out = pair.split(' / ')
        rate = values[currency_in] / values[currency_out]
        if rate > 1 / rate:
            print(f"{pair}: {rate}")
        else:
            print(f"{currency_out} / {currency_in}: {1 / rate}")


commands = dict()
commands['exit'] = exit_terminal
commands['help'] = help
commands['convert'] = convert
commands['rates'] = rates
commands['pairs'] = pairs_command


while True:
    line = input()
    command, params = '', ''
    if line.find(' ') > 0:
        command, params = line.split(maxsplit=1)
    else:
        command = line
    if command not in commands:
        print(f'Error: unknown command "{command}"')
        commands['help']()
        continue
    commands[command](*params.split())
