"""Perform fixed-rate mortgage calculations."""

from argparse import ArgumentParser
import math
import sys

def get_min_payment(principal,annual_interest_rate,term=30,payments_per_year=12):
    P = principal
    r = annual_interest_rate / payments_per_year
    n = term * payments_per_year
    A = (P * r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return math.ceil(A)


def interest_due(balance,annual_interest_rate,payments_per_year=12):
    b = balance
    r = annual_interest_rate / payments_per_year
    i = b * r
    return i


def remaining_payments(balance,annual_interest_rate,payment,payments_per_year=12):
    counter = 0
    while balance > 0:
        i = interest_due(balance,annual_interest_rate, payments_per_year)
        diff = payment - i
        counter += 1
        balance -= diff
    return counter


def main(principal,annual_interest_rate,term=30,payments_per_year=12,user_target=None):
    min_payment = get_min_payment(principal,annual_interest_rate,term,payments_per_year)
    print("The minimum payment is " + str(min_payment))
    if user_target == None:
        user_target = min_payment
    elif user_target < min_payment:
        print("Your target payment is less than the minimum payment for this mortgage.")
    else:
        required_payments = remaining_payments(principal,annual_interest_rate,min_payment,payments_per_year)
        print("If you make payments of ${}, you will pay off the mortgage in {} payments.".format(min_payment,required_payments))


from argparse import ArgumentParser
import math
import sys


def parse_args(arglist):
    # set up argument parser
    parser = ArgumentParser()
    parser.add_argument("mortgage_amount", type=float,
                        help="the total amount of the mortgage")
    parser.add_argument("annual_interest_rate", type=float,
                        help="the annual interest rate, as a float"
                             " between 0 and 1")
    parser.add_argument("-y", "--years", type=int, default=30,
                        help="the term of the mortgage in years (default: 30)")
    parser.add_argument("-n", "--num_annual_payments", type=int, default=12,
                        help="the number of payments per year (default: 12)")
    parser.add_argument("-p", "--target_payment", type=float,
                        help="the amount you want to pay per payment"
                        " (default: the minimum payment)")
    # parse and validate arguments
    args = parser.parse_args()
    if args.mortgage_amount < 0:
        raise ValueError("mortgage amount must be positive")
    if not 0 <= args.annual_interest_rate <= 1:
        raise ValueError("annual interest rate must be between 0 and 1")
    if args.years < 1:
        raise ValueError("years must be positive")
    if args.num_annual_payments < 0:
        raise ValueError("number of payments per year must be positive")
    if args.target_payment and args.target_payment < 0:
        raise ValueError("target payment must be positive")

    return args


if __name__ == "__main__":
    try:
        args = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    print("args", args)
    main(args.mortgage_amount, args.annual_interest_rate, args.years,
         args.num_annual_payments, args.target_payment)