from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='nanoclient',
    version='0.2.0',
    description='A nano python client to easily interact with the nano blockchain.',
    author='Celio Sevii',
    author_email='celiosevii@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords=['nano'],
    install_requires=[
        'numpy',
        'pandas'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/your_username/example_package/issues',
        'Source': 'https://github.com/your_username/example_package',
    },
    long_description=long_description,
    long_description_content_type="text/markdown"
)
