# Copyright 2018 The Emscripten Authors.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

import os
import logging
from tools import building

TAG = '2.0.2-em'
HASH = '2b96d17cc96439cbca0da313180c34dd302686d625a53efbbaf4ac3604fa7b5b374539799874b33645151a817c23f41f7b76db015d356bc3b19ef321aeff15ce'
REPO_NAME = 'fluidsynth-emscripten'

def get(ports, settings, shared):
  if settings.USE_FLUIDSYNTH != 1:
    return []

  ports.fetch_project('fluidsynth', 'https://github.com/mazmazz/fluidsynth-emscripten/archive/' + TAG + '.zip', REPO_NAME + '-' + TAG, sha512hash=HASH)

  def create():
    logging.info('building port: fluidsynth')
    ports.clear_project_build('fluidsynth')

    source_path = os.path.join(ports.get_dir(), 'fluidsynth', REPO_NAME + '-' + TAG)
    dest_path = os.path.join(ports.get_build_dir(), 'fluidsynth')
    target_path = os.path.join(dest_path, 'libfluidsynth.a')

    configure_args = [
      'cmake',
      '-G', 'Unix Makefiles',
      '-B' + dest_path,
      '-H' + source_path,
      '-DCMAKE_BUILD_TYPE=Release',
      '-DCMAKE_INSTALL_PREFIX=' + dest_path,
      '-Denable-static-emlib=on'
    ]

    building.configure(configure_args)
    building.make(['make', '-j%d' % building.get_num_cores(), '-C' + dest_path, 'install'])
    os.rename(os.path.join(dest_path, 'bin', 'libfluidsynth.a'), target_path)

    ports.install_header_dir(os.path.join(dest_path, 'include'))

    return target_path

  return [shared.Cache.get('libfluidsynth.a', create, what='port')]


def clear(ports, shared):
  shared.Cache.erase_file('libfluidsynth.a')


def process_dependencies(settings):
  pass


def process_args(ports, args, settings, shared):
  if settings.USE_FLUIDSYNTH == 1:
    get(ports, settings, shared)
    args += ['-I' + os.path.join(ports.get_build_dir(), 'fluidsynth', 'include')]
  return args


def show():
  return 'fluidsynth (USE_FLUIDSYNTH=1; LGPL license)'
