import setuptools
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setuptools.setup(
    name="test-package-lenin",
    version="0.0.1",
    author="Lenin Loitongbam",
    author_email="clear.lenin@gmail.com",
    packages=["test_package_lenin"],
    description="A sample test package",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/leninloitongbam/test-package-lenin",
    license='MIT',
    python_requires='>=3.7',
    install_requires=[]
)