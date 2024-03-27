import setuptools

setuptools.setup(
    name="yosemite-tiny",
    version="0.1.0",
    author="Hammad Saeed",
    author_email="hammad@supportvectors.com",
    description="yosemite tiny",
    entry_points={
        'console_scripts': [
            'yosemite-tiny = yosemite_tiny.__cli__.cli:main',
        ],
    },
    long_description="""
Yosemite
    """,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.9',
    install_requires=[
"art",
"libhammadpy-text",
"prompt_toolkit",
"wcwidth",
    ],
)