from setuptools import setup, find_packages


def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


setup(
    name="SystemsSolver",
    python_requires='>=3.6',
    version="1.0.0",
    description="SystemsSolver",
    author="Nicolas Primeau",
    author_email="nicolas.primeau@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'run-solver-app=bin.app:main',
        ]
    },
    install_requires=[
        "flask"
    ]
)
