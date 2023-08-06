from setuptools import setup, find_packages


setup(
    name='bpctl',
    version='1.1',
    author='Tajinder kumar',
    author_email='tajinder.kumar@opstree.com',
    description='A sample Python package',
    packages=find_packages(),
    url="https://gitlab.com/ot-okts/base/bpctl",
    install_requires=[
        'requests>=2.22.0',
        'PyYAML>=3.10,<5.5'
    ],
    python_requires='>=3.6',
    
)