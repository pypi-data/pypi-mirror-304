from setuptools import setup, find_packages

setup(
    name='lumtina',
    version='0.2.3',
    packages=find_packages(),
    description='Lumtina is a Python package for various utilities.',
    long_description=open('README.md').read(),  # Aggiungi questa riga per la descrizione lunga
    long_description_content_type='text/markdown',  # Specifica il tipo di contenuto
    author='Simo',
    author_email='cardellasimone10@gmail.com',
    url='https://github.com/sonosimooo/Lumtina',  # Modifica con il tuo URL GitHub
    install_requires=[
        'colorama'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
