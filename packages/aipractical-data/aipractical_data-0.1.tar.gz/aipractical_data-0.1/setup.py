from setuptools import setup, find_packages

setup(
    name="aipractical_data",
    version="0.1",
    description="A sample package that includes CSV and text files",
    author="Your Name",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # Specify the directory and file types to include in the package
        "aipractical_data": ["data/*"],
    },
    install_requires=[
        # Add any dependencies here
    ],
)
