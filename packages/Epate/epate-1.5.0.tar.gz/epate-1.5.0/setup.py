from setuptools import setup, find_packages

from pkg_resources import parse_requirements

install_requires = ['requests']

setup(name="Epate",
      version="1.5.0",
      author="xiaoxlh",
      author_email="xiaoxiaogzs@outlook.com",
      description="A python library for many API of the codemao's website.",
      long_description="look at https://github.com/xiaoxat/Epate",
      license="Apache License, Version 2.0",
      url="https://xihl.cn",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          "Programming Language :: Python :: 3.12",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      packages=find_packages(),
      install_requires=install_requires,
      entry_points={'console_scripts': ['test = test.help:main']})
