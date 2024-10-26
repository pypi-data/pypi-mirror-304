import os
import sys

def create_reg_file():
    reg_file_path = os.path.join(os.path.dirname(__file__), 'bythonj_file_association.reg')
    
    with open(reg_file_path, 'w') as reg_file:
        reg_file.write('Windows Registry Editor Version 5.00\n\n')
        reg_file.write('[HKEY_CLASSES_ROOT\\.by]\n')
        reg_file.write('\"\"=\"BythonJ File\"\n\n')
        reg_file.write('[HKEY_CLASSES_ROOT\\BythonJ File\\shell\\open\\command]\n')
        command = f'\"{sys.executable}\" \"{os.path.join(os.path.dirname(__file__), "BythonJ.py")}\" \"%1\"\n'
        reg_file.write(f'\"\"=\"{command}\"')

    return reg_file_path

def main():
    reg_file = create_reg_file()
    print(f"Registry file created: {reg_file}")
    print("To apply the registry settings, please run the .reg file as an administrator.")

if __name__ == '__main__':
    main()
