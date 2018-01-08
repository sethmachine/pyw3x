"""

"""

import collections
import json
import struct

import terrain_tiles

MAGIC_NUMBER = 'W3E!'

def iter_tiles(tiles):
    outer = list(tiles.keys())
    outer.sort()
    for i in outer:
        inner = list(tiles.keys())
        inner.sort()
        for j in outer:
            yield tiles[i][j]

def iter_tiles_keys(tiles):
    outer = list(tiles.keys())
    outer.sort()
    for i in outer:
        inner = list(tiles.keys())
        inner.sort()
        for j in outer:
            yield i, j, tiles[i][j]

CORNER_W3E_DATA = ['ground_height', 'water_and_edge', 'texture_and_flags', 'variation', 'misc']

class Corner():
    def __init__(self):
        self.ground_height = None
        self.water_and_edge = None
        self.texture_and_flags = None
        self.variation = None
        self.misc = None
        self.water_height = None
        self.map_edge = None
        self.ground_texture = None
        self.ramp = None
        self.blight = None
        self.water = None
        self.boundary = None
        self.ground_variation = None
        self.cliff_variation = None
        self.cliff_texture = None
        self.layer_height = None

    def parse_water_and_edge(self):
        self.water_height = self.water_and_edge & 0x3FFF
        # take last two bits and store these...
        self.map_edge = '{:016b}'.format(self.water_and_edge)[:2]
        # self.map_edge = self.water_and_edge & 0xC000

    def parse_texture_and_flags(self):
        self.ground_texture = self.texture_and_flags & 0x0F
        flags = self.texture_and_flags & 0xF0
        self.ramp = flags & 0X0010
        self.blight = flags & 0x0020
        self.water = flags & 0x0040
        self.boundary = flags & 0x4000

    def parse_variation(self):
        self.ground_variation = self.variation & 31
        self.cliff_variation = (self.variation & 224) >> 5

    def parse_misc(self):
        self.cliff_texture = (self.misc & 0xF0) >> 4
        self.layer_height = self.misc & 0x0F

    def parse(self):
        self.parse_water_and_edge()
        self.parse_texture_and_flags()
        self.parse_variation()
        self.parse_misc()

    def to_json(self):
        data = vars(self)
        out = collections.OrderedDict()
        for key in data:
            if key in CORNER_W3E_DATA:
                out[key] = data[key]
        return out

    def to_data(self, outfile):
        return vars(self)

    def __repr__(self):
        return json.dumps(vars(self), indent=1)

class Terrain():
    def __init__(self, infile):
        self.file = infile
        self.magic_number = None
        self.version = None
        self.tileset = None
        self.custom_tileset = None
        self.num_ground_textures = None
        self.ground_textures = None
        self.num_cliff_textures = None
        self.cliff_textures = None
        self.width = None
        self.height = None
        self.horizontal_offset = None
        self.vertical_offset = None
        self.tiles = None
        self.corners = None
        
    def read(self):
        with open(self.file, 'rb') as f:
            magic_number = f.read(4).decode('utf-8') #4 bytes (=4 chars)
            assert magic_number == MAGIC_NUMBER
            self.magic_number = magic_number
            self.version = struct.unpack('I', f.read(4))[0] # 4 bytes unsigned 32 bit int
            self.tileset = struct.unpack('c', f.read(1))[0].decode('utf-8') #1 byte char
            # o for no, 1 for custom
            self.custom_tileset = struct.unpack('I', f.read(4))[0] #1 byte boolean
            self.num_ground_textures = struct.unpack('I', f.read(4))[0]
            self.ground_textures = []
            for i in range(0, self.num_ground_textures):
                val = f.read(4).decode('utf-8')
                self.ground_textures.append(val)
            self.num_cliff_textures = struct.unpack('I', f.read(4))[0]
            self.cliff_textures = []
            for i in range(0, self.num_cliff_textures):
                val = f.read(4).decode('utf-8')
                self.cliff_textures.append(val)
            self.width = struct.unpack('I', f.read(4))[0]
            self.height = struct.unpack('I', f.read(4))[0]
            # 2 offsets are used in the scripts files, doodads and more.
            self.horizontal_offset = struct.unpack('f', f.read(4))[0]
            self.vertical_offset = struct.unpack('f', f.read(4))[0]
            self._read_tilepoints(f)
            assert len(f.read()) == 0 #no data left to read

    def _read_tilepoints(self, filehandle):
        self.tiles = collections.defaultdict(lambda: collections.defaultdict(dict))
        self.corners = collections.defaultdict(lambda: collections.defaultdict(dict))
        # add 1 because a map of 256 x 256 tiles will have 257 x 257 corners.
        for i in range(0, self.height):
            for j in range(0, self.width):
                corner = Corner()
                corner.ground_height = struct.unpack('H', filehandle.read(2))[0]
                corner.water_and_edge = struct.unpack('H', filehandle.read(2))[0]
                corner.texture_and_flags = struct.unpack('B', filehandle.read(1))[0]
                corner.variation = struct.unpack('B', filehandle.read(1))[0]
                corner.misc = struct.unpack('B', filehandle.read(1))[0]
                corner.parse()
                self.corners[i][j] = corner.to_json()
                self.tiles[i][j] = corner

    def write(self, outfile=None, tiles=None):
        if not outfile:
            outfile = self.file
        if not tiles:
            tiles = self.corners
        with open(outfile, 'wb') as f:
            f.write(self.magic_number.encode())
            f.write(struct.pack('I', self.version))
            f.write(struct.pack('c', self.tileset.encode()))
            f.write(struct.pack('I', self.custom_tileset))
            f.write(struct.pack('I', self.num_ground_textures))
            for texture in self.ground_textures:
                f.write(texture.encode())
            f.write(struct.pack('I', self.num_cliff_textures))
            for texture in self.cliff_textures:
                f.write(texture.encode())
            f.write(struct.pack('I', self.width))
            f.write(struct.pack('I', self.height))
            f.write(struct.pack('f', self.horizontal_offset))
            f.write(struct.pack('f', self.vertical_offset))
            for i in range(0, self.height):
                for j in range(0, self.width):
                    corner = tiles[i][j]
                    f.write(struct.pack('H', corner['ground_height']))
                    f.write(struct.pack('H', corner['water_and_edge']))
                    f.write(struct.pack('B', corner['texture_and_flags']))
                    f.write(struct.pack('B', corner['variation']))
                    f.write(struct.pack('B', corner['misc']))
        return outfile


    def to_json(self):
        data = vars(self)
        out = collections.OrderedDict()
        for key in data:
            if key != 'tiles':
                out[key] = data[key]
        return out

    def describe(self):
        data = self.to_json()
        print(json.dumps(data, indent=1))


def test_read_write():
    i = 'data/test/war3map.w3e' #extract using MPQExtractor
    t = Terrain(i)
    d = t.read()
    t.describe()
    t.write('data/test/bar.w3e')
    json.dump(t.to_json(), open('data/test/w3e.json', 'w'), indent=1)
    y = iter_tiles(t.tiles)
    d = [vars(x) for x in y]
    json.dump(d, open('data/test/tiles.json', 'w'), indent=1)

def tiles_to_terrain_tiles(tiles):
    import terrain_tiles
    out = collections.defaultdict(lambda: collections.defaultdict(dict))
    for i, j, tile in iter_tiles_keys(tiles):
        new_tile = terrain_tiles.Tile()
        new_tile.i = i
        new_tile.j = j
        new_tile.unpack(tile.ground_height, tile.water_and_edge, tile.texture_and_flags,
                        tile.variation, tile.misc)
        out[i][j] = new_tile
    return out

def terrain_tiles_to_corners(tiles):
    out = collections.defaultdict(lambda: collections.defaultdict(dict))
    for i, j, tile in iter_tiles_keys(tiles):
        new_corner = tile.pack()
        out[i][j] = new_corner
    return out


if __name__ == '__main__':
    # i = 'data/test/war3map.w3e' #extract using MPQExtractor
    # t = Terrain(i)
    # t.read()
    import os
    import shutil
    import random

    import archive
    import terrain_tiles
    i = 'data/test/w3x/(2)GlacialThaw.w3x'
    copyi = 'data/test/GlacialCopy3.w3x'
    if os.path.exists(copyi):
        shutil.copyfile(i, copyi)
    listfile = 'data/test/glacial-list.txt'
    with archive.open_archive(copyi, 'r') as a:
        a.extract_terrain('data/test/glacial.w3e')
        a.extract_list_file(listfile)
    t = Terrain('data/test/glacial.w3e')
    t.read()
    y = iter_tiles(t.tiles)
    d = [vars(x) for x in y]
    json.dump(d, open('data/test/glacial-tiles.json', 'w'), indent=1)
    json.dump(t.to_json(), open('data/test/glacial.w3e.json', 'w'), indent=1)
    new_tiles = tiles_to_terrain_tiles(t.tiles)
    #iterate tiles and randomize textures/variations
    for tile in iter_tiles(new_tiles):
        new_texture = random.randint(0, 15)
        new_variation = random.randint(0, 31)
        tile.ground_texture = new_texture
        tile.ground_variation = new_variation
        tile.cliff_texture = random.randint(0, 15)
        tile.cliff_variation = random.randint(0, 7)
        # tile.ground_height = random.randint(0, 8192 * 2)
        # tile.ground_height = 8192
        # tile.layer_height = 10
    new_corners = terrain_tiles_to_corners(new_tiles)
    t.write('data/test/glacial-mod2.w3e', tiles=new_corners)
    with archive.open_archive(copyi, 'w') as a:
        a.add_file('data/test/glacial-mod2.w3e', 'war3map.w3e')
        a.extract_all_files('glacial-mod', listfile)
        if not a.compact(listfile):
            print('Failed to compact')
    import wc3_runner
    w = wc3_runner.Wc3_Runner()
    w.run_map(copyi, 'foobar', replace_existing=True)

