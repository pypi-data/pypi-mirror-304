from setuptools import setup, find_packages

setup(
    name='infin8t',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'flask'
    ],
    author='Infin8t Team',
    author_email='support@infin8t.tech',
    description='A Python package for integrating AI-powered chatbots into web applications',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/infin8t',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
