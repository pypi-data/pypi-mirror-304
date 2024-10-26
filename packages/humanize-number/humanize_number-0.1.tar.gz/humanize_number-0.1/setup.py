from setuptools import setup, find_packages

setup(
    name='humanize_number',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    test_suite='tests',
    author='David Conteh',
    author_email='programmingdonebydavid@gmail.com',
    description='A package to humanize numbers into readable formats like 1K, 1M',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/davidddeveloper/humanize_number',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)