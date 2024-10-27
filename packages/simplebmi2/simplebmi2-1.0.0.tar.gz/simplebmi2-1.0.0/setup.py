from setuptools import setup, find_packages

setup(
    name='simplebmi2',  # Updated package name
    version='1.0.0',
    author='Muhammad Sohaib Hassan',
    author_email='muhammadsohaibhassan3@gmail.com',
    description='A minimal BMI calculator',
    long_description=open('README.md').read(),  # Reads from README.md if it exists
    long_description_content_type='text/markdown',  # Specify the format of long description
    packages=find_packages(),  # Automatically find packages in the current directory
    entry_points={
        'console_scripts': [
            'simple-bmi = simplebmi2.__main__:main',  # Updated entry point for command line
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Change as necessary
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the minimum Python version required
    install_requires=[  # Specify any dependencies your package needs
        # Example: 'numpy>=1.19.0',
    ],
)
