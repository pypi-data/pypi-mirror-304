import os
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install


class CustomInstallCommand(install):
    """Custom handler for the 'install' command to create the hyperlisa directory, copy the config file, and modify .gitignore."""

    def run(self):
        # Run the standard installation first
        install.run(self)

        # Define source and destination for the config file
        source = os.path.join(os.path.dirname(__file__), "lisa", "config.yaml")
        destination_dir = os.path.join(os.getcwd(), "hyperlisa")
        destination = os.path.join(destination_dir, "config.yaml")

        # Create the destination directory if it doesn't exist
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Copy the configuration file
        shutil.copy(source, destination)
        print(f"Configuration file has been copied to {destination}")

        # Path to .gitignore file in the current working directory
        gitignore_path = os.path.join(os.getcwd(), ".gitignore")

        # Check if .gitignore exists, and if so, add 'hyperlisa' if not already present
        if os.path.isfile(gitignore_path):
            with open(gitignore_path, "r") as gitignore_file:
                lines = gitignore_file.readlines()

            # Check if 'hyperlisa' is already in .gitignore
            if "hyperlisa\n" not in lines and "hyperlisa" not in [
                line.strip() for line in lines
            ]:
                with open(gitignore_path, "a") as gitignore_file:
                    gitignore_file.write("\nhyperlisa\n")
                print("Added 'hyperlisa' to .gitignore")


setup(
    name="hyperlisa",
    version="1.0.1",
    description="A package for combining source code files into one",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Omar Venturi",
    author_email="omar.venturi@hypertrue.com",
    url="https://github.com/moonClimber/hyperlisa",  # URL del repository GitHub
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "combine-code=lisa._combine_code:main",  # Comando originale
            "cmb=lisa._combine_code:main",  # Alias breve
            "lisacmb=lisa._combine_code:main",  # Alias descrittivo
            "hyperlisacmb=lisa._combine_code:main",  # Alias ancora più descrittivo
        ],
    },
    cmdclass={
        "install": CustomInstallCommand,
    },
)
