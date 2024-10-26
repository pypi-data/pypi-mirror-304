from setuptools import setup, find_packages

setup(
    name='aipp',
    version='0.1.1',
    description='A simple package with multiple file types',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='naice',
    author_email='xxx@gmail.com',
    url='https://github.com/yourusername/my_package',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
    install_requires=[
        # List your dependencies here
    ],
)