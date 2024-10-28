from setuptools import setup 

setup(
        name = 'DadosHelpers',
        version = '1.0.1',
        author = 'Eriton Gomes De Souza',
        author_email = 'eriton.gomes.souza@gmail.com',
        packages = ['DadosHelpers'],
        description = 'Funções denomidas Helpers',
        license = 'MIT',
        install_requires = [
        "requests>=2.25.1",
        "pytz>=2024.1",
        "pandas>=2.2.2"
    ],
        python_requires = '>=3.6'
    )