import pyperclip

def copy_to_clipboard(file_name):
    with open(file_name, 'r') as file:
        data = file.read()
        pyperclip.copy(data)

def anshu():
    file_name = input("Enter file name (a/aa): ")
    if file_name == "a":
        copy_to_clipboard("./a.txt")
    if file_name == "ao":
        copy_to_clipboard("./ao.txt")

