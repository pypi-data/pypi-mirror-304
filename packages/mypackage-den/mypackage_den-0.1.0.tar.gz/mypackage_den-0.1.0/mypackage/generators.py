# mypackage/generators.py

def get_keys(dictionary):
    return [key for key in dictionary.keys()]

if __name__ == "__main__":
    dictionary = {'Name': 'Denis', 'Work': 'Programming', 'Age': '22'}
    keys = get_keys(dictionary)
    print("Список ключей словаря:", keys)
