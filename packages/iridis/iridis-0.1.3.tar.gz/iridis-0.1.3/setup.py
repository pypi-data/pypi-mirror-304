from setuptools import setup, find_packages

setup(
    name="iridis",
    version="0.1.3",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Tobias Filgas",
    author_email="tobias.filgas@student.mgvsetin.cz",
    url="https://github.com/realtobi999/Python_PrettyPrint",
    packages=find_packages(),
    include_package_data=True, 
    install_requires=[],  
    python_requires=">=3.6",
)
