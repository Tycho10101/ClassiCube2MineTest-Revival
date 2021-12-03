import nbtlib
import math
import numpy
from nbtlib import parse_nbt, Path
from nbtlib.tag import String, List, Compound, IntArray, ByteArray
from numpy import int64
from io import BytesIO
import zlib
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("mapname")
parser.add_argument("ClassicWorld")

args = parser.parse_args()

MapName = args.mapname
ClassicWorld = args.ClassicWorld

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

CC_WorldFile = nbtlib.load(ClassicWorld)

CC_WorldFilePart = CC_WorldFile['ClassicWorld'] 

CC_RealWorldSizeX = int(CC_WorldFilePart['X'])
CC_RealWorldSizeY = int(CC_WorldFilePart['Y'])
CC_RealWorldSizeZ = int(CC_WorldFilePart['Z'])

CC_WorldSizeX = CC_RealWorldSizeX - 1
CC_WorldSizeY = CC_RealWorldSizeY - 1
CC_WorldSizeZ = CC_RealWorldSizeZ - 1

CC_Blocks = numpy.array(CC_WorldFilePart['BlockArray']) % 2**8 + numpy.array(CC_WorldFilePart['BlockArray2']) * 256
CC_Blocks_3D = CC_Blocks.reshape((CC_RealWorldSizeY,CC_RealWorldSizeZ,CC_RealWorldSizeX))

print(str(CC_RealWorldSizeX) + ' ' + str(CC_RealWorldSizeY) + ' ' + str(CC_RealWorldSizeZ))

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

MT_WorldSizeX = int(round_down(CC_RealWorldSizeX / 16)) + 1
MT_WorldSizeY = int(round_down(CC_RealWorldSizeY / 16)) + 1
MT_WorldSizeZ = int(round_down(CC_RealWorldSizeZ / 16)) + 1

MT_CurrentChunkX = 0
MT_CurrentChunkY = 0
MT_CurrentChunkZ = 0
MT_RealCurrentChunkX = 0

ConversionComplete = 0

conn = sqlite3.connect("./output/map.sqlite")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS `blocks` (\
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
  cur.execute("INSERT INTO blocks VALUES (?,?)", (int(MT_Pos), mapblockdata.getvalue()))
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
  
conn.commit()
conn.close()
