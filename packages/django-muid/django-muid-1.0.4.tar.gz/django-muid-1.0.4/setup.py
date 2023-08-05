from setuptools import setup, find_packages

setup(
    name="django-muid",
    version="1.0.4",
    description="MUID field for Django",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/angelcamelot/django-muid",
    author="Angel Camelot",
    author_email="dupeyron.camelot@gmail.com",
    packages=find_packages(),
    install_requires=[
        "django",
        "Pillow",
        "treepoem",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
