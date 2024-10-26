import os
import sys
import winreg as reg

def register_file_association():
    file_extension = ".by"
    command = f'"{sys.executable}" "{os.path.join(os.getcwd(), "BythonJ", "BythonJ.py")}" "%1"'
    
    try:
        reg_key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, file_extension)
        reg.SetValue(reg_key, '', reg.REG_SZ, 'BythonJ File')
        
        command_key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, r'BythonJ File\shell\open\command')
        reg.SetValue(command_key, '', reg.REG_SZ, command)

        print(f"Successfully associated {file_extension} files with BythonJ.")
    except Exception as e:
        print(f"Failed to register file association: {e}")

if __name__ == '__main__':
    register_file_association()
