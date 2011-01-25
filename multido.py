#! /usr/bin/env python

from ds import DS

import optparse
import os
import string
import sys

def safe_subs(tmpl, subs):
    """Substitute and throw exceptions when missing keys."""
    t = string.Template(tmpl)
    s = ''
    try:
        s = t.substitute(subs)
    except KeyError as e:
        print ('Error: did not find value for key: %s' % e)
        sys.exit(1)
    return s

def easy_subs(tmpl, subs):
    """Substitute but ignore lines with missing keys."""
    t = string.Template(tmpl)
    s = t.safe_substitute(subs)
    return '\n'.join(l for l in s.split('\n') if l.find('$') == -1)

def eval_subs(subs_path):
    with open(subs_path) as subs_file:
        exec subs_file.read()
    return result

def name_keys(ds):
    number = 0
    counter = {}
    for d in ds:
        number += 1
        for k,v in d.iteritems():
            counter[k] = counter.get(k, 0) + 1
    return number, [k for k,v in counter.iteritems() if v > 1]

def main():
    parser = optparse.OptionParser(usage='usage: %prog [options] <template>... <substitutions>')
    parser.add_option('-s', '--safe', action="store_true", default=False,
                      help='substitute safely and abort with missing keys')
    parser.add_option('-q', '--quiet', action="store_true", default=False,
                      help='do not print progress counter')
    (options, args) = parser.parse_args()
    if len(args) < 2:
        parser.error('incorrect number of arguments')

    tmpl_paths = args[:-1]
    subs_path  = args[-1]

    # get settings and determine active keys
    ds = eval_subs(subs_path)
    number, keys = name_keys(ds)

    # prepare progress bar
    step = number / 30
    if step == 0:
        options.quiet = True

    # first read in all template files once
    tmpls = {}
    for tmpl_path in tmpl_paths:
        tmpl_file = open(tmpl_path)
        basename = os.path.split(tmpl_path)[-1]
        tmpls[basename] = tmpl_file.read()
        tmpl_file.close()

    runs_file = open('runs', 'w')
    for i, d in enumerate(ds):
        # print progress bar
        if not options.quiet and ((i+1) % step) == 0:
            sys.stdout.write('\r%5d / %5d [%-30s]' % (i+1, number, '='*(i/step) + '>'))
            sys.stdout.flush()

        ids = ('%05d' % i)
        key = ','.join(('%s=%s' % (k, str(d[k]))) for k in keys)

        try:
            os.mkdir(ids)
        except OSError as e:
            print 'Error, will not overwrite existing file:', e.filename
            sys.exit(1)

        for tmpl_path, tmpl in tmpls.iteritems():
            result_file = open(os.path.join(ids, ids + '.' + tmpl_path), 'w')
            if options.safe:
                result = safe_subs(tmpl, d)
            else:
                result = easy_subs(tmpl, d)
            result_file.write(result)
            result_file.close()
        runs_file.write(ids + ' ' + key + '\n')

    # finish progress bar
    if not options.quiet:
        sys.stdout.write('\r%5d / %5d [%-30s]' % (number, number, '='*30))
        sys.stdout.flush()

    runs_file.close()

if __name__ == '__main__':
    main()
