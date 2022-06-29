import argparse
import cc2mt
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("mapname")
parser.add_argument("ClassicWorld")

args = parser.parse_args()

MapName = args.mapname
ClassicWorld = args.ClassicWorld

basenamewithext = os.path.basename(ClassicWorld)

worldname = basenamewithext.split('.')[0]

cc2mt.CCLoadMap(ClassicWorld)
cc2mt.ConvertBlocks(MapName, worldname) #blocks_modname
cc2mt.ConvertEnv(MapName + 'world', worldname) #blocks_worldname
shutil.rmtree('./texture')
cc2mt.ConvertWorld(MapName, worldname, 0, 0, 0, False) #using blocks_modname blocks
CC_WorldSpawn = cc2mt.GetSpawnData()
cc2mt.MT_MakePlayersFile(worldname, int(CC_WorldSpawn[0]['X']), int(CC_WorldSpawn[0]['Y']), int(CC_WorldSpawn[0]['Z']), CC_WorldSpawn[1])
cc2mt.MT_Final(MapName, worldname) #worldname
