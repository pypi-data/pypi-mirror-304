
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pipc_flask_app",
    version='0.1.0b1',
    description="A plugin to create flask app for pipCreator.",
    author="Rakesh Kanna",
    author_email='rakeshkanna0108@gmail.com',
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.6",
    keywords=['plugin', 'flask', 'app', 'pipcreator'],
    install_requires=
        ['Flask==2.3.2', 'Flask-SQLAlchemy==3.0.3', 'Flask-Migrate==4.0.4', 
         'Flask-WTF==1.0.1', 'python-dotenv', 'pipCreator'],
    entry_points={"console_scripts":["pipc-flask = pipc_flask_app:cli"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Build Tools",
    ]
)
