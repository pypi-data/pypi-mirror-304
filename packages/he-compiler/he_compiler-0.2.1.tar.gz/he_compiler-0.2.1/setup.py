from setuptools import setup, find_packages

setup(
    name='he-compiler',  # Nombre del paquete
    version="0.2.1",  # Versión del paquete
    author='Adrián',  # Autor del paquete
    author_email='adrianez2008@gmail.com',  # Correo electrónico
    description='A simple Python to EXE compiler',
    long_description=open('README.md').read(),  # Descripción detallada
    long_description_content_type='text/markdown',
    url='https://github.com/adrianez28/he-compiler.git',  # URL del repositorio
    packages=find_packages(),  # Encuentra automáticamente los paquetes
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versión mínima de Python requerida
    install_requires=[
        # Puedes agregar aquí las dependencias necesarias, si las hay
    ],
    entry_points={
        'console_scripts': [
            'he=he.compiler:main',  # Comando para ejecutar el compilador
        ],
    },
)