
def if_else(condition="True"):
    code = f"if {condition}:\n    # Write code for True condition\nelse:\n    # Write code for False condition\n    pass"
    return code

def switch_case(variable="x"):
    code = f"{variable}_switch = {{\n    'case1': lambda: print('case1'),\n    'case2': lambda: print('case2'),\n}}\n{variable}_switch.get({variable}, lambda: print('default'))()"
    return code
