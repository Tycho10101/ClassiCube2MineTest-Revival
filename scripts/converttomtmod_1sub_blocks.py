import argparse
import json
import numpy

parser = argparse.ArgumentParser()
parser.add_argument("BlockFile")
parser.add_argument("TextureName")

args = parser.parse_args()

BlockFile = open(args.BlockFile)
TextureName = args.TextureName

BlockFileData = json.loads(BlockFile.read())

ID = BlockFileData["ID2"]
CollideType = BlockFileData["CollideType"]
Speed = BlockFileData["Speed"]
TexturesFull = numpy.array(BlockFileData['Textures'])
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
TransmitsLight = BlockFileData["TransmitsLight"]
WalkSound = BlockFileData["WalkSound"]
FullBright = BlockFileData["FullBright"]
Shape = BlockFileData["Shape"]
BlockDraw = BlockFileData["BlockDraw"]
FogColor = numpy.array(BlockFileData['Fog'])
FogR = FogColor[0] % 2**8 
FogG = FogColor[1] % 2**8 
FogB = FogColor[2] % 2**8 
Coords = numpy.array(BlockFileData["Coords"])
Coords1 = Coords[0]
Coords2 = Coords[1]
Coords3 = Coords[2]
Coords4 = Coords[3]
Coords5 = Coords[4]
Coords6 = Coords[5]
BlockName = BlockFileData["Name"]

MinX = float(Coords[0])
MinY = float(Coords[1])
MinZ = float(Coords[2])
MaxX = float(Coords[3])
MaxY = float(Coords[4])
MaxZ = float(Coords[5])

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

print('minetest.register_node("' + TextureName + ':' + str(ID) + '", {')
print('\tdescription =  "' + TextureName + ' ' + BlockName + '",')
print('\tinventory_image = minetest.inventorycube("' + str(TextureNum1) + '.png", "' + str(TextureNum2) + '.png", "' + str(TextureNum3) + '.png"),')

if Shape != 0:
    if CollideType != 0:
    	if CollideType == 2 or CollideType == 3 or CollideType == 7:
        	print('\tdrawtype = "nodebox",')
    if CollideType != 1:
    	if CollideType == 4 or CollideType == 5:
        	print('\tdrawtype = "liquid",')
    else:
        print('\tdrawtype = "plantlike",')

if Shape != "0":
    print('\ttiles = { "' + str(TextureNum1) + '.png", "' + str(TextureNum2) + '.png", "' + str(TextureNum3) + '.png", "' + str(TextureNum4) + '.png", "' + str(TextureNum6) + '.png", "' + str(TextureNum5) + '.png" },')
else:
    print('\ttiles = { "' + TextureNum1 + '.png" },')
print('\tparamtype = "light",')

if CollideType != "2" or CollideType == "3" or CollideType == "4":
    	print('\twalkable = true,')
    	print('\tpointable = true,')
    	print('\tdiggable = true,')
    	print('\tbuildable_to = false,')

if CollideType == "1":
    print('\twalkable = false,')
    print('\tpointable = true,')
    print('\tdiggable = true,')
    print('\tbuildable_to = true,')
    print('\tclimbable = true,')

if CollideType != "0" or CollideType == "1" or CollideType == "5" or CollideType == "6":
    	print('\twalkable = false,')
    	print('\tpointable = false,')
    	print('\tdiggable = false,')
    	print('\tbuildable_to = true,')

if CollideType == "7":
    print('\twalkable = false,')
    print('\tpointable = true,')
    print('\tdiggable = true,')
    print('\tbuildable_to = false,')
    print('\tclimbable = true,')

print('\tis_ground_content = false,')

if FullBright == "1":
    print('\tlight_source = 14,')
print('\tuse_texture_alpha = "clip",')
print('\tdrop = "",')

if FogR != "0":
    if FogG != "0":
        if FogB != "0":
            print('\tpost_effect_color = {a=128, r=' + str(FogR) + ', g=' + str(FogG) + ', b=' + str(FogB) + '},')
print('\tnode_box = {')
print('\t\ttype = "fixed",')
print('\t\tfixed = {' + str(MinX) + ", " + str(MinY) + ", " + str(MinZ) + ", " + str(MaxX) + ", " + str(MaxY) + ", " + str(MaxZ) + '},')
print('\t},')

if WalkSound == "1":
    print('\tsounds = default.node_sound_wood_defaults(),')

if WalkSound == "2":
    print('\tsounds = default.node_sound_gravel_defaults(),')

if WalkSound == "3":
    print('\tsounds = default.node_sound_leaves_defaults(),')

if WalkSound == "4":
    print('\tsounds = default.node_sound_stone_defaults(),')

if WalkSound == "5":
    print('\tsounds = default.node_sound_metal_defaults(),')

if WalkSound == "6":
    print('\tsounds = default.node_sound_glass_defaults(),')

if WalkSound == "8":
    print('\tsounds = default.node_sound_sand_defaults(),')

if WalkSound == "9":
    print('\tsounds = default.node_sound_snow_defaults(),')

if CollideType == "5" or CollideType == "6":
    	print('\tdrowning = 1,')
    	print('\tliquidtype = "source",')
    	print('\tliquid_viscosity = 1,')

if Shape != "0":
    if CollideType == "0" or CollideType == "2" or CollideType == "3" or CollideType == "4" or CollideType == "7":
        print('\tgroups = {cracky = 3, oddly_breakable_by_hand = 3},')
    if CollideType == "5":
        print('\tgroups = {water = 3, liquid = 3, puts_out_fire = 1},')
    if CollideType == "6":
        print('\tgroups = {liquid = 2},')
else:
    print('\tgroups = {cracky = 3, oddly_breakable_by_hand = 3},')
print('})')
