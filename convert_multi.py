import cc2mt

cc2mt.CCLoadMap('firstworld.cw')
cc2mt.ConvertBlocks('firstblocks') #blocks_modname
cc2mt.ConvertWorld('firstblocks', 0, 0, 0, False) #using blocks_modname blocks
CC_WorldSpawn = cc2mt.GetSpawnData()
cc2mt.MT_MakePlayersFile(int(CC_WorldSpawn[0]['X']), int(CC_WorldSpawn[0]['Y']), int(CC_WorldSpawn[0]['Z']), CC_WorldSpawn[1])


cc2mt.CCLoadMap('secondworld.cw')
cc2mt.ConvertBlocks('secondblocks') #blocks_modname
cc2mt.ConvertWorld('secondblocks', 0, 0, 0, False) #using blocks_modname blocks


cc2mt.MT_Final('firstworld') #worldname
