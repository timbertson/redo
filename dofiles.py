from __future__ import print_function
import os
from os import path
import itertools

def _default_do_files(filename):
    l = filename.split('.')
    for i in range(1,len(l)+1):
        ext = '.'.join(l[i:])
        if ext: ext = '.' + ext
        yield ("default%s.do" % ext), ext

def _up_path(n):
    return '/'.join(itertools.repeat('..',n))

def _possible_do_files(p):
    r'''
    Finds all possible do files for a target.

    This combines the stacking of different levels
    of "default" fallback (e.g default.tar.gz.do,
    default.gz.do, default.do) as well as the
    genericness of dofiles (a/b/default.do is
    more generic than a/b/c/default.do).

    For any given dofile & level of genericity, we have to
    try all variations of that path that may be under a do/
    dir instead of a direct parent of the target.

    Each entry yields:
        dodir:    folder containing .do file
        dofile:   filename of .do file
        ext:      extension used to resolve default .do file
                  (e.g for default.foo.do, this is '.foo')

    >>> for (base, dofile, ext) in _possible_do_files('/a/b/c/d/e.ext'):
    ...     print(os.path.join(base, dofile))
    /a/b/c/d/e.ext.do
    /a/b/c/d/do/e.ext.do
    /a/b/c/d/../do/d/e.ext.do
    /a/b/c/d/../../do/c/d/e.ext.do
    /a/b/c/d/../../../do/b/c/d/e.ext.do
    /a/b/c/d/../../../../do/a/b/c/d/e.ext.do
    /a/b/c/d/default.ext.do
    /a/b/c/d/do/default.ext.do
    /a/b/c/d/../do/d/default.ext.do
    /a/b/c/d/../../do/c/d/default.ext.do
    /a/b/c/d/../../../do/b/c/d/default.ext.do
    /a/b/c/d/../../../../do/a/b/c/d/default.ext.do
    /a/b/c/d/default.do
    /a/b/c/d/do/default.do
    /a/b/c/d/../do/d/default.do
    /a/b/c/d/../../do/c/d/default.do
    /a/b/c/d/../../../do/b/c/d/default.do
    /a/b/c/d/../../../../do/a/b/c/d/default.do
    /a/b/c/d/../default.ext.do
    /a/b/c/d/../do/default.ext.do
    /a/b/c/d/../../do/c/default.ext.do
    /a/b/c/d/../../../do/b/c/default.ext.do
    /a/b/c/d/../../../../do/a/b/c/default.ext.do
    /a/b/c/d/../default.do
    /a/b/c/d/../do/default.do
    /a/b/c/d/../../do/c/default.do
    /a/b/c/d/../../../do/b/c/default.do
    /a/b/c/d/../../../../do/a/b/c/default.do
    /a/b/c/d/../../default.ext.do
    /a/b/c/d/../../do/default.ext.do
    /a/b/c/d/../../../do/b/default.ext.do
    /a/b/c/d/../../../../do/a/b/default.ext.do
    /a/b/c/d/../../default.do
    /a/b/c/d/../../do/default.do
    /a/b/c/d/../../../do/b/default.do
    /a/b/c/d/../../../../do/a/b/default.do
    /a/b/c/d/../../../default.ext.do
    /a/b/c/d/../../../do/default.ext.do
    /a/b/c/d/../../../../do/a/default.ext.do
    /a/b/c/d/../../../default.do
    /a/b/c/d/../../../do/default.do
    /a/b/c/d/../../../../do/a/default.do
    /a/b/c/d/../../../../default.ext.do
    /a/b/c/d/../../../../do/default.ext.do
    /a/b/c/d/../../../../default.do
    /a/b/c/d/../../../../do/default.do

    >>> for (base, dofile, ext) in itertools.islice(_possible_do_files('x/y/somefile'), 0, 3):
    ...     print(os.path.join(base, dofile))
    x/y/somefile.do
    x/y/do/somefile.do
    x/y/../do/y/somefile.do

    >>> for (base, dofile, ext) in itertools.islice(_possible_do_files('/x/y/somefile'), 0, 3):
    ...     print(os.path.join(base, dofile))
    /x/y/somefile.do
    /x/y/do/somefile.do
    /x/y/../do/y/somefile.do
    '''
    # we need an absolute path to tell how far up the tree we should go
    # XXX what about symlinks?
    dirname,filename = os.path.split(p)
    dirparts = os.path.normpath(os.path.join(os.getcwd(), dirname)).split('/')
    dirdepth = len(dirparts)

    # find direct match for `{target}.do` in all possible `/do` dirs
    yield (dirname, filename + '.do', '')
    for i in xrange(0, dirdepth):
        suff = '/'.join(dirparts[dirdepth - i:])
        base = path.join(dirname, _up_path(i))
        yield (path.join(base, 'do', suff), filename + '.do', '')

    dofilenames = list(_default_do_files(filename))
    for up in xrange(0, dirdepth):
        # `up` controls how "fuzzy" the match is, in terms
        # of how specific the path is - least fuzzy wins.
        #
        # As `up` increments, we discard a folder on the base path.
        # e.g the following have equal specificity:
        base_suff = '/'.join(dirparts[dirdepth - up:])
        for (dofilename, ext) in dofilenames:
            parent_base = path.join(dirname, _up_path(up))
            yield (parent_base, dofilename, ext)
            for i in xrange(0, dirdepth - up):
                # `i` is how far up the directory tree we're looking for the do/ directory
                suff = '/'.join(dirparts[dirdepth - i - up:dirdepth - up])
                base = path.join(parent_base, _up_path(i))
                yield (path.join(base, 'do', suff), dofilename, ext)
