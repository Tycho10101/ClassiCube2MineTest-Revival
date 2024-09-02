import mcc2mt

mcc2mt.CCLoadMap('firstworld.cw')
mcc2mt.ConvertBlocks('firstblocks') #blocks_modname
mcc2mt.ConvertWorld('firstblocks', 0, 0, 0, False) #using blocks_modname blocks
CC_WorldSpawn = mcc2mt.GetSpawnData()
mcc2mt.MT_MakePlayersFile(int(CC_WorldSpawn[0]['X']), int(CC_WorldSpawn[0]['Y']), int(CC_WorldSpawn[0]['Z']), CC_WorldSpawn[1])


mcc2mt.CCLoadMap('secondworld.cw')
mcc2mt.ConvertBlocks('secondblocks') #blocks_modname
mcc2mt.ConvertWorld('secondblocks', 0, 0, 0, False) #using blocks_modname blocks


mcc2mt.MT_Final('firstworld') #worldname
