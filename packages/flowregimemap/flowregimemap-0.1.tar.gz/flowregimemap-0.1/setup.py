from setuptools import setup

setup(
    name='flowregimemap',  # The package name for PyPI
    version='0.1',
    description='A Python package to predict flow regimes and plot flow regime maps',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Abdulrahman Shahin',
    author_email='your.email@example.com',
    url='https://github.com/abdopetroleum/flowregimemap',  # Your GitHub repository URL
    py_modules=['taitel_and_dukler_map'],  # Reference to your Python file
    install_requires=['numpy', 'matplotlib'],  # Dependencies for your package
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
