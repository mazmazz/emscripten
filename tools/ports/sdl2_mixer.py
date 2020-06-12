# Copyright 2016 The Emscripten Authors.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

import os
import shutil
import logging

TAG = 'release-2.0.2'
HASH = 'b9d03061d177f20f4e03f3e3553afd7bfe0c05da7b9a774312b389318e747cf9724e0475e9afff6a64ce31bab0217e2afb2619d75556753fbbb6ecafa9775219'


def get(ports, settings, shared):
  if settings.USE_SDL_MIXER != 2:
    return []

  sdl_build = os.path.join(ports.get_build_dir(), 'sdl2')
  assert os.path.exists(sdl_build), 'You must use SDL2 to use SDL2_mixer'
  ports.fetch_project('sdl2_mixer', 'https://github.com/emscripten-ports/SDL2_mixer/archive/' + TAG + '.zip', 'SDL2_mixer-' + TAG, sha512hash=HASH)
  libname = ports.get_lib_name('libSDL2_mixer')

  def create():
    logging.info('building port: sdl2_mixer')

    source_path = os.path.join(ports.get_dir(), 'sdl2_mixer', 'SDL2_mixer-' + TAG)
    dest_path = os.path.join(shared.Cache.get_path('ports-builds'), 'sdl2_mixer')

    shutil.rmtree(dest_path, ignore_errors=True)
    shutil.copytree(source_path, dest_path)

    flags = ['-DMUSIC_OGG', '-O2', '-s', 'USE_VORBIS=1', '-s', 'USE_SDL=2']
    exclude_files = ['music_mad', 'music_mpg123', 'music_smpeg',
                     'music_cmd', 'music_flac', 
                     'music_nativemidi', 'music_timidity',
                     'music_mikmod', 'music_modplug',
                     'playmus.c', 'playwave.c']

    if settings.USE_FLUIDSYNTH:
      flags.extend(['-DMUSIC_MID_FLUIDSYNTH', '-s', 'USE_FLUIDSYNTH=1'])
    else:
      exclude_files.append('music_fluidsynth')

    final = os.path.join(dest_path, libname)
    ports.build_port(dest_path, final, [], flags, exclude_files,
                     ['external', 'native_midi', 'timidity'])

    # copy header to a location so it can be used as 'SDL2/'
    ports.install_headers(source_path, pattern='SDL_*.h', target='SDL2')
    return final

  return [shared.Cache.get(libname, create, what='port')]


def clear(ports, shared):
  shared.Cache.erase_file(ports.get_lib_name('libSDL2_mixer'))


def process_dependencies(settings):
  if settings.USE_SDL_MIXER == 2:
    settings.USE_SDL = 2
    settings.USE_VORBIS = 1


def process_args(ports, args, settings, shared):
  if settings.USE_SDL_MIXER == 2:
    get(ports, settings, shared)
  return args


def show():
  return 'SDL2_mixer (USE_SDL_MIXER=2; zlib license)'
