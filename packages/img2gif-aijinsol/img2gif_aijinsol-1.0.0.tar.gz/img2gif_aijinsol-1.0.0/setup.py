from setuptools import setup, find_packages


setup(
    name             = 'img2gif_aijinsol',
    version          = '1.0.0',
    description      = 'Images to GIF Converter',
    author           = 'aijinsol',
    author_email     = 'jinsolkim719@gmail.com',
    url              = '',
    download_url     = '',
    install_requires = ['pillow'],
	include_package_data = True,
	packages         = find_packages(),
    keywords         = ['img2gif', 'gifconverter'],
    python_requires  = '>=3',
    zip_safe         = False,
    classifiers      = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
) 