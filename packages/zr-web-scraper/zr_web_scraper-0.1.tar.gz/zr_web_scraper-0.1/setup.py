from setuptools import setup, find_packages

setup(
    name='zr_web_scraper',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests',
        'pandas'
    ],
    author='Oluwafemi Olasegiri',
    author_email='olasegirioluwafemi@gmail.com',
    description='A simple Web scraper package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/olasegirioluwa3/zr_web_scraper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
