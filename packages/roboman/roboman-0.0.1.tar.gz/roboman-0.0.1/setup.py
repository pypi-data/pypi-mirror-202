import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='roboman',  
     version='0.0.1',
     author="Homagni Saha",
     author_email="homagnisaha@gmail.com",
     description="ROBOtic perception using Modules And Neural networks- A modular perception library for machine learning in robotics use cases",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/Homagn/roboman",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
