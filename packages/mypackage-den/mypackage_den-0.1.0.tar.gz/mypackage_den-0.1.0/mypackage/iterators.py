# mypackage/iterators.py

def stroki(n, text="Hello World!"):
    for _ in range(n):
        yield text

if __name__ == "__main__":
    n = 5
    print("Генератор строк:")
    for j in stroki(n):
        print(j)
