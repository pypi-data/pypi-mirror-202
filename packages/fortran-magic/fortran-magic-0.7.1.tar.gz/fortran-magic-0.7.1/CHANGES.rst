
Changelog
=========

0.7.1 / 2022-04-12
------------------

- Synchronize version number in fortranmagic.py & setup.py (TBD, TBD, https://github.com/Serge3leo)

- Patch fortran source in compiled object. (029d890, 2020-08-01, https://github.com/mgaitan)

- Fix deprecation warning (3667bc1, 2017-08-18, https://github.com/guihigashi)
  [IPython.utils.path removed from IPython 8.x] 

- Simplify f2py execution. (d8a058f, 2016-06-04, https://github.com/QuLogic)
  Don't change directories, and don't mangle `sys.argv`. The former can be
  specified directly in the `Popen` constructor, and the latter is cruft
  from when the f2py module was imported directly.


0.7 / 2016-03-13 
----------------

- Fix cross compatibility with older NumPy and Python 3. (15ab10c)

Thanks to `Elliott Sales de Andrade`_ for this contribution

.. _Elliott Sales de Andrade: https://github.com/QuLogic


0.6 / 2015-12-02
----------------

- Decode text before printing
- Call f2py module instead of binary (numpy >=1.10 is mandatory)
- Check if f2py command failed

Thanks to `Juan Luis Cano Rodríguez`_ for this contribution

.. _Juan Luis Cano Rodríguez: https://github.com/Juanlu001


0.5 / 2015-01-21
----------------

- Call f2py via subprocess. It fixes problems finding fortran compilers under Windows. (Thanks to `David Powell`_ )

.. _David Powell: https://github.com/DavidPowell

0.4.3 / 2013-12-09
-------------------

- Fix two python3.2+ incompatibilities (Thanks `Ramon Crehuet`_ for the report)

.. _Ramon Crehuet: https://github.com/rcrehuet

0.4.2 / 2013-10-08
------------------

- Implement the ``--extra`` option (Thanks to `Denis Vasilyev`_ for the help)
- Include ``%%fortran``'s args in the hashing, so the same cell are
  recompiled with the same code but different arguments

.. _Denis Vasilyev: https://github.com/Vutshi

0.3 / 2013-10-03
------------------

- Added ``%fortran_config`` to set and persist default arguments
  for ``%%fortran``
- Improve documentation

0.2.1 / 2013-09-24
------------------

- Packaged and registered in pypi
- Starting a version's changelog

0.2 / 2013-09-19
----------------

- Fortran highlighting in a ``%%fortran`` cell
- Works (or it should) in any platform (linux/windows/osx)
  and with py3 (thanks to `Bradley Froehle`_)
- Many f2py's arguments exposed as magic arguments
- Verbosity handling
- Improved documentation

.. _Bradley Froehle: https://github.com/bfroehle

0.1 / 2013-09-08
----------------

- First public release