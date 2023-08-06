from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='smobot_api',
    version='0.0.4',
    url='https://github.com/adam-mckee/smobot_api',
    description='Pull data for your Smobot Controller',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='adam-mckee',
    author_email='invalid@example.org',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='smobot_api',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'asyncio',
        'aiohttp'
    ]
)
