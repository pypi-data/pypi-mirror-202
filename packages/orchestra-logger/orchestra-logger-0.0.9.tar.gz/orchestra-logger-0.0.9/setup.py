from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description__ = "\n" + fh.read()

VERSION = '0.0.9'
DESCRIPTION = 'Logging module to enable orchestration on self-hosted applications'

# Setting up
setup(
    name="orchestra-logger",
    version=VERSION,
    author="Orchestra (Hugo Lu)",
    author_email="<hugo@getorchestra.io>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description__,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'logging', 'data', 'orchestration'],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9']
)
