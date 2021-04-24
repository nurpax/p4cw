#!/usr/bin/env python3

import argparse
import os
import subprocess
import tempfile
import sys
import re

from typing import List, Optional, Tuple


def friendlify(spec: List[str]) -> Tuple[Optional[str], List[str]]:
    if len(spec) < 1:
        return None, spec
    if spec[0].startswith('# A Perforce Client Specification.'):
        spec_out = []
        client_spec_name = None
        state = 'spec'
        for line in spec:
            if state == 'spec':
                if m := re.match(r'^Client:\s+(.*)$', line):
                    client_spec_name = m[1]
                    spec_out.append(line)
                    continue
                if re.match(r'^View:\s*$', line):
                    state = 'view'
                    spec_out.append(line)
                    continue
                # Pass everything else through as-is.
                spec_out.append(line)
            elif state == 'view':
                if m := re.match(r'^\t//([a-zA-Z0-9_-]+)/(.*) //([a-zA-Z0-9_-]+)/(.*)$', line):
                    # friendlify client spec mapping
                    depot = m[1]
                    depot_path = m[2]
                    client_name = m[3]
                    client_path = m[4]
                    if (depot_path == client_path) and (client_name == client_spec_name):
                        spec_out.append(f'\t//{depot}/{depot_path}')
                    else:
                        spec_out.append(line)
                    continue
                else:
                    state = 'spec'
                    spec_out.append(line)
                    continue
        return 'clientspec', spec_out
    return None, spec


def unfriendlify(spec: List[str], spec_type: Optional[str]) -> List[str]:
    if spec_type is None or len(spec_type) < 1:
        return spec
    assert spec_type in ['clientspec']
    if spec_type == 'clientspec':
        spec_out = []
        client_spec_name = None
        state = 'spec'
        for line in spec:
            if state == 'spec':
                if m := re.match(r'^Client:\s+(.*)$', line):
                    client_spec_name = m[1]
                elif re.match(r'^View:\s*$', line):
                    state = 'view'
                # Pass everything else through as-is.
                spec_out.append(line)
            elif state == 'view':
                # TODO exclusions prefixed with `-` not supported yet.
                if m := re.match(r'^\t//([a-zA-Z0-9_-]+)/(.*)$', line):
                    depot = m[1]
                    depot_path = m[2]
                    # Add client path mapping back.
                    spec_out.append(f'\t//{depot}/{depot_path} //{client_spec_name}/{depot_path}')
                elif m := re.match(r'^\t//.*$', line):
                    # Pass other types of client spec mappings as-is.
                    spec_out.append(line)
                else:
                    state = 'spec'
                    spec_out.append(line)
        return spec_out
    assert False, 'unknown spec type'


def main():
    parser = argparse.ArgumentParser(
        description='Wrapper for Perforce `p4 client` editor  (See https://github.com/nurpax/p4cw.)'
    )

    parser.add_argument('spec', metavar='FILE', nargs=1,  help='input file')
    parser.add_argument('--stdout', action='store_true', help='Print edited spec on stdout for debugging')
    args = parser.parse_args()

    real_editor = os.environ.get('EDITOR')
    if real_editor is None or real_editor == '':
        print ('EDITOR must be set')
        sys.exit(1)

    # Read input spec from p4 (this can be a client spec, submit spec, or similar.)
    with open(args.spec[0], 'rt') as f:
        spec_in = [line.rstrip(' \r\n') for line in f.readlines()]

    fd, path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'w') as tmp:
            spec_type, lines = friendlify(spec_in)
            tmp.write('\n'.join(lines) + '\n')

        # Spawn editor for the "friendlier" version of the input spec for the user
        # to edit.
        subprocess.run([real_editor] + [path], check=True)

        with open(path, 'rt') as tmp:
            # Transform friendly format spec back to something p4 can understand
            # and save to disk.
            spec_out = unfriendlify([line.rstrip(' \r\n') for line in tmp.readlines()], spec_type)
            if args.stdout:
                print ('\n'.join(spec_out) + '\n')
            else:
                with open(args.spec[0], 'wt') as fout:
                    fout.write('\n'.join(spec_out) + '\n')
    finally:
        os.remove(path)


if __name__ == "__main__":
    main()
