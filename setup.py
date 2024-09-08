from setuptools import setup, find_packages

setup(
    name='asciimage',
    version='0.1',
    packages=find_packages(),
    install_requires=['numpy',
                      'pillow',
                      ],
    entry_points={
        'console_scripts': [
            'asciimage = asciimage.core.converter:main'
        ],
    },
)
