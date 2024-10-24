from setuptools import setup, find_packages

setup(
    name='Fcstatistics',
    version='0.0.3',
    description='Fc statistics algorithm',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='fourchains_R&D',
    author_email='fourchainsrd@gmail.com',
    url='https://github.com/leechaeeyoung/Fc',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.6',
)
