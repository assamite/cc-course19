from setuptools import setup
setup(
    name="graphical_group_01",
    packages=["graphical_group_01"],
    version="0.0.1.dev1",
    description="Computational Creativity project",
    author="Fabio Colella et al.",
    author_email="fabio.colella@aalto.fi",
    url="https://github.com/fcole90/cc-course19/tree/master/graphical_group_01",
    download_url="https://github.com/fcole90/cc-course19/tree/master/graphical_group_01",
    keywords=["computational", "creativity", "artificial", "intelligence"],
    license="MIT License",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research"
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
        ],
    long_description="""\
Computational Creativity project on the Graphics topic.
""",
    install_requires=['numpy', 'Pillow'],
    python_requires='>=3.6'
)
