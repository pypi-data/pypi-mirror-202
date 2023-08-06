from setuptools import setup, find_namespace_packages

setup(
    name='nvosscript',
    version='1.2.3',
    description='nvos toolchain script',
    packages=find_namespace_packages(),
    author = 'andre.zhao',
    author_email = 'andre.zhao@nio.com',
    keywords='pack',
    readme = "README.md",
    install_requires=[],
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'ndtc=start.main:main',
            # Any other console scripts
        ]
    }
)