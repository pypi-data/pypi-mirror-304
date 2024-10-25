from setuptools import setup, find_packages

setup(
    name='',           # Nome da sua biblioteca
    version='0.1.0',                   # Versão da sua biblioteca
    author='Hnery Lunz',                  # Seu nome
    author_email='brainprogramacoes@gmail.com',  # Seu e-mail
    description='Biblioteca Em construção para diversas coisas como: uso melhor de variaveis, funçoes e outras coisas...',  # Descrição curta
    long_description=open('README.md').read(),  # Descrição longa (geralmente lida do README)
    long_description_content_type='text/markdown',  # Tipo do conteúdo (Markdown)
    url='https://github.com/usuario/minha_biblioteca',  # URL do repositório
    packages=find_packages(),           # Encontra automaticamente os pacotes
    install_requires=[                  # Dependências da sua biblioteca
        'numpy',                        # Exemplo de dependência
    ],
    classifiers=[                       # Classificadores (opcional)
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',           # Versão mínima do Python
)