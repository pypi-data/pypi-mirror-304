from setuptools import setup, find_packages

setup(
    name='WebTableScrapper',
    version='0.1',
    packages=find_packages(),
    description='Table scrapping Module',
    author='Abdhul Rahim Sheikh M',
    author_email='mbabdhulrahim@gmail.com',
    url='https://github.com/yourusername/web_scraper',
    install_requires=[
        "pandas>=1.0",
        "selenium>=4.0",
        "beautifulsoup4>=4.9",
        "webdriver-manager>=3.5",
        "lxml"
    ],

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
