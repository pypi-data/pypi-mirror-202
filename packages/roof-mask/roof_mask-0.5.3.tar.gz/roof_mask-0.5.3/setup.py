## test upload
import setuptools

setuptools.setup(
    name = "roof_mask",
    version = "0.5.3",
    author = "Ruixu",
    author_email = "lrxjason@gmail.com",
    description = "upload pip package test",
    long_description = 'v0.5.3: backend errors (coded as 11, 21, 31, and 41) from image vender and geo-coding vender are raised as exceptions and passed back to the caller.',
    long_description_content_type="text/markdown",
    url="https://github.com/lrxjason/roof_model_test/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
