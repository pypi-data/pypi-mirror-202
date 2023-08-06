from setuptools import find_packages, setup

setup(
    name='voliboli_sgqlc_types',
    version='1.9',
    package_dir= {"": "src"},
    packages=find_packages(where="src"),
    description='Voliboli SGQLC Types',
    author='Teodor Janez Podobnik',
    license='MIT',
    install_requires=["sgqlc"],
)