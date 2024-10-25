from setuptools import setup, find_packages

setup(
    name='snowconection',  # Nombre de tu paquete
    version='0.1',  # Versión inicial
    packages=find_packages(),
    description='A library with reusable functions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tu Nombre',
    author_email='carlitos8medina@gmail.com',
    url='',  # URL de tu repositorio
    license='MIT',  # Tipo de licencia
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)