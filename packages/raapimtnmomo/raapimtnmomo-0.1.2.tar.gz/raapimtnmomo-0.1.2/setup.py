from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='raapimtnmomo',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'momo-create-api-user = raapimtnmomo.create_api_user:main'
        ]
    },
    description='A package to interact with MTN MoMo API in Sandbox Mode',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Roméo AZAGBA',
    author_email='roazagba@gmail.com',
    url='https://github.com/roazagba/apimtnmomo-python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
