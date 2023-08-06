from setuptools import setup

setup(name="hagis",
      version="0.1",
      description="A high availability GIS client",
      url="https://github.com/jshirota/Hagis",
      author="Jiro Shirota",
      author_email="jshirota@gmail.com",
      license="MIT",
      packages=["hagis"],
      zip_safe=False,
      install_requires=["requests"])
