from mypackage.utils import multiply
import mypackage
import inspect
import this
import os

if __name__ == "__main__":
    print("hello")
    print(multiply(2, 4))

print(mypackage)
print(inspect.getfile(this))
print(os.listdir('/anaconda3/lib/python3.7/'))