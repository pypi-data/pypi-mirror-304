from setuptools import setup, find_packages

setup(
    name="centerer",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[],
    description="A package to center text horizontally and vertically in the terminal",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="kbdevs",
    # author_email='your.email@example.com',
    # url='https://github.com/yourusername/centererpypi',
    # classifiers=[
    #     'Programming Language :: Python :: 3',
    #     'License :: OSI Approved :: MIT License',
    #     'Operating System :: OS Independent',
    # ],
    python_requires=">=3.6",
)
