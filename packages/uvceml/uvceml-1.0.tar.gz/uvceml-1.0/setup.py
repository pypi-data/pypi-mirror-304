from setuptools import setup, find_packages

setup(
    name='uvceml',
    version='1.0',
    description='List Of ML Programs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Ganesh57803/uvceml',
    author='Ganesh',
    author_email='ganesh4study@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'pgmpy',
        'matplotlib'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
