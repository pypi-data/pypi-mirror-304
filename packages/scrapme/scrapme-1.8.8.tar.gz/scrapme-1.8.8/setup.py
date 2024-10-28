from setuptools import setup, find_packages

# Read README.md with UTF-8 encoding
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="scrapme",
    version="1.8.8",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4>=4.9.0',
        'requests>=2.25.0',
        'pandas>=1.2.0',
        'selenium>=4.0.0',
        'trafilatura>=1.4.0'
    ],
    python_requires='>=3.8',
    author="N.Sikharulidze",
    author_email="info@ubix.pro",
    description="A comprehensive web scraping framework featuring both static and dynamic content extraction, automatic Selenium/geckodriver management, rate limiting, proxy rotation, and Unicode support (including Georgian). Built with BeautifulSoup4 and Selenium, it provides an intuitive API for extracting text, tables, links and more from any web source.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ubix.pro/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/NSb0y/scrapme/issues",
        "Documentation": "https://github.com/NSb0y/scrapme",
        "Page": "https://ubix.pro",
    },
)
