from setuptools import setup, find_packages

setup(
    name="organizer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "colorama",
    ],
    entry_points={
        'console_scripts': [
            'organizer=organizer.main:main',
            'organizer-seed=organizer.seed:seed_demo_data',
        ],
    },
    author="spro77",
    description="A terminal-based organizer application",
    url="https://github.com/spro77/goit-final-1",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)