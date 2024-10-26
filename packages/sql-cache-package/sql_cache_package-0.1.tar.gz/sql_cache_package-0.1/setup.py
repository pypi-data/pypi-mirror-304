from setuptools import setup, find_packages

setup(
    name='sql_cache_package',
    version='0.1',
    description='A package for intelligent SQL query caching and results storage',
    long_description=open("README.md").read(),  # Detailed description from README.md
    long_description_content_type="text/markdown",  # README file format
    author="Pooja Sambhwani",  # Your name
    author_email="sambhwanipooja08@gmail.com",  # Your email
    url="https://github.com/poojasambhwani/sql_cache_package",  # URL to your project's repo (if any)
    packages=find_packages(),
    python_requires='>=3.6',  # Minimum Python version requirement
    classifiers=[  # PyPI classifiers
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pandas',
        'pyarrow',
        'redis',
    ],
    entry_points={
        'console_scripts': [
            'sql_cache=sql_cache.main:main',
        ],
    },
)
