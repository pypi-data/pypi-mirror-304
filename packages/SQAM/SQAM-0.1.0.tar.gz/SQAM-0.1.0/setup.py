from setuptools import setup, find_packages

setup(
    name='SQAM',  # Package name
    version='0.1.0',  # Version number
    description='Simplified Question Answering Machine',
    long_description=open('README.md').read(),  # Use README for the long description
    long_description_content_type='text/markdown',
    author='preslaff',
    author_email='preslaff@gmail.com',
    url='https://github.com/preslaff/SQAM',
    packages=find_packages(),  # Automatically find the packages in sqam/
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    install_requires=[
        'Flask',
        'numpy',
        'sentence-transformers',
        'scikit-learn',
        'pytest'
    ],
    entry_points={
        'console_scripts': [
            'sqam=sqam.app:main',  # Allow starting the app from the command line
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
