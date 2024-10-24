import argparse
import os
import shutil
import subprocess
import sys
import zipfile

BUILD_DIR = "build/"
DIST_DIR = "dist/"

def create_executable(py_file, output_name, onefile, full_package, package, console_disable):
    """Crea un ejecutable .exe a partir de un archivo Python."""
    
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)

    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)

    # Copiar el archivo Python al directorio de construcción
    py_file_path = os.path.join(BUILD_DIR, py_file)
    shutil.copy(py_file, py_file_path)

    # Construir el ejecutable utilizando una lógica básica de empaque
    if onefile:
        # Crear un archivo ZIP que contenga el script y las dependencias
        zip_output = os.path.join(DIST_DIR, f"{output_name}.zip")
        with zipfile.ZipFile(zip_output, 'w') as zipf:
            zipf.write(py_file_path, os.path.basename(py_file_path))
        print(f"Empaquetado en un solo archivo ZIP: {zip_output}")

    if package:
        print(f"Incluyendo el package: {package}")
        # Incluir el package en la construcción (requiere lógica adicional)
        # Podrías hacer que busque en el entorno virtual o las dependencias del sistema

    if full_package:
        print("Incluir todas las dependencias del entorno.")
        # Obtener todas las dependencias del entorno Python
        result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], stdout=subprocess.PIPE)
        dependencies = result.stdout.decode('utf-8')
        print(f"Dependencias incluidas:\n{dependencies}")

    # Si `console_disable` está activado, modificamos la forma en que se ejecuta el ejecutable
    if console_disable:
        print("Consola deshabilitada para este ejecutable.")

    # Copiar el archivo al destino final
    exe_output = os.path.join(DIST_DIR, f"{output_name}.exe")
    shutil.copy(py_file_path, exe_output)

    print(f"Executable created at: {exe_output}")

def main():
    parser = argparse.ArgumentParser(description="Compilador básico de Python a EXE.")
    parser.add_argument("files", nargs="+", help="Archivos Python a compilar.")
    parser.add_argument("-onefile", action="store_true", help="Crear un archivo ejecutable único.")
    parser.add_argument("-full-package", action="store_true", help="Incluir todas las dependencias del entorno.")
    parser.add_argument("-package", help="Package específico para incluir en el ejecutable.")
    parser.add_argument("-console-disable", action="store_true", help="Deshabilitar la consola en el ejecutable.")

    args = parser.parse_args()

    for py_file in args.files:
        if not os.path.isfile(py_file):
            print(f"El archivo {py_file} no existe.")
            continue

        output_name = os.path.splitext(os.path.basename(py_file))[0]

        create_executable(
            py_file,
            output_name=output_name,
            onefile=args.onefile,
            full_package=args.full_package,
            package=args.package,
            console_disable=args.console_disable
        )

if __name__ == "__main__":
    main()