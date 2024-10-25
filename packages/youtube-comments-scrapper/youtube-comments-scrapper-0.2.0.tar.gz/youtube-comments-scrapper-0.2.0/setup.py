from setuptools import setup, find_packages

setup(
    name='youtube-comments-scrapper',  # Replace with your package name
    version='0.2.0',
    description='A Python package to scrape YouTube comments using Selenium and BeautifulSoup',
    author='Abhishek Kumar',
    author_email='abhiop.dev@gmail.com',
    url='https://github.com/yourusername/youtube-comment-scraper',  # Replace with your repository URL
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'selenium>=4.25.0',
        'webdriver-manager>=4.0.2',
        'beautifulsoup4>=4.12.3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
