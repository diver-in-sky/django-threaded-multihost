"""
Based entirely on Django's own ``setup.py``.
"""
import os
from distutils.command.install import INSTALL_SCHEMES
from distutils.core import setup

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
extensions_dir = os.path.join(root_dir, 'threaded_multihost')
pieces = fullsplit(root_dir)
if pieces[-1] == '':
    len_root_dir = len(pieces) - 1
else:
    len_root_dir = len(pieces)

for dirpath, dirnames, filenames in os.walk(extensions_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    #if 'conf' in dirpath:
    #    print dirpath
    if '__init__.py' in filenames and not 'conf' in dirpath:
        packages.append('.'.join(fullsplit(dirpath)[len_root_dir:]))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

version = __import__('threaded_multihost').__version__

setup(
    name = 'threaded_multihost',
    version = version,
    description = "Django Threaded Multihost",
    long_description = """django-threaded multihost provides support utilities to
    enable easy multi-site awareness in Django apps.""",
    author = 'Bruce Kroeze',
    author_email = 'brucek@solidsitesolutions.com',
    url = 'http://getbanjo.com/threaded-multihost/',
    license = 'New BSD License',
    platforms = ['any'],
    packages = packages,
    data_files = data_files,
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
)