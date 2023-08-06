from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='magyar',
    version='2.6.1',
    description='Magyar nevek listája',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kobanya',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    author='Nagy Béla',
    author_email='nagy.bela.budapest@gmail.com',
    license='MIT',
    keywords='magyar nevek',
    include_package_data=True,
    install_requires=[],
)
