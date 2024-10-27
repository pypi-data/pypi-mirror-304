from setuptools import setup, find_packages

setup(
    name='erd_mesh',
    version='0.1.1',
    description='to use with mesh-* packages',
    author='ivan',
    author_email='pypi@eriad.com',
    url='https://github.com/ivan-loh/erd_mesh',  # Your GitHub repo URL
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-dotenv'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.12',
)
