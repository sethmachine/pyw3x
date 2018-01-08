"""Script to manipulate terrain tiles with arbitrary callbacks.

"""

import collections
import json
import os
import shutil
import random

import archive
import terrain
import terrain_tiles
import wc3_runner

WC3_MAP_EXTENSION = '.w3x'
TERRAIN_FILE = 'war3map.w3e'
LIST_FILE = 'listfile.txt'

class Terrain_Manipulator():
    def __init__(self, basemap, outname, outdir):
        self.basemap = basemap
        self.outname = outname
        self.outdir = outdir
        self._make_outdir()
        self.outmap = os.path.join(outdir, outname + WC3_MAP_EXTENSION)
        self.listfile = os.path.join(outdir, LIST_FILE)
        self.w3e = os.path.join(outdir, TERRAIN_FILE)
        shutil.copyfile(self.basemap, self.outmap)

    def _make_outdir(self):
        if not os.path.exists(self.outdir):
            os.mkdir(self.outdir)

    def extract_assets(self):
        """Extracts terrain and list file.

        :return:
        """
        with archive.open_archive(self.outmap, 'r') as a:
            a.extract_terrain(self.w3e)
            a.extract_list_file(self.listfile)

    def mod_terrain(self, callback):
        """Applies the callback to the iteration of all available tiles.

        The callback should modify the tiles in place.

        :param callback:
        :return:
        """
        ter = terrain.Terrain(self.w3e)
        ter.read()
        new_tiles = terrain.tiles_to_terrain_tiles(ter.tiles)
        callback(new_tiles)
        new_corners = terrain.terrain_tiles_to_corners(new_tiles)
        ter.write(self.w3e, tiles=new_corners)

    def write_new_terrain(self):
        with archive.open_archive(self.outmap, 'w') as a:
            a.add_file(self.w3e, TERRAIN_FILE)
            if not a.compact(self.listfile):
                print('Failed to compact archive!')


def randomize_tile(tile):
    new_texture = random.randint(0, 15)
    new_variation = random.randint(0, 31)
    tile.ground_texture = new_texture
    tile.ground_variation = new_variation
    tile.cliff_texture = random.randint(0, 15)
    tile.cliff_variation = random.randint(0, 7)
    # tile.ground_height = random.randint(0, 8192 * 2)

def single_texture_closure(texture, variation):
    assert texture >= 0 and texture <= 15
    assert variation >= 0 and variation <= 31
    def func(tile):
        tile.ground_texture = texture
        tile.ground_variation = variation
    return func

def random_tile_textures(tiles):
    for tile in terrain.iter_tiles(tiles):
        randomize_tile(tile)

def tile_row_closure(starti, endi):
    def func(tiles):
        mx = 0
        counts = collections.defaultdict(int)
        for tile in terrain.iter_tiles(tiles):
            if tile.i >= starti and tile.i <= endi:
                print(tile.i)
                counts['=='] += 1
                randomize_tile(tile)
            elif tile.i > endi:
                counts['>'] += 1
            if tile.i > mx:
                mx = tile.i
        print('MAX i: {}'.format(mx))
        print(json.dumps(counts, indent=1))
    return func

def tile_column_closure(startj, endj):
    def func(tiles):
        mx = 0
        counts = collections.defaultdict(int)
        for tile in terrain.iter_tiles(tiles):
            if tile.j >= startj and tile.j <= endj:
                print(tile.j)
                counts['=='] += 1
                randomize_tile(tile)
            elif tile.j > endj:
                counts['>'] += 1
            if tile.j > mx:
                mx = tile.j
        print('MAX j: {}'.format(mx))
        print(json.dumps(counts, indent=1))
    return func

def tile_rectangle_closure(starti, endi, startj, endj, tile_callback):
    def func(tiles):
        for tile in terrain.iter_tiles(tiles):
            if tile.i >= starti and tile.i <= endi:
                if tile.j >= startj and tile.j <= endj:
                    tile_callback(tile)
    return func

if __name__ == '__main__':
    basemap = 'data/test/w3x/(2)GlacialThaw.w3x'
    basemap = 'data/test/w3x/(12)EmeraldGardens.w3x'
    tm = Terrain_Manipulator(basemap, 'foobar', 'foobar-out')
    tm.extract_assets()
    cb = random_tile_textures
    #1, 96 splits map in middle for 192 tiles aka 256 x 256
    cb = tile_column_closure(1, 96) #0 based will have odd number of rows with 192 tiles (0 - 192)
    cb = tile_rectangle_closure(80 + 30, 100 + 30, 80, 100, single_texture_closure(10, 10))
    tm.mod_terrain(callback=cb)
    tm.write_new_terrain()
    w = wc3_runner.Wc3_Runner()
    w.run_map(tm.outmap, 'terrain-mod')
