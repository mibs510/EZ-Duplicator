#!/usr/bin/env python3

#  Copyright (c) 2021 Connor McMillan. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
#  following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#  disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#  following disclaimer in the documentation and/or other materials provided with the distribution.
#
#  3. All advertising materials mentioning features or use of this software must display the following acknowledgement:
#  This product includes software developed by Connor McMillan.
#
#  4. Neither Connor McMillan nor the names of its contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY CONNOR MCMILLAN "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
#  EVENT SHALL CONNOR MCMILLAN BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
#  TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.

import argparse
import os.path
import sys


from EZDuplicator.version import __version__

parser = argparse.ArgumentParser(prog="setup.py",
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 epilog="setup.py - EZDuplicator v{}\n"
                                        "(c) 2021 Connor McMillan "
                                        "<connor@mcmillan.website>".format(__version__),
                                 exit_on_error=False)
parser.add_argument('--post', help='Add a post onto the semantic versioning for the wheel package.\n'
                                   'e.g. EZDuplicator-X.Y.Z.postW-py2.py3-none-any.whl',
                    action='store')

args, unkown = parser.parse_known_args()
sys.argv = [sys.argv[0]] + unkown
from setuptools import setup # noqa


if args.post is not None:
    __version__ = __version__ + "-" + args.post

if os.path.exists("README.md"):
    with open("README.md", "r") as fh:
        long_description = fh.read()

setup(
    name='EZDuplicator',
    version=__version__,
    platforms='linux',
    packages=['EZDuplicator', 'EZDuplicator/12VPM', 'EZDuplicator/lib', 'EZDuplicator/res', 'EZDuplicator/utils'],
    include_package_data=True,
    entry_points={"gui_scripts": ["EZDuplicator = EZDuplicator.EZDuplicator:main"],
                  "console_scripts": ["ezd-update = EZDuplicator.utils.update_ezduplicator:main",
                                      "ezd-generate_mount_map = EZDuplicator.utils.generate_mount_map:main",
                                      "ezd-generate_port_map = EZDuplicator.utils.generate_port_map:main"]},
    url='https://ezduplicator.com',
    license='BSD',
    author='Connor McMillan',
    author_email='connor@mcmillan.website',
    description='A simple GUI application to securely erase, duplicate, and verify USB flash memory in mass.',
    long_description=long_description,
    python_requires=">=3.9",
    install_requires=['certifi~=2021.10.8', 'charset-normalizer~=2.0.9', 'elevate~=0.1.3', 'idna~=3.3',
                      'keyboard~=0.13.5', 'numpy~=1.21.4', 'parse~=1.19.0', 'pexpect==4.8.0', 'psutil~=5.8.0',
                      'pycairo~=1.20.1', 'pydbus~=0.6.0', 'PyGObject~=3.42.0', 'pyserial~=3.5',
                      'python-json-logger~=2.0.2', 'requests~=2.26.0', 'sentry-sdk~=1.5.0', 'urllib3~=1.26.7',
                      'xxhash~=2.0.2', 'Yapsy~=1.12.2'],
    classifiers=['Environment :: X11 Applications :: GTK',
                 'Intended Audience :: Manufacturing',
                 'License :: Other/Proprietary License',
                 'Natural Language :: English',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 3.9',
                 'Topic :: System :: Hardware :: Universal Serial Bus (USB)',
                 'Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Hub',
                 'Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Mass Storage',
                 'Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Miscellaneous'],
)

if __name__ == "__main__":
    pass
