# he/compiler.py

import argparse
import os
import marshal
import sys
import subprocess
import pip

# Función para compilar el código fuente a bytecode
def compile_to_bytecode(source_file):
    with open(source_file, 'r') as file:
        source_code = file.read()
    bytecode = compile(source_code, source_file, 'exec')
    return bytecode

# Función para serializar el bytecode en un archivo
def serialize_bytecode(bytecode, output_file):
    with open(output_file, 'wb') as file:
        marshal.dump(bytecode, file)

# Función para crear un ejecutable simple
def create_executable(bytecode_file, output_name, console_disable):
    with open(output_name, 'wb') as exe_file:
        # Aquí puedes agregar un encabezado o más lógica
        exe_file.write(b'#! /usr/bin/env python\n')
        if console_disable:
            exe_file.write(b'import os\n')
            exe_file.write(b'os.environ["PYTHONNOUSERSITE"] = "1"\n')
        exe_file.write(b'import marshal\n')
        exe_file.write(b'with open("bytecode.bc", "rb") as f:\n')
        exe_file.write(b'    code = marshal.load(f)\n')
        exe_file.write(b'exec(code)')

# Función para instalar paquetes
def install_package(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Función principal del compilador
def main():
    parser = argparse.ArgumentParser(description="Compile Python files into a simple executable.")
    parser.add_argument("source", help="Source code to compile")
    parser.add_argument("-onefile", action="store_true", help="Create a single-file executable")
    parser.add_argument("-full-package", action="store_true", help="Include all dependencies")
    parser.add_argument("-package", help="Specific package to include")
    parser.add_argument("-console-disable", action="store_true", help="Disable console window in the executable")

    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"File not found: {args.source}")
        return

    # Instalar paquetes si se especifica
    if args.full_package:
        requirements_file = 'requirements.txt'
        if os.path.exists(requirements_file):
            with open(requirements_file) as f:
                for line in f:
                    install_package(line.strip())
        else:
            print("requirements.txt file not found for installing packages.")

    if args.package:
        install_package(args.package)

    # Compila el código fuente
    bytecode = compile_to_bytecode(args.source)

    # Serializa el bytecode a un archivo
    bytecode_file = "bytecode.bc"
    serialize_bytecode(bytecode, bytecode_file)

    # Crea el ejecutable
    executable_name = "output.exe"
    create_executable(bytecode_file, executable_name, args.console_disable)

    print(f"Executable created at: {executable_name}")

if __name__ == "__main__":
    main()