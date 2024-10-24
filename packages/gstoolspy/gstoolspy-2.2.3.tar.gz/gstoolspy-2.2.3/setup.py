from setuptools import setup, find_packages

setup(
    name='gstoolspy',
    version='2.2.3',
    author='Hilton Queiroz Rebello',
    author_email='rebello.hiltonqueiroz@gmail.com',
    description='GsTools é uma ferramenta poderosa para disponibilizar dados de abas do Google Sheets. Com uma configuração simples e suporte a múltiplas abas, o GSTools facilita a integração de dados do Google Sheets em seus projetos Python.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hqr90/gsTools',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "gspread",
        "time",
    ],
)