# Non-parametric optimization.<br>
# Find interesting bits. Combine them. Repeat.<br>
# [home](http://menzies.us/bnbab2)         :: [lib](http://menzies.us/bnbad2/lib.html) ::
# [cols](http://menzies.us/bnbad2/tab.html) :: [tbl](http://menzies.us/bnbad2/grow.html)<br>
# <hr>
# <a href="http://github.com/timm/bnbad2"><img src="https://github.com/timm/bnbad2/raw/main/etc/img/banner.png" align=left></a>
# [![DOI](https://zenodo.org/badge/326061406.svg)](https://zenodo.org/badge/latestdoi/326061406)<br>
# ![](https://img.shields.io/badge/platform-osx%20,%20linux-orange)<br>
# ![](https://img.shields.io/badge/language-python3,bash-blue)<br>
# ![](https://img.shields.io/badge/purpose-ai%20,%20se-blueviolet)<br>
# [![Build Status](https://travis-ci.com/timm/bnbad2.svg?branch=main)](https://travis-ci.com/timm/bnbad2)<br>
# ![](https://img.shields.io/badge/license-mit-lightgrey)
# --------

from distutils.core import setup

def readme():
  with open('README.md') as f:
    s = f.read()
    n = s.find("\n\n") + 2
    return s[n:]


setup(
    name='bnbad2',
    version='0.3',
    description='Non-parametric optimization',
    long_description=readme(),
    url='http://menzies.us/bnbad2',
    author='Tim Menzies',
    author_email='timm@ieee.org',
    license='MIT',
    packages=['bnbad2'],
    include_package_data=True,
    zip_safe=False,
    keywords='data mining, optimization',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ])
