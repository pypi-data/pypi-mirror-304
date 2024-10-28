from setuptools import setup

setup(
    name='generate_reciept_tikhonmakeev',
    version='0.1',
    py_modules=['generate_reciept'],
    entry_points={
        'console_scripts': [
            'generate_reciept = generate_reciept:main'
        ]
    }
)