from setuptools import setup, find_packages

setup(
    name="flexiparse",
    version="0.3.0",
    description="A dynamic JSON parser for OpenSearch API responses.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Andrew Gordienko",  # Replace with your name
    author_email="gordienko.adg@gmail.com",  # Replace with your email
    url="https://github.com/AndrewGordienko/flexiparse",  # Replace with your URL or GitHub link
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'flexiparse=flexiparse.main:process_data',  # Entry point for CLI
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

