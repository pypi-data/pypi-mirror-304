from setuptools import setup, find_packages

setup(
    name='nome_do_pacote',  # Nome do seu pacote
    version='0.1.0',  # Versão do seu pacote
    author='Seu Nome',
    author_email='seuemail@example.com',
    description='Uma breve descrição do seu pacote',
    packages=find_packages(),  # Encontra pacotes automaticamente
    python_requires='>=3.6',
)
