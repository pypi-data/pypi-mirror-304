def read_file(filepath="file.txt"):
    code = f"with open('{filepath}', 'r') as file:\n    data = file.read()\n    print(data)"
    return code

def write_file(filepath="file.txt", content="Hello, World!"):
    code = f"with open('{filepath}', 'w') as file:\n    file.write('{content}')"
    return code
