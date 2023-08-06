import setuptools

setuptools.setup(
    name="pm4edu",
    version="0", 
    description="Python Package",
    packages=setuptools.find_packages('src'),
    package_dir={'':'src'},
    install_requires=[
        'pandas'
    ]
)