from setuptools import setup, find_packages

setup(
    name="base-decryptor",
    version="1.0.0",
    description="A CLI tool to decode base-encoded strings.",
    author="Aaryan Golatkar",
    author_email="your-email@example.com",
    url="https://github.com/your-username/base-decryptor",  # Update with your actual GitHub repo URL
    packages=find_packages(),  # Automatically find and include all packages
    include_package_data=True,  # Include other files specified in MANIFEST.in
    install_requires=[
        "base36==0.1.1",
        "base4096==1.0",
        "base45==0.4.4",
        "base58==2.1.1",
        "base91==1.0.1",
        "click==8.1.7",
        "colorama==0.4.6",
        "pybase62==1.0.0",
        "pycryptodome==3.20.0",
        "pyfiglet==1.0.2",
        "requests==2.32.3",
        "rich==13.9.3",
        "tabulate==0.9.0",
        "yaspin==3.1.0"
    ],
    entry_points={
        "console_scripts": [
            "base-decryptor=main:input_handler",  # Update if the function name or module name changes
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
