from setuptools import setup, find_packages
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Base requirements
install_requires = [
    "google-generativeai",
]

# Add python3-tk for Linux
if sys.platform.startswith('linux'):
    install_requires.append('python3-tk')

# Windows-specific entry point
if sys.platform == 'win32':
    entry_points = {
        "console_scripts": [
            "fluxel=fluxel.interpreter:main",
            "fluxel_runner=fluxel_runner:main",
        ],
        "gui_scripts": [
            "fluxel_gui=fluxel_runner:main",
        ],
    }
else:
    entry_points = {
        "console_scripts": [
            "fluxel=fluxel.interpreter:main",
        ],
    }

setup(
    name="fluxel",
    version="0.3.0",
    author="Trey",
    author_email="allanleonardiii@gmail.com",
    description="A simple interpreter for Fluxel scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gigachadtrey/fluxel/",
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    entry_points=entry_points,
    py_modules=['fluxel_runner'],
)