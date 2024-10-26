from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of the README file
here = Path(__file__).parent
long_description = (here / "README.md").read_text(encoding='utf-8')

setup(
    name='relaxtemplates',
    version='1.0.2',
    description='A Python-based template engine that features variables, conditionals, loops, call, extends, includes, comments, and more, making it easy to create dynamic web pages.',
    author='Ravi Kishan',
    author_email='ravikishan63392@gmail.com',
    url='https://github.com/Ravikisha/relaxtemplates',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),  # Automatically find packages in the same directory
    python_requires='>=3.8',
    install_requires=[],  # No dependencies
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords=[
        'template engine',
        'python',
        'dynamic templates',
        'web development',
        'variables',
        'conditionals',
        'loops',
        'includes',
        'extends',
        'comments'
    ]
)
