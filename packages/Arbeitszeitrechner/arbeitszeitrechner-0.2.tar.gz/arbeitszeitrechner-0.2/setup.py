from setuptools import setup, find_packages

setup(
    name='Arbeitszeitrechner',
    version='0.2',
    description='Arbeitszeitrechner',
    author='Julian Egger, Marc Liesch',
    author_email='julian.elias.egger@outlook.com',
    packages=find_packages(),
    install_requires=[
        'customtkinter'
    ],
    entry_points={
        'gui_scripts': [
            'Arbeitszeitrechner=LucaZeitRechner.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)