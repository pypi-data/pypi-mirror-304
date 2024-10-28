import numpy as np

def print_gen():
    print("generator from module")
    print(np.random.rand(10))

if __name__ == "__main__":
    print_gen()