from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="loxprox",
    version='0.1.1',
    description='Control Philips Hue lights from Loxone Miniserver',
    author='Kevin Bortis',
    url="https://github.com/kwinsch/loxprox",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'loxprox=loxprox.main:main',
            ],
        },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
)