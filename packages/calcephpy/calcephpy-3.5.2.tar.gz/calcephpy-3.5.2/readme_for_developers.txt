This file contains the instructions for the developers of the library.

To build the documentation using sphinx-doc, it requires the pip packages : 
    pip install Sphinx sphinx-fortran sphinx-rtd-theme sphinxcontrib-matlabdomain

To publish a new release, you have to :
- change the version number in the following files :
 configure.ac
 src/calceph.h

- update the changelog in the following files :
 NEWS
 doc/source/calceph.final.rst

- update the version of the library using the instructions of
  http://www.gnu.org/software/libtool/manual/html_node/Updating-version-info.html
  in the file :
 src/Makefile.am

- apply these previous changes:
  run the commands :
     autoreconf
     configure --enable-python=yes --enable-maintainer-mode
     cd doc && makedoc.sh && cd ..
     make clean && make
    
- under mac os, to build the final tarball : perform the following command
  # turn off special handling of ._* files in tar, etc.
  COPYFILE_DISABLE=1   make dist
  COPYFILE_DISABLE=1   make dist_octave


- build the archive for the Pypi (pip)
  run the commands (create the archive in the directory dist):
    rm -r -f dist
    make clean
    python setup.py sdist  
    
  test the package using testpypi:
    see instructions on https://wiki.python.org/moin/TestPyPI for .pypirc    
    twine upload dist/* -r testpypi
    pip install --user -i https://test.pypi.org/pypi calcephpy
    
   release of the package on pypi :
    see instructions on https://wiki.python.org/moin/TestPyPI for .pypirc    
    twine upload dist/*
    pip install --user  calcephpy
   
- publish the new version to homebrew
  run the commans
     export HOMEBREW_GITHUB_API_TOKEN=....yourtoken....
     cd /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core
     git -C $(brew --repo homebrew/core) checkout master
     brew bump-formula-pr  --sha256 ...shasum_-a_256....tar.gz...  --url https://www.imcce.fr/content/medias/recherche/equipes/asd/calceph/calceph-x.x.x.tar.gz calceph
      