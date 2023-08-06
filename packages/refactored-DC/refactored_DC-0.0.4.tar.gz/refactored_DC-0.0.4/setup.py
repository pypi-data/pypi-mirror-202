from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Test package'
LONG_DESCRIPTION = 'Test package.'

# Setting up
setup(
    name="refactored_DC",
    version=VERSION,
    author="Poly",
    author_email="<ghassendaoud99@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={'refactored_DC': ['config/settings.yaml', 'config/messages.properties']},
    install_requires=['fastnumbers'],
    keywords=['python', 'cnn', 'test'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)