import argparse
import cc2mt

parser = argparse.ArgumentParser()
parser.add_argument("mapname")
parser.add_argument("ClassicWorld")

args = parser.parse_args()

MapName = args.mapname
ClassicWorld = args.ClassicWorld

cc2mt.CCLoadMap(ClassicWorld)
cc2mt.ConvertBlocks(MapName) #blocks_modname
cc2mt.ConvertEnv(MapName + 'world') #blocks_worldname
cc2mt.ConvertWorld(MapName, 0, 0, 0, False) #using blocks_modname blocks
CC_WorldSpawn = cc2mt.GetSpawnData()
cc2mt.MT_MakePlayersFile(int(CC_WorldSpawn[0]['X']), int(CC_WorldSpawn[0]['Y']), int(CC_WorldSpawn[0]['Z']), CC_WorldSpawn[1])
cc2mt.MT_Final(MapName) #worldname
