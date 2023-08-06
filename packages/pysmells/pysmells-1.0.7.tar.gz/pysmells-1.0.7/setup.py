from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pysmells",
    version="1.0.7",
    author="Marcos Paulo Alves de Sousa and Marco Aurélio Proença Neto",
    author_email="msousa@museu-goeldi.br",
    description="Pysmells is a tool that identifies when something doesn't 'smell right' in a python code, checking for programming errors, inconsistencies and programming style violations. Pysmells is based on the following Python Enhancement Proposals (PEPs): PEP 8, PEP 257 and PEP 20.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pysmells/pysmells",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.7',
    install_requires=[
        'tabulate',
        'mypy',
        'pylint',
    ],
    entry_points={
        'console_scripts': [
            'pysmells=pysmells:main',
        ],
    },
)

