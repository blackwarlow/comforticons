"""Interactive usage example"""
from . import Identicon


def main():
    print(Identicon().generate(input(">>> ")))


if __name__ == "__main__":
    main()
