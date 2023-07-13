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

import configparser
from bs4 import BeautifulSoup
import os.path
from pathlib import Path
from subprocess import Popen
import requests.auth
import requests
import sys

__homedir__ = os.path.expanduser('~')
__pypi__ = __homedir__ + "/.pypirc"
__root_dir__ = str(Path(__file__).parent.absolute())


def main() -> int:
    try:
        if Path(__pypi__).is_file:
            os.system("py3clean {}".format(__root_dir__))
            username = get_config_setting("username")
            password = get_config_setting("password")
            repository = get_config_setting("repository") + "packages/"
            post = get_latest_post(username, password, repository)
            Popen("py3clean .", stdout=sys.stdout, stderr=sys.stderr, shell=True).communicate()
            Popen("rm -rf build && rm -rf dist && rm -rf *.egg-info", stdout=sys.stdout,
                  stderr=sys.stderr, shell=True).communicate()
            Popen("python3.9 setup.py --post {} sdist bdist_wheel --universal upload -r dev".format(post),
                  stdout=sys.stdout, stderr=sys.stderr, shell=True).communicate()
            Popen("py3clean .", stdout=sys.stdout, stderr=sys.stderr, shell=True).communicate()
            Popen("rm -rf build && rm -rf dist && rm -rf *.egg-info", stdout=sys.stdout,
                  stderr=sys.stderr, shell=True).communicate()
        else:
            print("Error: Could not find {}".format(__pypi__))
            print("Error: Visit https://help.ezduplicator.com to download pypirc")
            return 1
    except Exception as ex:
        print("Exception: {}".format(ex))
        return 1
    return 0


def get_latest_post(username, password, repository) -> int:
    url = repository
    html = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password)).content
    soup = BeautifulSoup(html, 'html.parser')
    whl = soup.find_all('a')[-1].text
    post = whl.split('-')
    post = post[1]
    post = post.split('.')
    if len(post) <= 3:
        return 1
    post = post[3]
    post = post.replace('post', '')
    return int(post) + 1


def get_config_setting(setting) -> str:
    try:
        config = configparser.ConfigParser(interpolation=None)
        config.read(__pypi__)
        if config.has_option('dev', setting):
            return config['dev'][setting]
        else:
            raise Exception("Key {} not found in {}!".format(setting, __pypi__))
    except Exception as ex:
        raise Exception(ex)


if __name__ == '__main__':
    mainret = main()
    sys.exit(mainret)
