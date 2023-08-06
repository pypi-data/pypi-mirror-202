from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gotya-text-anonymizer',
    version='1.1.0',
    description='A text anonymizer to redact sensitive information',
    author='Gotya Tech',
    author_email='technical.team@gotya.tech',
    packages=find_packages(),
    install_requires=[
        'transformers',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
