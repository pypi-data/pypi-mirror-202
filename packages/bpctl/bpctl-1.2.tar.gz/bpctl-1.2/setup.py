from setuptools import setup, find_packages


setup(
    name='bpctl',
    version='1.2',
    author='Amit Kumar Tiwari',
    author_email='amit.tiwari@opstree.com',
    description='A sample Python package',
    packages=find_packages(),
    url="https://github.com/OT-BUILDPIPER-MARKETPLACE/bpctl",
    install_requires=[
        'requests>=2.22.0',
        'PyYAML>=3.10,<5.5'
    ],
    python_requires='>=3.6',
    
)