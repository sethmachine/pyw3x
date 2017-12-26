"""

"""

import collections
import json
import struct

import numpy

MAGIC_NUMBER = 'W3E!'

class Corner():
    def __init__(self):
        self.ground_height = None
        self.water_and_edge = None
        self.texture_and_flags = None
        self.variation = None
        self.misc = None

    def to_json(self):
        return vars(self)

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
        # add 1 because a map of 256 x 256 tiles will have 257 x 257 corners.
        for i in range(0, self.height):
            for j in range(0, self.width):
                corner = Corner()
                corner.ground_height = struct.unpack('h', filehandle.read(2))[0]
                corner.water_and_edge = struct.unpack('h', filehandle.read(2))[0]
                corner.texture_and_flags = struct.unpack('b', filehandle.read(1))[0]
                corner.variation = struct.unpack('b', filehandle.read(1))[0]
                corner.misc = struct.unpack('b', filehandle.read(1))[0]
                self.tiles[i][j] = corner.to_json()

    def write(self, outfile=None):
        if not outfile:
            outfile = self.file
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
                    corner = self.tiles[i][j]
                    f.write(struct.pack('h', corner['ground_height']))
                    f.write(struct.pack('h', corner['water_and_edge']))
                    f.write(struct.pack('b', corner['texture_and_flags']))
                    f.write(struct.pack('b', corner['variation']))
                    f.write(struct.pack('b', corner['misc']))
        return outfile


    def to_json(self):
        return vars(self)

    def describe(self):
        print(json.dumps(vars(self), indent=1))





if __name__ == '__main__':
    i = 'data/test/war3map.w3e' #extract using MPQExtractor
    t = Terrain(i)
    d = t.read()
    t.describe()
    t.write('data/test/foof.w3e')
    json.dump(t.to_json(), open('w3e.json', 'w'), indent=1)
