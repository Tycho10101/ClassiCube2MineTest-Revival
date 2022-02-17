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

parser = argparse.ArgumentParser()
parser.add_argument("mapname")
parser.add_argument("ClassicWorld")

args = parser.parse_args()

MapName = args.mapname
ClassicWorld = args.ClassicWorld

CC_WorldFile = nbtlib.load(ClassicWorld)
CC_WorldFileData = CC_WorldFile['ClassicWorld'] 

CC_Metadata = CC_WorldFileData['Metadata'] 
CC_Metadata = CC_Metadata['CPE']

# ---------------------------- Store Classicube BlockDefinitions ----------------------------
 
print('ClassiCube2Minetest: Get BlockDefinitions')
CC_BlockDefinitions = CC_Metadata['BlockDefinitions']

# BlockName, CollideType, Texture1, Texture2, Texture3, Texture4, Texture5, Texture6, TransmitsLight, WalkSound, FullBright, Shape, BlockDraw, FogR, FogG, FogB, FogDensity, Coords1, Coords2, Coords3, Coords4, Coords5, Coords6
BlockDef = [ [ None for y in range( 23 ) ]
             for x in range( 767 ) ]

for BlockNumber in range(0, 767):
    BlockDefHex = '{:04x}'.format(BlockNumber)
    BlockDefName = "Block" + BlockDefHex.upper()
    print(BlockDefName)
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

        BlockDef[BlockNumber][0] = str(BlockName)
        BlockDef[BlockNumber][1] = CollideType
        BlockDef[BlockNumber][2] = TextureNum1
        BlockDef[BlockNumber][3] = TextureNum2
        BlockDef[BlockNumber][4] = TextureNum3
        BlockDef[BlockNumber][5] = TextureNum4
        BlockDef[BlockNumber][6] = TextureNum5
        BlockDef[BlockNumber][7] = TextureNum6
        BlockDef[BlockNumber][8] = int(TransmitsLight)
        BlockDef[BlockNumber][9] = WalkSound
        BlockDef[BlockNumber][10] = FullBright
        BlockDef[BlockNumber][11] = Shape
        BlockDef[BlockNumber][12] = int(BlockDraw)
        BlockDef[BlockNumber][13] = FogR
        BlockDef[BlockNumber][14] = FogG
        BlockDef[BlockNumber][15] = FogB
        BlockDef[BlockNumber][16] = FogDensity
        BlockDef[BlockNumber][17] = Coords[0]
        BlockDef[BlockNumber][18] = Coords[1]
        BlockDef[BlockNumber][19] = Coords[2]
        BlockDef[BlockNumber][20] = Coords[3]
        BlockDef[BlockNumber][21] = Coords[4]
        BlockDef[BlockNumber][22] = Coords[5]

# ---------------------------- Download and Extract Texture ----------------------------

print('ClassiCube2Minetest: Texture: Download')
CC_EnvMapAppearance = CC_Metadata['EnvMapAppearance']
TextureURL = str(CC_EnvMapAppearance['TextureURL'])

if not os.path.isdir('./texture/'):
   os.makedirs('./texture/')

downloadtexturefile = requests.get(TextureURL, allow_redirects=True)
open('./texture/texturefile', 'wb').write(downloadtexturefile.content)

texturefile = open("./texture/texturefile", "rb")
texturefilefirstbytes = texturefile.read(4)

if texturefilefirstbytes == b'PK\x03\x04':
    print('ClassiCube2Minetest: Texture: Download: ZIP File')
    if not os.path.isdir('./texture/zip'):
        os.makedirs('./texture/zip')
    with ZipFile('./texture/texturefile', 'r') as zipObj:
        zipObj.extractall(path='./texture/zip')

if texturefilefirstbytes == b'\x89PNG':
    print('ClassiCube2Minetest: Texture: Download: PNG File')

if not os.path.isdir('./texture/res'):
    os.makedirs('./texture/res')
shutil.copyfile('./texture/zip/terrain.png', './texture/res/terrain.png')
if os.path.isfile('./texture/zip/skybox.png'):
   shutil.copyfile('./texture/zip/skybox.png', './texture/res/skybox.png')


# ---------------------------- Crop Textures ----------------------------

print('ClassiCube2Minetest: Texture: Seperate')

terrainimage = Image.open(r"./texture/res/terrain.png")

blocktexture_width, blocktexture_height = terrainimage.size

BlockSize = blocktexture_width / 16
BlockSizeX = blocktexture_width / 16
BlockSizeY = blocktexture_height / 16

CurrentBlockX = 1
CurrentBlockY = 1

BlockNumber = 0

if not os.path.isdir('./output/'):
        os.makedirs('./output/')

if not os.path.isdir('./output/worldmods/' + MapName):
        os.makedirs('./output/worldmods/' + MapName)

if not os.path.isdir('./output/worldmods/' + MapName + '/textures/'):
        os.makedirs('./output/worldmods/' + MapName + '/textures/')

while CurrentBlockY <= BlockSizeY:  
    PixelCropX = CurrentBlockX * BlockSize
    PixelCropX = PixelCropX - BlockSize
    PixelCropY = CurrentBlockY * BlockSize
    PixelCropY = PixelCropY - BlockSize
    blockimage = terrainimage.crop((PixelCropX, PixelCropY, PixelCropX+BlockSize, PixelCropY+BlockSize))
    blockimage.save('./output/worldmods/' + MapName + '/textures/' + str(BlockNumber) + '.png')
    BlockNumber = BlockNumber + 1
    CurrentBlockX = CurrentBlockX + 1
    if CurrentBlockX > BlockSizeX:
        CurrentBlockY = CurrentBlockY + 1
        CurrentBlockX = 1

# ---------------------------- Classicube Blocks to Minetest Mod ----------------------------

CC_EnvColors = CC_Metadata['EnvColors']
CC_SkyColors = CC_EnvColors['Sky']
CC_CloudColors = CC_EnvColors['Cloud']

SkyColor_R = int(CC_SkyColors['R'])
SkyColor_G = int(CC_SkyColors['G'])
SkyColor_B = int(CC_SkyColors['B'])
CloudColor_R = int(CC_CloudColors['R'])
CloudColor_G = int(CC_CloudColors['G'])
CloudColor_B = int(CC_CloudColors['B'])

print('ClassiCube2Minetest: Minetest Mod')
if not os.path.isdir('./output/worldmods/'):
        os.makedirs('./output/worldmods/')

initfile = open("output/worldmods/" + MapName + "/init.lua", "w")



initfile.write('minetest.register_on_joinplayer(function(player)\n')

if os.path.isfile('./texture/res/skybox.png'):
    skyboximage = Image.open(r"./texture/res/skybox.png")
    skyboxsize_x, skyboxsize_y = skyboximage.size
    skyboxsize4 = skyboxsize_x / 4
    skyboxpart = skyboximage.crop((skyboxsize4*1, skyboxsize4*0, skyboxsize4*2, 0+skyboxsize4))
    skyboxpart.save('./output/worldmods/' + str(MapName) + '/textures/skybox1.png')
    skyboxpart = skyboximage.crop((skyboxsize4*2, skyboxsize4*0, skyboxsize4*3, 0+skyboxsize4))
    skyboxpart.save('./output/worldmods/' + str(MapName) + '/textures/skybox2.png')
    skyboxpart = skyboximage.crop((skyboxsize4*0, skyboxsize4*1, skyboxsize4*1, skyboxsize4*2))
    skyboxpart.save('./output/worldmods/' + str(MapName) + '/textures/skybox3.png')
    skyboxpart = skyboximage.crop((skyboxsize4*1, skyboxsize4*1, skyboxsize4*2, skyboxsize4*2))
    skyboxpart.save('./output/worldmods/' + str(MapName) + '/textures/skybox4.png')
    skyboxpart = skyboximage.crop((skyboxsize4*2, skyboxsize4*1, skyboxsize4*3, skyboxsize4*2))
    skyboxpart.save('./output/worldmods/' + str(MapName) + '/textures/skybox5.png')
    skyboxpart = skyboximage.crop((skyboxsize4*3, skyboxsize4*1, skyboxsize4*4, skyboxsize4*2))
    skyboxpart.save('./output/worldmods/' + str(MapName) + '/textures/skybox6.png')


    initfile.write('\tplayer:set_sky({\n')
    initfile.write('\t\ttype = "skybox",\n')
    initfile.write('\t\ttextures = {"skybox1.png", "skybox2.png^[transformR180", "skybox4.png", "skybox6.png^[transformR180", "skybox3.png^[transformR180", "skybox5.png^[transformR180"},\n')
    initfile.write('\t\tclouds = false\n')
    initfile.write('\t})\n')
    initfile.write('\tplayer:set_sun({visible = false, sunrise_visible = false})\n')
    initfile.write('\tplayer:set_moon({visible = false})\n')
    initfile.write('\tplayer:set_stars({visible = false})\n')
else:
    initfile.write('\tplayer:set_sky({r=' + str(SkyColor_R) + ', g=' + str(SkyColor_G) + ', b=' + str(SkyColor_B) + '}, "plain", {})\n')

initfile.write('\tplayer:set_clouds({\n')
initfile.write('\t\tcolor = {r=' + str(CloudColor_R) + ', g=' + str(CloudColor_G) + ', b=' + str(CloudColor_B) + '}\n')
initfile.write('\t})\n')
initfile.write('end)\n')

for BlockNumber in range(0, 767):
    BlockName = BlockDef[BlockNumber][0]
    if(BlockName is not None):
        CollideType = BlockDef[BlockNumber][1]
        TextureNum1 = BlockDef[BlockNumber][2]
        TextureNum2 = BlockDef[BlockNumber][3]
        TextureNum3 = BlockDef[BlockNumber][4]
        TextureNum4 = BlockDef[BlockNumber][5]
        TextureNum5 = BlockDef[BlockNumber][6]
        TextureNum6 = BlockDef[BlockNumber][7]
        TransmitsLight = BlockDef[BlockNumber][8]
        WalkSound = BlockDef[BlockNumber][9]
        FullBright = BlockDef[BlockNumber][10]
        Shape = BlockDef[BlockNumber][11]
        BlockDraw = BlockDef[BlockNumber][12]
        FogR = BlockDef[BlockNumber][13]
        FogG = BlockDef[BlockNumber][14]
        FogB = BlockDef[BlockNumber][15]
        FogDensity = BlockDef[BlockNumber][16]
        Coords1 = BlockDef[BlockNumber][17]
        Coords2 = BlockDef[BlockNumber][18]
        Coords3 = BlockDef[BlockNumber][19]
        Coords4 = BlockDef[BlockNumber][20]
        Coords5 = BlockDef[BlockNumber][21]
        Coords6 = BlockDef[BlockNumber][22]
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
        
        initfile.write('minetest.register_node("' + str(MapName) + ':' + str(BlockNumber) + '", {\n')
        initfile.write('\tdescription =  "' + str(MapName) + ' ' + str(BlockName) + '",\n')
        initfile.write('\tinventory_image = minetest.inventorycube("' + str(TextureNum1) + '.png", "' + str(TextureNum2) + '.png", "' + str(TextureNum3) + '.png"),\n')
        
        if BlockDraw != 4:
            if Shape != 0:
                if CollideType == 0:
                    initfile.write('\tdrawtype = "nodebox",\n')
                if CollideType == 1:
                    initfile.write('\tdrawtype = "nodebox",\n')
                if CollideType == 2:
                    initfile.write('\tdrawtype = "nodebox",\n')
                if CollideType == 3:
                    initfile.write('\tdrawtype = "nodebox",\n')
                if CollideType == 7:
                    initfile.write('\tdrawtype = "nodebox",\n')
                if CollideType == 4:
                    initfile.write('\tdrawtype = "nodebox",\n')
                if CollideType == 5:
                    initfile.write('\tdrawtype = "nodebox",\n')
            else:
                initfile.write('\tdrawtype = "plantlike",\n')
        else:
            initfile.write('\tdrawtype = "airlike",\n')
        
        if Shape != 0:
            if (BlockName.find('#\n') == -1):
                initfile.write('\ttiles = { "' + str(TextureNum1) + '.png^[transformr180", "' + str(TextureNum2) + '.png", "' + str(TextureNum3) + '.png", "' + str(TextureNum4) + '.png", "' + str(TextureNum6) + '.png", "' + str(TextureNum5) + '.png" },\n')
            else:
                initfile.write('\ttiles = { "' + str(TextureNum1) + '.png^[multiply:#' + str(FogHex) + '^[transformr180", "' + str(TextureNum2) + '.png^[multiply:#' + str(FogHex) + '", "' + str(TextureNum3) + '.png^[multiply:#' + str(FogHex) + '", "' + str(TextureNum4) + '.png^[multiply:#' + str(FogHex) + '", "' + str(TextureNum6) + '.png^[multiply:#' + str(FogHex) + '", "' + str(TextureNum5) + '.png^[multiply:#' + str(FogHex) + 'D0" },\n')
        else:
            initfile.write('\ttiles = { "' + str(TextureNum1) + '.png" },\n')
        
        initfile.write('\tparamtype = "light",\n')
        
        if CollideType == 2 or CollideType == 3 or CollideType == 4:
            initfile.write('\twalkable = true,\n')
            initfile.write('\tpointable = true,\n')
            initfile.write('\tdiggable = true,\n')
            initfile.write('\tbuildable_to = false,\n')
        
        if CollideType == 1:
            initfile.write('\twalkable = false,\n')
            initfile.write('\tpointable = true,\n')
            initfile.write('\tdiggable = true,\n')
            initfile.write('\tbuildable_to = true,\n')
            initfile.write('\tclimbable = true,\n')
        
        if CollideType == 0 or CollideType == 1 or CollideType == 5 or CollideType == 6:
            initfile.write('\twalkable = false,\n')
            initfile.write('\tpointable = false,\n')
            initfile.write('\tdiggable = false,\n')
            initfile.write('\tbuildable_to = true,\n')
        
        if CollideType == 7:
            initfile.write('\twalkable = false,\n')
            initfile.write('\tpointable = true,\n')
            initfile.write('\tdiggable = true,\n')
            initfile.write('\tbuildable_to = false,\n')
            initfile.write('\tclimbable = true,\n')
        
        initfile.write('\tis_ground_content = false,\n')
        
        if FullBright == 1:
            initfile.write('\tlight_source = 14,\n')
        
        initfile.write('\tuse_texture_alpha = "clip",\n')
        initfile.write('\tdrop = "",\n')
        
        if FogR != 0:
            if FogG != 0:
                if FogB != 0:
                    initfile.write('\tpost_effect_color = {a=' + str(FogDensity) + ', r=' + str(FogR) + ', g=' + str(FogG) + ', b=' + str(FogB) + '},\n')
        initfile.write('\tnode_box = {\n')
        initfile.write('\t\ttype = "fixed",\n')
        initfile.write('\t\tfixed = {' + str(MinX) + ", " + str(MinY) + ", " + str(MinZ) + ", " + str(MaxX) + ", " + str(MaxY) + ", " + str(MaxZ) + '},\n')
        initfile.write('\t},\n')
        
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
        
        if CollideType == 5 or CollideType == 6:
                initfile.write('\tdrowning = 1,\n')
                initfile.write('\tliquidtype = "source",\n')
                initfile.write('\tliquid_viscosity = 1,\n')
        
        if Shape != 0:
            if CollideType == 0 or CollideType == 2 or CollideType == 3 or CollideType == 4 or CollideType == 7:
                initfile.write('\tgroups = {cracky = 3, oddly_breakable_by_hand = 3},\n')
            if CollideType == 5:
                initfile.write('\tgroups = {water = 3, liquid = 3, puts_out_fire = 1},\n')
            if CollideType == 6:
                initfile.write('\tgroups = {liquid = 2},\n')
        else:
            initfile.write('\tgroups = {cracky = 3, oddly_breakable_by_hand = 3},\n')
        initfile.write('})\n')

initfile.close() #This close() is important

# ---------------------------- Classicube Map to Minetest World ----------------------------

print('ClassiCube2Minetest: World Conversion')

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
  if blockposX < CC_RealWorldSizeX:
    if blockposY < CC_RealWorldSizeY:
      if blockposZ < CC_RealWorldSizeZ:
        CC_BlockID = CC_Blocks_3D[blockposY][blockposZ][blockposX]

CC_RealWorldSizeX = int(CC_WorldFileData['X'])
CC_RealWorldSizeY = int(CC_WorldFileData['Y'])
CC_RealWorldSizeZ = int(CC_WorldFileData['Z'])

CC_WorldSizeX = CC_RealWorldSizeX - 1
CC_WorldSizeY = CC_RealWorldSizeY - 1
CC_WorldSizeZ = CC_RealWorldSizeZ - 1


if 'BlockArray2' in CC_WorldFileData:
  CC_Blocks = numpy.array(CC_WorldFileData['BlockArray']) % 2**8 + numpy.array(CC_WorldFileData['BlockArray2']) * 256
else:
  CC_Blocks = numpy.array(CC_WorldFileData['BlockArray']) % 2**8



CC_Blocks_3D = CC_Blocks.reshape((CC_RealWorldSizeY,CC_RealWorldSizeZ,CC_RealWorldSizeX))

print(str(CC_RealWorldSizeX) + ' ' + str(CC_RealWorldSizeY) + ' ' + str(CC_RealWorldSizeZ))

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

MT_WorldSizeX = int(round_down(CC_RealWorldSizeX / 16)) - 1
MT_WorldSizeY = int(round_down(CC_RealWorldSizeY / 16)) - 1
MT_WorldSizeZ = int(round_down(CC_RealWorldSizeZ / 16)) - 1

MT_HalfWorldSizeY = int(round_down(CC_RealWorldSizeY / 2))

MT_CurrentChunkX = 0
MT_CurrentChunkY = 0
MT_CurrentChunkZ = 0
MT_RealCurrentChunkX = 0

ConversionComplete = 0

CC_WorldSpawn = CC_WorldFileData['Spawn']
CC_SpawnX = int(CC_WorldSpawn['X'])
CC_SpawnY = int(CC_WorldSpawn['Y'])
CC_SpawnZ = int(CC_WorldSpawn['Z'])

MT_SpawnX = CC_SpawnX * -1 + CC_WorldSizeX

playersfile = sqlite3.connect("./output/players.sqlite")
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

mapsqlfile = sqlite3.connect("./output/map.sqlite")
mapsqlfilecur = mapsqlfile.cursor()

mapsqlfilecur.execute("CREATE TABLE IF NOT EXISTS `blocks` (\
`pos` INT NOT NULL PRIMARY KEY, `data` BLOB);")

while ConversionComplete == 0:
  print(str(MT_CurrentChunkX) + ' ' + str(MT_CurrentChunkY) + ' ' + str(MT_CurrentChunkZ))



      
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

      # if CC_X_BlockPosition > 14:  
      #     CC_X_BlockPosition = -1  
      #     CC_Y_BlockPosition += 1  
      #     if CC_Y_BlockPosition > 15:  
      #       CC_Y_BlockPosition = 0  
      #         CC_Z_BlockPosition += 1  
      # CC_X_BlockPosition += 1
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
      BlockName = str(MapName) + ":" + str(MT_UsedBlocksList[i])  
      if BlockName == str(MapName) + ":0":  
          BlockName = 'air'  
      writeU16(mapblockdata, MT_UsedBlocksList[i])  
      print(BlockName)  
      writeString(mapblockdata, BlockName)


  MT_RealCurrentChunkX = MT_CurrentChunkX*-1 + MT_WorldSizeX
  MT_Pos = getBlockAsInteger(MT_RealCurrentChunkX, MT_CurrentChunkY, MT_CurrentChunkZ)
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

worldmtfile = open("output/world.mt", "w")
worldmtfile.write('enable_damage = true\n')
worldmtfile.write('creative_mode = true\n')
worldmtfile.write('auth_backend = sqlite3\n')
worldmtfile.write('player_backend = sqlite3\n')
worldmtfile.write('backend = sqlite3\n')
worldmtfile.write('gameid = minetest\n')
worldmtfile.write('world_name = ' + str(MapName) + '\n')
worldmtfile.write('server_announce = false\n')
worldmtfile.close()

mapmetafile = open("output/map_meta.txt", "w")
mapmetafile.write('mg_flags = caves, dungeons, light, decorations, biomes, ores\n')
mapmetafile.write('chunksize = 5\n')
mapmetafile.write('mapgen_limit = 31000\n')
mapmetafile.write('water_level = 1\n')
mapmetafile.write('seed = 0\n')
mapmetafile.write('mg_name = singlenode\n')
mapmetafile.write('[end_of_params]\n')
mapmetafile.close()

dependsfile = open("output/worldmods/" + str(MapName) + "/depends.txt", "w")
dependsfile.write('default')
dependsfile.close()