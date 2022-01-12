import math
import argparse

cmd_parser = argparse.ArgumentParser(description="This program is Calculate credits parameters")

cmd_parser.add_argument("--type", choices=["annuity", "diff"], help="Use annuity or diff calculate mode")
cmd_parser.add_argument("--principal", help="Enter summa credit")
cmd_parser.add_argument("--periods", help="How many periods payment")
cmd_parser.add_argument("--interest", help="How percents for credit, without '%' charter ")
cmd_parser.add_argument("--payment", help="How many payment in month")

cmd_args = cmd_parser.parse_args()


class CreditCalc:

    def __init__(self):
        self.capital = cmd_args.principal
        self.period = cmd_args.periods
        self.percent = cmd_args.interest
        self.payment = cmd_args.payment

    def calc(self):
        mode = cmd_args.type
        if mode == 'annuity':
            self.annuity()
        elif mode == 'diff':
            self.diff()
        else:
            print('Incorrect parameters.')

    # Different math mode ====================================================
    def diff(self):
        if self.capital and self.period and self.percent:
            p = int(self.capital)  # P = the loan principal;
            n = int(self.period)  # n = number of payments.
            i = float(self.percent) / 1200  # i = nominal interest rate. This is usually 1/12 of the annual
            total_pay = 0
            for m in range(1, n + 1):
                diff_pay = math.ceil(p / n + i * (p - (p * (m - 1)) / n))
                print(diff_pay)
                total_pay += math.ceil(diff_pay)
            over_pay = total_pay - p
            print(f"\nOverpayment = {over_pay}")
        else:
            print('Incorrect parameters.')

    # Math if type Annuity =========================================================
    def annuity(self):
        if cmd_args.principal and not cmd_args.payment:
            a = int(self.capital)  # P = the loan principal;
            b = int(self.period)  # n = number of payments.
            c = float(self.percent) / 1200  # i = nominal interest rate.
            ann = math.ceil(a * ((c * pow((1 + c), b)) / (pow((1 + c), b) - 1)))
            over_pay = ann * b - a
            print(f'Your monthly payment = {ann}!\nOverpayment = {over_pay}')

        elif cmd_args.payment and not cmd_args.principal:
            a = float(self.payment)
            b = int(self.period)  # n = number of payments.
            c = float(self.percent) / 1200  # i = nominal interest rate.
            credit = int(a / ((c * pow((1 + c), b)) / (pow((1 + c), b) - 1)))
            over_pay = math.ceil(b * a - credit)
            print(f'Your loan principal = {credit}!\nOverpayment = {over_pay}')

        elif cmd_args.payment and cmd_args.principal:
            a = int(self.capital)  # P = the loan principal;
            b = int(self.payment)
            c = float(self.percent) / 1200  # i = nominal interest rate.
            res = math.log(abs(b / (b - c * a)), 1 + c)
            year = int(res // 12)
            mon = math.ceil(res % 12)
            if mon == 12:
                year += 1
                mon = 0
            if mon > 1:
                print_m = f'{mon} months'
            else:
                print_m = f'{mon} month'
            if year == 1:
                print_y = f'{year} year'
            else:
                print_y = f'{year} years'
            if mon > 0 and year < 1:
                print_out = f'{print_m}'
            elif mon < 1 and year > 0:
                print_out = f'{print_y}'
            else:
                print_out = f'{print_y} and {print_m}'
            over_pay = math.ceil(res) * b - a  # Need round for correct test.
            print(f'It will take {print_out} to repay this loan!\nOverpayment = {over_pay}')
        else:
            print('Incorrect parameters.')


creditcalc = CreditCalc()
creditcalc.calc()
