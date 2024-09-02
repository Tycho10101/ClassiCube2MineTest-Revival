import argparse
import mcc2mt
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("mapname")
parser.add_argument("ClassicWorld")

args = parser.parse_args()

MapName = args.mapname
ClassicWorld = args.ClassicWorld

basenamewithext = os.path.basename(ClassicWorld)

worldname = basenamewithext.split(".")[0]

mcc2mt.CCLoadMap(ClassicWorld)
mcc2mt.ConvertBlocks(MapName, worldname)  # blocks_modname
mcc2mt.ConvertEnv(MapName + "world", worldname)  # blocks_worldname
shutil.rmtree("./texture")
mcc2mt.ConvertWorld(MapName, worldname, 0, 0, 0, False)  # using blocks_modname blocks
CW_WorldSpawn = mcc2mt.GetSpawnData()
mcc2mt.MT_MakePlayersFile(
    worldname,
    int(CW_WorldSpawn[0]["X"]),
    int(CW_WorldSpawn[0]["Y"]),
    int(CW_WorldSpawn[0]["Z"]),
    CW_WorldSpawn[1],
)
mcc2mt.MT_Final(MapName, worldname)  # worldname
