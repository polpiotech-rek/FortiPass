from setuptools import setup, find_packages

setup(
    name="fortipass",
    version="0.1",
    description="A password generator program.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Piotr Bodych",
    author_email="polpiotech@gmail.com",
    url="https://example.com/fortipass",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        #'requests',
        #'pyyaml',
    ],
    extras_require={
        #'dev': ['pytest', 'tox'],
        #'docs': ['sphinx'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'fortipass = fortipass.main:main',
        ],
    },
    python_requires='>=3.9',
    zip_safe=False,
    license='MIT',
    #test_suite='tests',
    tests_require=['pytest'],
    package_data={
        'fortipass': ['data/*.json', 'config/*.yml'],
    },
)