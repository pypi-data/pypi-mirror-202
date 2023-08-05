from setuptools import setup

setup(name='HomePay.Core',
      version='0.0.1',
      description='HomePay Blaze v2 RSA 2048 bit api signature integration python pack',
      py_modules=["payment"],
      package_dir={'': 'src'},
      classifiers=[],
      extras_require={
          "dev": [
              "pytest>=3.7",
          ]
      },
      zip_safe=False)
