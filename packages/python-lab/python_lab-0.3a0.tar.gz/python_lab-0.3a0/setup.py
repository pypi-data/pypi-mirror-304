from setuptools import setup, find_packages

# Load dependencies from requirements.txt
def parse_requirements():
    """Parse requirements from the requirements.txt file."""
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='python-lab',
    version='v0.3-alpha',  # Updated version
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pylab=src.main:main',  # Command line script name
        ],
    },
    install_requires=parse_requirements(),  # Correctly load dependencies from requirements.txt
    author="Team VeHost",
    description="A workspace dedicated to experimenting with and exploring Python concepts.",
    license="MIT",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
