from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.0.1'
DESCRIPTION = 'Quality Assurance data and machine learning'
LONG_DESCRIPTION = 'Quality assurance (QA) data and machine learning are essential\
      components in the development and maintenance of machine learning models, \
    particularly in open-source projects hosted on platforms like GitHub. Quality\
    assurance in this context refers to the process of ensuring that \
    the data used to train, validate, and test machine learning models meets\
    specific quality standards. This is crucial in order to build models that \
    are accurate, reliable, and robust.'

# Setting up
setup(
    name="quality-assurance-data",
    version=VERSION,
    author="quality-assurance-data AI Team",
    author_email="<alinemati@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['python', 'pandas', 'numpy', 'scikit-learn', 'scipy', 'matplotlib', 'seaborn', 'tqdm'],
    keywords=['python', 'pandas', 'numpy', 'scikit-learn', 'scipy', 'matplotlib', 'seaborn'],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: Free To Use But Restricted",

    ] ,
)
