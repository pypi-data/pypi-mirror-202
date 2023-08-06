from setuptools import setup, find_packages

setup(
    name='HaiqvML',
    version='0.0.1',
    description='HaiqvMLops SDK wrapped mlflow',
    author='haha2432',
    author_email='haha2432@gmail.com',
    url='https://github.com/teddylee777/teddynote',
    install_requires=['mlflow'],
    packages=find_packages(exclude=[]),
    keywords=['haiqv','mlflow','haiqvml'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[        
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
