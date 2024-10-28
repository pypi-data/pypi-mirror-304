from setuptools import setup, find_packages

version = '0.0.1'
setup(
    name='folder_test_lib',
    version=version,
    author='Mikynay',
    author_email='rast100man4ik@gmail.com',
    url='https://github.com/BeginnerDualist/forecastin',
    packages=find_packages(),
    install_requires=['matplotlib', 'numpy'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
