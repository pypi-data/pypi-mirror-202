
from setuptools import setup, find_packages, Distribution


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""

    # pylint: disable=no-self-use
    def has_ext_modules(self):
        """Distribution which always forces a binary package with platform name"""
        return True


with open("./src/HardwareLibrary/version.py", "r") as fh:
    VersionFile = fh.read()
    VersionFile = VersionFile.replace("\n", "")
    IGNORE, VERSION = VersionFile.split(" = ")
    VERSION = VERSION.replace("\"", "")

with open("./Readme.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

REQUIREMENTS = []
with open("./requirements.txt", "r") as f:
    REQUIREMENTS = list(filter(lambda s: s != "", f.read().split("\n")))

setup(name="robotframework-hardware-jim",
      version=VERSION,
      description="Support Command and GUI operation for Windows",
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown",
      author="HP",
      author_email="jim.tang@hp.com",
      url = 'https://github.com/JimRevolutionist/robotframework-hardware',
      license='MIT',
      install_requires=REQUIREMENTS,
      packages=find_packages("src"),
      package_dir={"HardwareLibrary": "src/HardwareLibrary"},
    #   package_data={"HardwareLibrary": ["bin/*.dll"]},
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "License :: OSI Approved :: MIT License",
          "Operating System :: Microsoft",
          "Topic :: Software Development :: Testing",
          "Framework :: Robot Framework",
          "Framework :: Robot Framework :: Library"
      ],
      distclass=BinaryDistribution,
      platforms=['Windows']
      )
