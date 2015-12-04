# GOK-whatsapp

## Installation 
(Updated Jan 12, 2015)

 - Requires python2.6+, or python3.0 +
 - Required python packages: python-dateutil, 
 

### Linux

You need to have installed python headers (from probably python-dev package) and ncurses-dev, then run
```
python setup.py install
```
Because of a bug with python-dateutil package you might get permission error for some dateutil file called requires.txt when you use yowsup (see [this bug report](https://bugs.launchpad.net/dateutil/+bug/1243202)) to fix you'll need to chmod 644 that file.

### Mac
```
python setup.py install
```
Administrators privileges might be required, if so then run with 'sudo' 

### Windows

 - Install [mingw](http://www.mingw.org/) compiler
 - Add mingw to your PATH
 - In PYTHONPATH\Lib\distutils create a file called distutils.cfg and add these lines:
 
```
[build]
compiler=mingw32
```
 - Install gcc: ```mingw-get.exe install gcc```
 - Install [zlib](http://www.zlib.net/)
 - ```python setup.py install```

If pycrypto fails to install with some "chmod error". You can install it separately using something like 
```easy_install http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe```

or for python3 from:

 > [https://github.com/axper/python3-pycrypto-windows-installer](https://github.com/axper/python3-pycrypto-windows-installer)

and then rerun the install command again



# License:

As of January 1, 2015 yowsup is licensed under the GPLv3+: http://www.gnu.org/licenses/gpl-3.0.html.
