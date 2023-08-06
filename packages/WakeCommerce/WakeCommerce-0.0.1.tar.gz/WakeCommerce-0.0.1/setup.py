from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'WakeCommerce API Request Module'
LONG_DESCRIPTION = 'A package that allows to request WakeCommerce API with ease.'

setup(
    name="WakeCommerce",
    version=VERSION,
    author="Elemental (Tom Neto)",
    author_email="<info@elemental.run>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'WakeCommerce', 'TrayCorp', 'API', 'Request'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)