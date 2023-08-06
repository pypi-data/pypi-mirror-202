from setuptools import setup, find_packages

setup(
    name='ynm3000',
    version='0.1.0',
    description='tools',
    author='sunyongdi',
    author_email='sunyd0305@gmail.com',
    url='https://github.com/sunyongdi/ynm3000',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
