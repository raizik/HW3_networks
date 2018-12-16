import numpy as np


def main():
    number = np.random.choice([0, 1], 1, False, [0.1, 0.9])
    print("number: ")
    print(number)


if __name__ == '__main__':
    main()
