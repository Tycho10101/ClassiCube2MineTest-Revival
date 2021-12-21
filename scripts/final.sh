echo "enable_damage = true" >> output/world.mt
echo "creative_mode = true" >> output/world.mt
echo "auth_backend = sqlite3" >> output/world.mt
echo "player_backend = sqlite3" >> output/world.mt
echo "backend = sqlite3" >> output/world.mt
echo "gameid = minetest" >> output/world.mt
echo "world_name = $@" >> output/world.mt
echo "server_announce = false" >> output/world.mt

echo "mg_flags = caves, dungeons, light, decorations, biomes, ores" >> output/map_meta.txt
echo "chunksize = 5" >> output/map_meta.txt
echo "mapgen_limit = 31000" >> output/map_meta.txt
echo "water_level = 1" >> output/map_meta.txt
echo "seed = 0" >> output/map_meta.txt
echo "mg_name = singlenode" >> output/map_meta.txt
echo "[end_of_params]" >> output/map_meta.txt
