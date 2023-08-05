from setuptools import setup

setup(
    name='encpp',
    version='1.0.0',    
    description='Encryption Plus Plus (encpp)',
    long_description='Encryption Plus Plus (encpp) is a Python library for encryption and decryption of data. It uses AES and RSA for encryption and decryption. Supports Strings as AES password.',
    url='https://github.com/tchello45/encpp',
    author='Tilman Kurmayer',
    author_email='tilman.kurmayer@outlook.de',
    license='MIT',
    packages=['encpp'],
    python_requires='>=3.0',
    install_requires=['pycryptodome',
                      'pycryptodomex', 
                      'rsa'                
                      ],
    
)