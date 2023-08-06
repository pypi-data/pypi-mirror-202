from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A package to work with a database'
LONG_DESCRIPTION = 'Python package to work with a database for our project'

setup(
        name="work_with_database", 
        version=VERSION,
        author="Yan Novikau",
        author_email="s24238@pjwstk.edu.pl",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        url="https://github.com/y4kenz1/ppy-project",
        packages=find_packages(),
        python_requires=">=3.6",
        install_requires=[]
)