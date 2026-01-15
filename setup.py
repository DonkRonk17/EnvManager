"""
Setup script for EnvManager
Cross-platform environment and service manager
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="envmanager",
    version="1.0.0",
    description="Cross-platform environment and service manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Logan Smith / Metaphy LLC",
    author_email="",
    url="https://github.com/DonkRonk17/EnvManager",
    py_modules=["envmanager"],
    python_requires=">=3.7",
    install_requires=[
        # Zero dependencies - pure Python stdlib
    ],
    entry_points={
        "console_scripts": [
            "envmanager=envmanager:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    keywords="environment variables services docker devops system-administration cross-platform",
    project_urls={
        "Bug Reports": "https://github.com/DonkRonk17/EnvManager/issues",
        "Source": "https://github.com/DonkRonk17/EnvManager",
    },
)
