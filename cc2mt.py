import argparse
import math
import nbtlib
import numpy
import os
import requests
import shutil
import sqlite3
import zlib
from io import BytesIO
from nbtlib import parse_nbt, Path
from nbtlib.tag import String, List, Compound, IntArray, ByteArray
from numpy import int64
from os.path import exists
from PIL import Image
from zipfile import ZipFile

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def writeU8(os, u8):
    os.write(bytes((u8&0xff,)))

def writeU16(os, u16):
    os.write(bytes(((u16>>8)&0xff,)))
    os.write(bytes((u16&0xff,)))

def writeU32(os, u32):
    os.write(bytes(((u32>>24)&0xff,)))
    os.write(bytes(((u32>>16)&0xff,)))
    os.write(bytes(((u32>>8)&0xff,)))
    os.write(bytes((u32&0xff,)))

def writeString(os, s):
    b = bytes(s, "utf-8")
    writeU16(os, len(b))
    os.write(b)

def writeLongString(os, s):
    b = bytes(s, "utf-8")
    writeU32(os, len(b))
    os.write(b)

def bytesToInt(b):
    s = 0
    for x in b:
        s = (s<<8)+x
    return s

def getBlockAsInteger(Xval, Yval, Zval):
    return int64(Zval*16777216 + Yval*4096 + Xval)

def getclassicubeblock(blockposX, blockposZ, blockposY):
  global CC_BlockID
  CC_BlockID = 0
  if -1 < blockposX < CC_RealWorldSizeX:
    if blockposY < CC_RealWorldSizeY:
      if blockposZ < CC_RealWorldSizeZ:
        CC_BlockID = CC_Blocks_3D[blockposY][blockposZ][blockposX]

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

def GetTexture(TextureNumber, ExtraTransform):
    isAnimated = TextureAnim[TextureNumber][0]
    TextureFileName = TextureAnim[TextureNumber][1]
    TextureSize = TextureAnim[TextureNumber][2]
    Speed = TextureAnim[TextureNumber][3]
    Count = TextureAnim[TextureNumber][4]
    if isAnimated == False:
        return '"' + BlocksModName + str(TextureNumber) + '.png' + ExtraTransform + '"'
    if isAnimated == True:
        Speed = Speed*0.30
        return '{name = "' + str(TextureFileName) + '.png' + ExtraTransform + '",animation = {type = "vertical_frames",aspect_w = ' + str(TextureSize) + ',aspect_h = ' + str(TextureSize) + ',length = ' + str(Speed) + "}}"

def CCLoadMap(CCMapFile):
    global CC_Metadata
    global BlockDef
    global CC_WorldFileData
    CC_WorldFile = nbtlib.load(CCMapFile)
    CC_WorldFileData = CC_WorldFile['ClassicWorld'] 
    CC_Metadata = CC_WorldFileData['Metadata'] 

def ConvertBlocks(BlocksModName_input, fileworldname):
    global BlocksModName
    BlocksModName = BlocksModName_input
    global CC_Metadata
    BlockDef = [ [ None for y in range( 24 ) ]
                 for x in range( 768 ) ]
    # BlockUsed, BlockName, CollideType, Texture1, Texture2, Texture3, Texture4, Texture5, Texture6, TransmitsLight, WalkSound, FullBright, Shape, BlockDraw, FogR, FogG, FogB, FogDensity, Coords1, Coords2, Coords3, Coords4, Coords5, Coords6
    BlockDef[1] = [1, "Stone", 2, 1, 1, 1, 1, 1, 1, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[2] = [1, "Grass Block", 2, 0, 2, 3, 3, 3, 3, 0, 3, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[3] = [1, "Dirt", 2, 2, 2, 2, 2, 2, 2, 0, 3, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[4] = [1, "Cobblestone", 2, 16, 16, 16, 16, 16, 16, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[5] = [1, "Wood Planks", 2, 4, 4, 4, 4, 4, 4, 0, 1, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[6] = [1, "Sapling", 0, 15, 15, 15, 15, 15, 15, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[7] = [1, "Bedrock", 2, 17, 17, 17, 17, 17, 17, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[8] = [1, "Flowing Water", 5, 14, 14, 14, 14, 14, 14, 1, 0, 0, 16, 3, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[9] = [1, "Stationary Water", 5, 14, 14, 14, 14, 14, 14, 1, 0, 0, 16, 3, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[10] = [1, "Flowing Lava", 6, 30, 30, 30, 30, 30, 30, 1, 0, 1, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[11] = [1, "Stationary Lava", 6, 30, 30, 30, 30, 30, 30, 1, 0, 1, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[12] = [1, "Sand", 2, 18, 18, 18, 18, 18, 18, 0, 8, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[13] = [1, "Gravel", 2, 19, 19, 19, 19, 19, 19, 0, 8, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[14] = [1, "Gold Ore", 2, 32, 32, 32, 32, 32, 32, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[15] = [1, "Iron Ore", 2, 33, 33, 33, 33, 33, 33, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[16] = [1, "Coal Ore", 2, 34, 34, 34, 34, 34, 34, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[17] = [1, "Wood", 2, 21, 21, 20, 20, 20, 20, 0, 1, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[18] = [1, "Leaves", 2, 22, 22, 22, 22, 22, 22, 1, 3, 0, 16, 2, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[19] = [1, "Sponge", 2, 48, 48, 48, 48, 48, 48, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[20] = [1, "Glass", 2, 49, 49, 49, 49, 49, 49, 1, 6, 0, 16, 1, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[21] = [1, "Red Cloth", 2, 64, 64, 64, 64, 64, 64, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[22] = [1, "Orange Cloth", 2, 65, 65, 65, 65, 65, 65, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[23] = [1, "Yellow Cloth", 2, 66, 66, 66, 66, 66, 66, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[24] = [1, "Lime Cloth", 2, 67, 67, 67, 67, 67, 67, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[25] = [1, "Green Cloth", 2, 68, 68, 68, 68, 68, 68, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[26] = [1, "Aqua Green Cloth", 2, 69, 69, 69, 69, 69, 69, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[27] = [1, "Cyan Cloth", 2, 70, 70, 70, 70, 70, 70, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[28] = [1, "Blue Cloth", 2, 71, 71, 71, 71, 71, 71, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[29] = [1, "Purple Cloth", 2, 72, 72, 72, 72, 72, 72, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[30] = [1, "Indigo Cloth", 2, 73, 73, 73, 73, 73, 73, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[31] = [1, "Violet Cloth", 2, 74, 74, 74, 74, 74, 74, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[32] = [1, "Magenta Cloth", 2, 75, 75, 75, 75, 75, 75, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[33] = [1, "Pink Cloth", 2, 76, 76, 76, 76, 76, 76, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[34] = [1, "Black Cloth", 2, 77, 77, 77, 77, 77, 77, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[35] = [1, "Gray Cloth", 2, 78, 78, 78, 78, 78, 78, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[36] = [1, "White Cloth", 2, 79, 79, 79, 79, 79, 79, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[37] = [1, "Dandelion", 0, 13, 13, 13, 13, 13, 13, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[38] = [1, "Rose", 0, 12, 12, 12, 12, 12, 12, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[39] = [1, "Brown Mushroom", 0, 29, 29, 29, 29, 29, 29, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[40] = [1, "Red Mushroom", 0, 28, 28, 28, 28, 28, 28, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[41] = [1, "Block of Gold", 2, 24, 56, 40, 40, 40, 40, 0, 5, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[42] = [1, "Block of Iron", 2, 23, 55, 39, 39, 39, 39, 0, 5, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[43] = [1, "Double Slab", 2, 6, 6, 5, 5, 5, 5, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[44] = [1, "Slab", 2, 6, 6, 5, 5, 5, 5, 0, 4, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 16, 8, 16]
    BlockDef[45] = [1, "Brick", 2, 7, 7, 7, 7, 7, 7, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[46] = [1, "TNT", 2, 9, 10, 8, 8, 8, 8, 0, 8, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[47] = [1, "Bookshelf", 2, 4, 4, 35, 35, 35, 35, 0, 1, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[48] = [1, "Moss Stone", 2, 36, 36, 36, 36, 36, 36, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[49] = [1, "Obsidian", 2, 37, 37, 37, 37, 37, 37, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[50] = [1, "Cobblestone Slab", 2, 16, 16, 16, 16, 16, 16, 0, 4, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 16, 8, 16]
    BlockDef[51] = [1, "Rope", 7, 11, 11, 11, 11, 11, 11, 1, 7, 0, 16, 1, 0, 0, 0, 0, 6, 0, 6, 10, 16, 10]
    BlockDef[52] = [1, "Sandstone", 2, 25, 57, 41, 41, 41, 41, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[53] = [1, "Snow", 0, 50, 50, 50, 50, 50, 50, 1, 9, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 16, 2, 16]
    BlockDef[54] = [1, "Fire", 0, 38, 38, 38, 38, 38, 38, 1, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 2, 13, 11, 13]
    BlockDef[55] = [1, "Light Pink Cloth", 2, 80, 80, 80, 80, 80, 80, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[56] = [1, "Forest Green Cloth", 2, 81, 81, 81, 81, 81, 81, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[57] = [1, "Brown Cloth", 2, 82, 82, 82, 82, 82, 82, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[58] = [1, "Deep Blue Cloth", 2, 83, 83, 83, 83, 83, 83, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[59] = [1, "Turquoise Cloth", 2, 84, 84, 84, 84, 84, 84, 0, 7, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[60] = [1, "Ice", 2, 51, 51, 51, 51, 51, 51, 0, 6, 0, 16, 3, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[61] = [1, "Ceramic Tile", 2, 54, 54, 54, 54, 54, 54, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[62] = [1, "Magma", 2, 86, 86, 86, 86, 86, 86, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[63] = [1, "Pillar", 2, 26, 58, 42, 42, 42, 42, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[64] = [1, "Crate", 2, 53, 53, 53, 53, 53, 53, 0, 1, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    BlockDef[65] = [1, "Stone Brick", 2, 52, 52, 52, 52, 52, 52, 0, 4, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 16, 16, 16]
    
    if not os.path.isdir('./texture/'):
        os.makedirs('./texture/')

    if 'CPE' in CC_Metadata:
        CC_Metadata = CC_Metadata['CPE']
        print('ClassiCube2Minetest: Get BlockDefinitions')
        CC_BlockDefinitions = CC_Metadata['BlockDefinitions']

        for BlockNumber in range(1, 768):
            BlockDefHex = '{:04x}'.format(BlockNumber)
            BlockDefName = "Block" + BlockDefHex.upper()
            if BlockDefName in CC_BlockDefinitions:
                CC_Block = CC_BlockDefinitions[BlockDefName]
                ID = CC_Block["ID2"]
                BlockName = CC_Block["Name"]
                CollideType = int(CC_Block["CollideType"])
                TexturesFull = numpy.array(CC_Block['Textures'])
                Textures256_1 = TexturesFull[6] % 2**8 
                Textures256_2 = TexturesFull[7] % 2**8 
                Textures256_3 = TexturesFull[8] % 2**8 
                Textures256_4 = TexturesFull[9] % 2**8 
                Textures256_5 = TexturesFull[10] % 2**8 
                Textures256_6 = TexturesFull[11] % 2**8 
                TextureNum1 = TexturesFull[0] % 2**8 + Textures256_1 * 256
                TextureNum2 = TexturesFull[1] % 2**8 + Textures256_2 * 256
                TextureNum3 = TexturesFull[2] % 2**8 + Textures256_3 * 256
                TextureNum4 = TexturesFull[3] % 2**8 + Textures256_4 * 256
                TextureNum5 = TexturesFull[4] % 2**8 + Textures256_5 * 256
                TextureNum6 = TexturesFull[5] % 2**8 + Textures256_6 * 256
                TransmitsLight = CC_Block["TransmitsLight"]
                WalkSound = int(CC_Block["WalkSound"])
                FullBright = int(CC_Block["FullBright"])
                Shape = int(CC_Block["Shape"])
                BlockDraw = CC_Block["BlockDraw"]
                FogColor = numpy.array(CC_Block['Fog'])
                FogDensity = int(FogColor[0] % 2**8)
                FogR = int(FogColor[1] % 2**8)
                FogG = int(FogColor[2] % 2**8)
                FogB = int(FogColor[3] % 2**8)
                Coords = numpy.array(CC_Block["Coords"])
        
                BlockDef[BlockNumber][0] = 1
                BlockDef[BlockNumber][1] = str(BlockName)
                BlockDef[BlockNumber][2] = CollideType
                BlockDef[BlockNumber][3] = TextureNum1
                BlockDef[BlockNumber][4] = TextureNum2
                BlockDef[BlockNumber][5] = TextureNum3
                BlockDef[BlockNumber][6] = TextureNum4
                BlockDef[BlockNumber][7] = TextureNum5
                BlockDef[BlockNumber][8] = TextureNum6
                BlockDef[BlockNumber][9] = int(TransmitsLight)
                BlockDef[BlockNumber][10] = WalkSound
                BlockDef[BlockNumber][11] = FullBright
                BlockDef[BlockNumber][12] = Shape
                BlockDef[BlockNumber][13] = int(BlockDraw)
                BlockDef[BlockNumber][14] = FogR
                BlockDef[BlockNumber][15] = FogG
                BlockDef[BlockNumber][16] = FogB
                BlockDef[BlockNumber][17] = FogDensity
                BlockDef[BlockNumber][18] = Coords[0]
                BlockDef[BlockNumber][19] = Coords[1]
                BlockDef[BlockNumber][20] = Coords[2]
                BlockDef[BlockNumber][21] = Coords[3]
                BlockDef[BlockNumber][22] = Coords[4]
                BlockDef[BlockNumber][23] = Coords[5]

        CC_EnvMapAppearance = CC_Metadata['EnvMapAppearance']
        TextureURL = str(CC_EnvMapAppearance['TextureURL'])
        if TextureURL == '':
            TextureURL = "https://www.classicube.net/static/default.zip"
        print(TextureURL)
    else:  
        TextureURL = "https://www.classicube.net/static/default.zip"

    print('ClassiCube2Minetest: Texture: Download')
    downloadtexturefile = requests.get(TextureURL, allow_redirects=True)
    open('./texture/texturefile', 'wb').write(downloadtexturefile.content)

    texturefile = open("./texture/texturefile", "rb")
    texturefilefirstbytes = texturefile.read(4)
    texfolder = "./texture/zip"

    if texturefilefirstbytes == b'PK\x03\x04':
        print('ClassiCube2Minetest: Texture: Download: ZIP File')
        if not os.path.isdir('./texture/zip'):
            os.makedirs('./texture/zip')
        with ZipFile('./texture/texturefile', 'r') as zipObj:
            zipObj.extractall(path='./texture/zip')
        if not os.path.exists('./texture/zip/terrain.png'):
            subfolders = [ f.path for f in os.scandir('./texture/zip') if f.is_dir() ]
            texfolder = subfolders[0]
            print(texfolder)
    
    if texturefilefirstbytes == b'\x89PNG':
        print('ClassiCube2Minetest: Texture: Download: PNG File')
        os.makedirs('./texture/zip/')
        os.rename("./texture/texturefile", "./texture/zip/terrain.png")
    
    if not os.path.isdir('./texture/res'):
        os.makedirs('./texture/res')
    shutil.copyfile(texfolder + '/terrain.png', './texture/res/terrain.png')
    if os.path.isfile(texfolder + '/skybox.png'):
       shutil.copyfile(texfolder + '/skybox.png', './texture/res/skybox.png')

    # ---------------------------- Crop Textures ----------------------------
    print('ClassiCube2Minetest: Texture: Seperate')
    
    BlockTextureImage = Image.open(r"./texture/res/terrain.png")
    BlockTextureX, BlockTextureY = BlockTextureImage.size
    BlockSize = int(BlockTextureX / 16)
    CurrentBlockX = 1
    CurrentBlockY = 1
    MaxBlockX = BlockTextureX / BlockSize
    MaxBlockY = BlockTextureY / BlockSize
    BlockNumber = 0
    
    if not os.path.isdir('./' + fileworldname + '/'):
            os.makedirs('./' + fileworldname + '/')
    
    if not os.path.isdir('./' + fileworldname + '/worldmods/' + BlocksModName):
            os.makedirs('./' + fileworldname + '/worldmods/' + BlocksModName)
    
    if not os.path.isdir('./' + fileworldname + '/worldmods/' + BlocksModName + '/textures/'):
            os.makedirs('./' + fileworldname + '/worldmods/' + BlocksModName + '/textures/')
    
    while CurrentBlockY <= MaxBlockY:
        #print(str(BlockNumber) + " " + str(CurrentBlockX) + " " + str(CurrentBlockY))
        BlockCropRealX = CurrentBlockX-1
        BlockCropRealY = CurrentBlockY-1
        BlockCropX = BlockCropRealX*BlockSize
        BlockCropY = BlockCropRealY*BlockSize
        BlockImage = BlockTextureImage.crop((BlockCropX, BlockCropY, BlockCropX+BlockSize, BlockCropY+BlockSize))
        BlockImage.save('./' + fileworldname + '/worldmods/' + BlocksModName + '/textures/' + BlocksModName + str(BlockNumber) + '.png')
        BlockNumber = BlockNumber + 1
        CurrentBlockX = CurrentBlockX + 1
        if CurrentBlockX > 16:
            CurrentBlockY = CurrentBlockY + 1
            CurrentBlockX = 1

    dependsfile = open("./" + fileworldname + "/worldmods/" + str(BlocksModName) + "/depends.txt", "w")
    dependsfile.write('default')
    dependsfile.close()

    # Animated, TextureName, Size, Speed
    global TextureAnim
    TextureAnim = [ [ None for y in range( 5 ) ] for x in range( 512 ) ]
    for TextureNumber in range(0, 512):
        TextureAnim[TextureNumber] = [False, BlocksModName + str(TextureNumber), None, None, 1]

    if os.path.isfile(texfolder + '/animations.png'):
        TextureImageAnim = Image.open(texfolder + "/animations.png")
        with open(texfolder + "/animations.txt") as animationsfile :
            for line in animationsfile:
                AnimParams = line. rstrip('\n').split(' ')
                if '#' not in AnimParams[0] and len(AnimParams) == 7:
                    AnimTileX = int(AnimParams[0])
                    AnimTileY = int(AnimParams[1])
                    AnimFrameX = int(AnimParams[2])
                    AnimFrameY = int(AnimParams[3])
                    AnimFrameSize = int(AnimParams[4])
                    AnimFramesCount = int(AnimParams[5])
                    AnimTickDelay = int(AnimParams[6])
                    TextureXYOut = AnimTileX + AnimTileY*16
                    TextureAnim[TextureXYOut] = [True, BlocksModName + str(TextureXYOut) + '_anim', AnimFrameSize,AnimTickDelay,AnimFramesCount]
        
                    AnimFrames = Image.new("RGBA", (AnimFrameSize, AnimFrameSize*AnimFramesCount), (255, 255, 255, 0))
                    for AnimFrameCount in range(0, AnimFramesCount):
                        TextureImageFrame = TextureImageAnim.crop((AnimFrameX + AnimFrameCount*AnimFrameSize, AnimFrameY,       AnimFrameX+ AnimFrameSize + AnimFrameCount*AnimFrameSize, AnimFrameY + AnimFrameSize))
                        AnimFrames.paste(TextureImageFrame, (0, AnimFrameCount*AnimFrameSize))
                    AnimFrames.save('./' + fileworldname + '/worldmods/' + BlocksModName + '/textures/' + BlocksModName + str(TextureXYOut) + '_anim.png', "PNG")

    # ---------------------------- Convert Blocks ----------------------------
    print('ClassiCube2Minetest: Minetest Mod: Convert Blocks')

    if not os.path.isdir('./' + fileworldname + '/worldmods/'):
            os.makedirs('./' + fileworldname + '/worldmods/')
 
    if not os.path.isdir('./' + fileworldname + '/worldmods/' + BlocksModName):
            os.makedirs('./' + fileworldname + '/worldmods/' + BlocksModName)

    initfile = open("./" + fileworldname + "/worldmods/" + BlocksModName + "/init.lua", "w")
    for BlockNumber in range(0, 768):
        BlockUsed = BlockDef[BlockNumber][0]
        if BlockUsed == 1:
            BlockName = BlockDef[BlockNumber][1]
            CollideType = BlockDef[BlockNumber][2]
            TextureNum1 = BlockDef[BlockNumber][3]
            TextureNum2 = BlockDef[BlockNumber][4]
            TextureNum3 = BlockDef[BlockNumber][5]
            TextureNum4 = BlockDef[BlockNumber][6]
            TextureNum5 = BlockDef[BlockNumber][7]
            TextureNum6 = BlockDef[BlockNumber][8]
            TransmitsLight = BlockDef[BlockNumber][9]
            WalkSound = BlockDef[BlockNumber][10]
            FullBright = BlockDef[BlockNumber][11]
            Shape = BlockDef[BlockNumber][12]
            BlockDraw = BlockDef[BlockNumber][13]
            FogR = BlockDef[BlockNumber][14]
            FogG = BlockDef[BlockNumber][15]
            FogB = BlockDef[BlockNumber][16]
            FogDensity = BlockDef[BlockNumber][17]
            Coords1 = BlockDef[BlockNumber][18]
            Coords2 = BlockDef[BlockNumber][19]
            Coords3 = BlockDef[BlockNumber][20]
            Coords4 = BlockDef[BlockNumber][21]
            Coords5 = BlockDef[BlockNumber][22]
            Coords6 = BlockDef[BlockNumber][23]
            CoordsTable = [Coords1, Coords2, Coords3, Coords4, Coords5, Coords6]
            FogHex = rgb_to_hex((FogR, FogG, FogB))
            
            MinX = float(Coords1)
            MinY = float(Coords2)
            MinZ = float(Coords3)
            MaxX = float(Coords4)
            MaxY = float(Coords5)
            MaxZ = float(Coords6)
            
            MinX = MinX / 16
            MinY = MinY / 16
            MinZ = MinZ / 16
            MaxX = MaxX / 16
            MaxY = MaxY / 16
            MaxZ = MaxZ / 16
            
            MinX = MinX - 0.5
            MinY = MinY - 0.5
            MinZ = MinZ - 0.5
            MaxX = MaxX - 0.5
            MaxY = MaxY - 0.5
            MaxZ = MaxZ - 0.5
            
            MinX = MinX * -1
            MaxX = MaxX * -1
            
            initfile.write('minetest.register_node("' + str(BlocksModName) + ':' + str(BlockNumber) + '", {\n')
            initfile.write('\tdescription =  "' + str(BlocksModName) + ' ' + str(BlockName) + '",\n')
            initfile.write('\tinventory_image = minetest.inventorycube("' + BlocksModName + str(TextureNum1) + '.png", "' + BlocksModName + str(TextureNum4) + '.png", "' + BlocksModName + str(TextureNum5) + '.png"),\n')

            CanBePointed = "false"
            CanBeDug = "false"
            if BlockDraw != 4:
                if Shape != 0:
                    if Coords1 == Coords2 == Coords3 == 0 and Coords4 == Coords5 == Coords6 == 16:
                        if BlockDraw == 0: # fully opaque
                            initfile.write('\tdrawtype = "normal",\n')
                        if BlockDraw == 1: # transparent (e.g. like glass)
                            initfile.write('\tdrawtype = "nodebox",\n')
                            initfile.write('\tnode_box = {\n')
                            initfile.write('\t\ttype = "fixed",\n')
                            initfile.write('\t\tfixed = {' + str(MinX) + ", " + str(MinY) + ", " + str(MinZ) + ", " + str(MaxX) + ", " + str(MaxY) + ", " + str(MaxZ) + '},\n')
                            initfile.write('\t},\n')
                        if BlockDraw == 2: # transparent but with no face culling of same neighbours (e.g. like leaves)
                            initfile.write('\tdrawtype = "nodebox",\n')
                            initfile.write('\tnode_box = {\n')
                            initfile.write('\t\ttype = "fixed",\n')
                            initfile.write('\t\tfixed = {' + str(MinX) + ", " + str(MinY) + ", " + str(MinZ) + ", " + str(MaxX) + ", " + str(MaxY) + ", " + str(MaxZ) + '},\n')
                            initfile.write('\t},\n')
                        if BlockDraw == 3: # translucent, where texture's alpha is blended (e.g. like ice or water)
                            initfile.write('\tdrawtype = "liquid",\n')
                    else:
                        initfile.write('\tdrawtype = "nodebox",\n')
                        initfile.write('\tnode_box = {\n')
                        initfile.write('\t\ttype = "fixed",\n')
                        initfile.write('\t\tfixed = {' + str(MinX) + ", " + str(MinY) + ", " + str(MinZ) + ", " + str(MaxX) + ", " + str(MaxY) + ", " + str(MaxZ) + '},\n')
                        initfile.write('\t},\n')
                else:
                    initfile.write('\tdrawtype = "plantlike",\n')
                    CanBePointed = "true"
                    CanBeDug = "true"
            else:
                initfile.write('\tdrawtype = "airlike",\n')
            
            if Shape != 0:
                if (BlockName.find('#') == -1):
                    initfile.write('\ttiles = {' + GetTexture(TextureNum1, '^[transformr180') + ', ' + GetTexture(TextureNum2, '') + ', ' + GetTexture(TextureNum3, '') + ', ' + GetTexture(TextureNum4, '') + ', ' + GetTexture(TextureNum6, '') + ', ' + GetTexture(TextureNum5, '') + '},\n')
                else:
                    tintedblock = '^[multiply:#' + str(FogHex)
                    initfile.write('\ttiles = {' + GetTexture(TextureNum1, '^[transformr180' + tintedblock) + ', ' + GetTexture(TextureNum2, tintedblock) + ', ' + GetTexture(TextureNum3, tintedblock) + ', ' + GetTexture(TextureNum4, tintedblock) + ', ' + GetTexture(TextureNum6, tintedblock) + ', ' + GetTexture(TextureNum5, tintedblock) + '},\n')
            else:
                initfile.write('\ttiles = {' + GetTexture(TextureNum3, '') + '},\n')
            
            initfile.write('\tparamtype = "light",\n')


            if CollideType == 2 or CollideType == 3 or CollideType == 4:
                initfile.write('\twalkable = true,\n')
                CanBePointed = "true"
                CanBeDug = "true"
                initfile.write('\tbuildable_to = false,\n')

            if CollideType == 1:
                initfile.write('\twalkable = false,\n')
                CanBePointed = "true"
                CanBeDug = "true"
                initfile.write('\tclimbable = true,\n')
            
            if CollideType == 0 or CollideType == 1 or CollideType == 5 or CollideType == 6:
                initfile.write('\twalkable = false,\n')
                initfile.write('\tbuildable_to = true,\n')
            
            if CollideType == 7:
                initfile.write('\twalkable = false,\n')
                CanBePointed = "true"
                CanBeDug = "true"
                initfile.write('\tbuildable_to = false,\n')
                initfile.write('\tclimbable = true,\n')

            if CollideType == 0:
                CanBePointed = "true"
                CanBeDug = "true"

            initfile.write('\tpointable = ' + CanBePointed + ',\n')
            initfile.write('\tdiggable = ' + CanBeDug + ',\n')
            initfile.write('\tis_ground_content = false,\n')
            
            if FullBright == 1:
                initfile.write('\tlight_source = 14,\n')
            
            initfile.write('\tuse_texture_alpha = "blend",\n')
            initfile.write('\tdrop = "",\n')
            
            initfile.write('\tpost_effect_color = {a=' + str(FogDensity * 0.8) + ', r=' + str(FogR) + ', g=' + str(FogG) + ', b=' + str(FogB) + '},\n')
    
            
            if WalkSound == 1:
                initfile.write('\tsounds = default.node_sound_wood_defaults(),\n')
            
            if WalkSound == 2:
                initfile.write('\tsounds = default.node_sound_gravel_defaults(),\n')
            
            if WalkSound == 3:
                initfile.write('\tsounds = default.node_sound_leaves_defaults(),\n')
            
            if WalkSound == 4:
                initfile.write('\tsounds = default.node_sound_stone_defaults(),\n')
            
            if WalkSound == 5:
                initfile.write('\tsounds = default.node_sound_metal_defaults(),\n')
            
            if WalkSound == 6:
                initfile.write('\tsounds = default.node_sound_glass_defaults(),\n')
            
            if WalkSound == 8:
                initfile.write('\tsounds = default.node_sound_sand_defaults(),\n')
            
            if WalkSound == 9:
                initfile.write('\tsounds = default.node_sound_snow_defaults(),\n')
            
            #if CollideType == 5 or CollideType == 6:
            #        initfile.write('\tdrowning = 4,\n')
            #        initfile.write('\tliquidtype = "source",\n')
            #        initfile.write('\tliquid_viscosity = 1,\n')
            
            if Shape != 0:
                if CollideType == 0 or CollideType == 2 or CollideType == 3 or CollideType == 4 or CollideType == 7:
                    initfile.write('\tgroups = {cracky = 3, oddly_breakable_by_hand = 3},\n')
                if CollideType == 5:
                    initfile.write('\tgroups = {water = 3, liquid = 3, puts_out_fire = 1},\n')
                if CollideType == 6:
                    initfile.write('\tgroups = {liquid = 2},\n')
                if CollideType == 3:
                    initfile.write('\tgroups = {cracky = 3, oddly_breakable_by_hand = 3, slippery = 3},\n')
                if CollideType == 4:
                    initfile.write('\tgroups = {cracky = 3, oddly_breakable_by_hand = 3, slippery = 5},\n')
            else:
                initfile.write('\tgroups = {cracky = 3, oddly_breakable_by_hand = 3},\n')
            initfile.write('})\n')
    initfile.close()

def ConvertEnv(WorldName, fileworldname):
    print('ClassiCube2Minetest: Minetest Mod: Convert Env')

    CC_EnvColors = CC_Metadata['EnvColors']
    CC_SkyColors = CC_EnvColors['Sky']
    CC_CloudColors = CC_EnvColors['Cloud']
    
    SkyColor_R = int(CC_SkyColors['R'])
    SkyColor_G = int(CC_SkyColors['G'])
    SkyColor_B = int(CC_SkyColors['B'])
    CloudColor_R = int(CC_CloudColors['R'])
    CloudColor_G = int(CC_CloudColors['G'])
    CloudColor_B = int(CC_CloudColors['B'])

    if not os.path.isdir('./' + fileworldname + '/worldmods/'):
            os.makedirs('./' + fileworldname + '/worldmods/')
 
    if not os.path.isdir('./' + fileworldname + '/worldmods/' + WorldName):
            os.makedirs('./' + fileworldname + '/worldmods/' + WorldName)

    if not os.path.isdir('./' + fileworldname + '/worldmods/' + WorldName + '/textures/'):
            os.makedirs('./' + fileworldname + '/worldmods/' + WorldName + '/textures/')

    initfile = open("./" + fileworldname + "/worldmods/" + WorldName + "/init.lua", "w")
    initfile.write('minetest.register_on_joinplayer(function(player)\n')
    
    if os.path.isfile('./texture/res/skybox.png'):
        skyboximage = Image.open(r"./texture/res/skybox.png")
        skyboxsize_x, skyboxsize_y = skyboximage.size
        skyboxsize4 = skyboxsize_x / 4
        skyboxpart = skyboximage.crop((skyboxsize4*1, skyboxsize4*0, skyboxsize4*2, 0+skyboxsize4))
        skyboxpart.save('./' + fileworldname + '/worldmods/' + str(WorldName) + '/textures/skybox1.png')
        skyboxpart = skyboximage.crop((skyboxsize4*2, skyboxsize4*0, skyboxsize4*3, 0+skyboxsize4))
        skyboxpart.save('./' + fileworldname + '/worldmods/' + str(WorldName) + '/textures/skybox2.png')
        skyboxpart = skyboximage.crop((skyboxsize4*0, skyboxsize4*1, skyboxsize4*1, skyboxsize4*2))
        skyboxpart.save('./' + fileworldname + '/worldmods/' + str(WorldName) + '/textures/skybox3.png')
        skyboxpart = skyboximage.crop((skyboxsize4*1, skyboxsize4*1, skyboxsize4*2, skyboxsize4*2))
        skyboxpart.save('./' + fileworldname + '/worldmods/' + str(WorldName) + '/textures/skybox4.png')
        skyboxpart = skyboximage.crop((skyboxsize4*2, skyboxsize4*1, skyboxsize4*3, skyboxsize4*2))
        skyboxpart.save('./' + fileworldname + '/worldmods/' + str(WorldName) + '/textures/skybox5.png')
        skyboxpart = skyboximage.crop((skyboxsize4*3, skyboxsize4*1, skyboxsize4*4, skyboxsize4*2))
        skyboxpart.save('./' + fileworldname + '/worldmods/' + str(WorldName) + '/textures/skybox6.png')
    
        initfile.write('\tplayer:override_day_night_ratio(1)\n')
        initfile.write('\tplayer:set_sky({\n')
        initfile.write('\t\ttype = "skybox",\n')
        initfile.write('\t\ttextures = {"skybox1.png^[transformR90", "skybox2.png^[transformFXR90", "skybox3.png", "skybox5.png", "skybox4.png", "skybox6.png^[transformR90"},\n')
        initfile.write('\t\tclouds = false\n')
        initfile.write('\t})\n')
        initfile.write('\tplayer:set_sun({visible = false, sunrise_visible = false})\n')
        initfile.write('\tplayer:set_moon({visible = false})\n')
        initfile.write('\tplayer:set_stars({visible = false})\n')
    else:
        if SkyColor_R!=153 and SkyColor_G!=204 and SkyColor_B!=255:
            initfile.write('\tplayer:set_sky({r=' + str(SkyColor_R) + ', g=' + str(SkyColor_G) + ', b=' + str(SkyColor_B) + '}, "plain", {})\n')
    
    initfile.write('\tplayer:set_clouds({\n')
    initfile.write('\t\tcolor = {r=' + str(CloudColor_R) + ', g=' + str(CloudColor_G) + ', b=' + str(CloudColor_B) + '}\n')
    initfile.write('\t})\n')
    initfile.write('end)\n')
    initfile.close() #This close() is important

def ConvertWorld(BlocksModName, fileworldname, MTChunkPosX, MTChunkPosY, MTChunkPosZ, IsTest):
    global CC_RealWorldSizeX
    global CC_RealWorldSizeY
    global CC_RealWorldSizeZ
    global CC_Blocks_3D
    CC_RealWorldSizeX = int(CC_WorldFileData['X'])
    CC_RealWorldSizeY = int(CC_WorldFileData['Y'])
    CC_RealWorldSizeZ = int(CC_WorldFileData['Z'])

    if 'BlockArray2' in CC_WorldFileData:
      CC_Blocks = numpy.array(CC_WorldFileData['BlockArray']) % 2**8 + numpy.array(CC_WorldFileData['BlockArray2']) * 256
    else:
      CC_Blocks = numpy.array(CC_WorldFileData['BlockArray']) % 2**8
    CC_Blocks_3D = CC_Blocks.reshape((CC_RealWorldSizeY,CC_RealWorldSizeZ,CC_RealWorldSizeX))
    print('World Size:' + str(CC_RealWorldSizeX) + ' ' + str(CC_RealWorldSizeY) + ' ' + str(CC_RealWorldSizeZ))
    
    MT_WorldSizeX = int(round_down(CC_RealWorldSizeX / 16))
    MT_WorldSizeY = int(round_down(CC_RealWorldSizeY / 16))
    MT_WorldSizeZ = int(round_down(CC_RealWorldSizeZ / 16))
    
    MT_CurrentChunkX = 0
    MT_CurrentChunkY = 0
    MT_CurrentChunkZ = 0
    MT_RealCurrentChunkX = 0
    ConversionComplete = 0
    
    mapsqlfile = sqlite3.connect("./" + fileworldname + "/map.sqlite")
    mapsqlfilecur = mapsqlfile.cursor()
    mapsqlfilecur.execute("CREATE TABLE IF NOT EXISTS `blocks` (\
    `pos` INT NOT NULL PRIMARY KEY, `data` BLOB);")
    
    while ConversionComplete == 0:
      print(str(MT_CurrentChunkX) + ' ' + str(MT_CurrentChunkY) + ' ' + str(MT_CurrentChunkZ) + ' / ' + str(MT_WorldSizeX) + ' ' + str(MT_WorldSizeY) + ' ' + str(MT_WorldSizeZ))
    
      mapblockdata = BytesIO()  
      writeU8(mapblockdata, 24)  
        
      flags = 0x00  
      flags |= 0x02  
      writeU8(mapblockdata, flags)  
      writeU8(mapblockdata, 2) # content_width  
      writeU8(mapblockdata, 2) # params_width  
        
      # Bulk node data  
      zlibnodedata = BytesIO()  
        
      CC_X_BlockPosition = 0  
      CC_Y_BlockPosition = 0  
      CC_Z_BlockPosition = 0  
        
      MT_BlocksList = []  
        
      while CC_Z_BlockPosition <= 15:  
    
          CC_X_RealBlockPosition = CC_X_BlockPosition*-1 + 15
          CCMT_X_BlockPosition = CC_X_RealBlockPosition + MT_CurrentChunkX * 16
          CCMT_Y_BlockPosition = CC_Y_BlockPosition + MT_CurrentChunkY * 16
          CCMT_Z_BlockPosition = CC_Z_BlockPosition + MT_CurrentChunkZ * 16
          global CC_BlockID
          if IsTest == True:  
            CC_BlockID = 1
          else:
            getclassicubeblock(CCMT_X_BlockPosition, CCMT_Z_BlockPosition, CCMT_Y_BlockPosition)  
          # print(str(CCMT_X_BlockPosition) + ' ' + str(CCMT_Y_BlockPosition) + ' ' + str(CCMT_Z_BlockPosition) + ' ' + str(CC_BlockID))  
          MT_BlocksList.append(CC_BlockID)  
          if 15 == CC_X_BlockPosition:  
            CC_X_BlockPosition = 0  
            if 15 == CC_Y_BlockPosition:  
              CC_Y_BlockPosition = 0  
              if 16 != CC_Z_BlockPosition:  
                CC_Z_BlockPosition = CC_Z_BlockPosition + 1  
            else:  
              CC_Y_BlockPosition = CC_Y_BlockPosition + 1  
          else:  
            CC_X_BlockPosition = CC_X_BlockPosition + 1  
          writeU16(zlibnodedata, CC_BlockID)
    
      ByteRepeat = 1  
      while ByteRepeat <= 4096:  
          ByteRepeat += 1  
          writeU8(zlibnodedata, 15)  
        
      ByteRepeat = 1  
      while ByteRepeat <= 4096:  
          ByteRepeat += 1  
          writeU8(zlibnodedata, 0)  
        
      mapblockdata.write(zlib.compress(zlibnodedata.getvalue()))  
    
      zlibmetadata = BytesIO()  
      writeU8(zlibmetadata, 1)  
      mapblockdata.write(zlib.compress(zlibmetadata.getvalue()))  
           
      writeU8(mapblockdata, 0) #nodetimer_version
      
      # Static objects  
      writeU8(mapblockdata, 0) # Version  
      writeU16(mapblockdata, 0) # Number of objects  
        
      # Timestamp  
      writeU32(mapblockdata, 0x0000027a) # BLOCK_TIMESTAMP_UNDEFINED  
        
      MT_UsedBlocksList = []  
        
      for word in MT_BlocksList:  
          if word not in MT_UsedBlocksList:  
              MT_UsedBlocksList.append(word)  
        
      # Name-ID mapping  
      writeU8(mapblockdata, 0) # Version  
      writeU16(mapblockdata, len(MT_UsedBlocksList))  
        
      for i in range(len(MT_UsedBlocksList)):  
          BlockName = str(BlocksModName) + ":" + str(MT_UsedBlocksList[i])  
          if BlockName == str(BlocksModName) + ":0":  
              BlockName = 'air'  
          writeU16(mapblockdata, MT_UsedBlocksList[i])  
          #print(BlockName)  
          writeString(mapblockdata, BlockName)
    
      MT_RealCurrentChunkX = MT_CurrentChunkX*-1 + MT_WorldSizeX
      MT_Pos = getBlockAsInteger(MT_RealCurrentChunkX+MTChunkPosX, MT_CurrentChunkY+MTChunkPosY, MT_CurrentChunkZ+MTChunkPosZ)
      mapsqlfilecur.execute("INSERT INTO blocks VALUES (?,?)", (int(MT_Pos), mapblockdata.getvalue()))
      if MT_WorldSizeX <= MT_CurrentChunkX:
        MT_CurrentChunkX = 0
        if MT_WorldSizeY <= MT_CurrentChunkY:
          MT_CurrentChunkY = 0
          if MT_WorldSizeZ <= MT_CurrentChunkZ:
            ConversionComplete = 1
          else:
            MT_CurrentChunkZ = MT_CurrentChunkZ + 1
        else:
          MT_CurrentChunkY = MT_CurrentChunkY + 1
      else:
        MT_CurrentChunkX = MT_CurrentChunkX + 1
      
    mapsqlfile.commit()
    mapsqlfile.close()


def GetSpawnData():
    return [CC_WorldFileData['Spawn'], CC_RealWorldSizeX]

def MT_MakePlayersFile(fileworldname, ccX, ccY, ccZ, ccWX):
    CC_WorldSpawn = CC_WorldFileData['Spawn']
    CC_SpawnX = int(ccX)
    CC_SpawnY = int(ccY)
    CC_SpawnZ = int(ccZ)
    
    MT_SpawnX = CC_SpawnX * -1 + ccWX
    
    playersfile = sqlite3.connect("./" + fileworldname + "/players.sqlite")
    playersfile_cur = playersfile.cursor()
    
    playersfile_cur.execute("CREATE TABLE `player` (`name` VARCHAR(50) NOT NULL,`pitch` NUMERIC(11, 4) NOT NULL,`yaw` NUMERIC(11, 4) NOT NULL,`posX` NUMERIC(11, 4) NOT NULL,`posY` NUMERIC(11, 4) NOT NULL,`posZ` NUMERIC(11, 4) NOT NULL,`hp` INT NOT NULL,`breath` INT NOT NULL,`creation_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,`modification_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (`name`))")
    playersfile_cur.execute("CREATE TABLE `player_inventories` (   `player` VARCHAR(50) NOT NULL, `inv_id` INT NOT NULL,  `inv_width` INT NOT NULL, `inv_name` TEXT NOT NULL DEFAULT '',  `inv_size` INT NOT NULL,  PRIMARY KEY(player, inv_id),   FOREIGN KEY (`player`) REFERENCES player (`name`) ON DELETE CASCADE )")
    
    playersfile_cur.execute('INSERT INTO player_inventories VALUES ("singleplayer", 0, 0, "main", 32)')
    playersfile_cur.execute('INSERT INTO player_inventories VALUES ("singleplayer", 1, 0, "craft", 9)')
    playersfile_cur.execute('INSERT INTO player_inventories VALUES ("singleplayer", 2, 0, "craftpreview", 1)')
    playersfile_cur.execute('INSERT INTO player_inventories VALUES ("singleplayer", 3, 0, "craftresult", 1)')
    
    playersfile_cur.execute("CREATE TABLE `player_inventory_items` (   `player` VARCHAR(50) NOT NULL, `inv_id` INT NOT NULL,  `slot_id` INT NOT NULL, `item` TEXT NOT NULL DEFAULT '',  PRIMARY KEY(player, inv_id, slot_id),   FOREIGN KEY (`player`) REFERENCES player (`name`) ON DELETE CASCADE )")
    
    for x in range(0, 32):
        playersfile_cur.execute('INSERT INTO player_inventory_items VALUES ("singleplayer", 0, ' + str(x) + ', " ")')
    
    for x in range(0, 9):
        playersfile_cur.execute('INSERT INTO player_inventory_items VALUES ("singleplayer", 1, ' + str(x) + ', " ")')
    
    playersfile_cur.execute('INSERT INTO player_inventory_items VALUES ("singleplayer", 2, 0, "")')
    playersfile_cur.execute('INSERT INTO player_inventory_items VALUES ("singleplayer", 3, 0, "")')
    
    playersfile_cur.execute("CREATE TABLE `player_metadata` (    `player` VARCHAR(50) NOT NULL,    `metadata` VARCHAR(256) NOT NULL,    `value` TEXT,    PRIMARY KEY(`player`, `metadata`),    FOREIGN KEY (`player`) REFERENCES player (`name`) ON DELETE CASCADE )")
    
    spawncmd = 'INSERT INTO player VALUES ("singleplayer", 60, 0, ' + str(MT_SpawnX * 10) + ', ' + str(CC_SpawnY * 10) + ', ' + str(CC_SpawnZ * 10) + ', ' + '16, 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)'
    
    playersfile_cur.execute(spawncmd)
    
    playersfile.commit()
    playersfile.close()

def MT_Final(WorldName, fileworldname):
    worldmtfile = open("./" + fileworldname + "/world.mt", "w")
    worldmtfile.write('enable_damage = true\n')
    worldmtfile.write('creative_mode = true\n')
    worldmtfile.write('auth_backend = sqlite3\n')
    worldmtfile.write('player_backend = sqlite3\n')
    worldmtfile.write('backend = sqlite3\n')
    worldmtfile.write('gameid = minetest\n')
    worldmtfile.write('world_name = ' + str(fileworldname) + '\n')
    worldmtfile.write('server_announce = false\n')
    worldmtfile.close()
    
    mapmetafile = open("./" + fileworldname + "/map_meta.txt", "w")
    mapmetafile.write('mg_flags = caves, dungeons, light, decorations, biomes, ores\n')
    mapmetafile.write('chunksize = 5\n')
    mapmetafile.write('mapgen_limit = 31000\n')
    mapmetafile.write('water_level = 1\n')
    mapmetafile.write('seed = 0\n')
    mapmetafile.write('mg_name = singlenode\n')
    mapmetafile.write('[end_of_params]\n')
    mapmetafile.close()
    
