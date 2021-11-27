mkdir output
mkdir output/worldmods
export TextureName=$1

mkdir output/worldmods/$1

rm output/worldmods/$1/init.lua
rm output/worldmods/$1/depends.txt

echo default > output/worldmods/$1/depends.txt

echo ClassiCube2Minetest: Convert to MT Mod: Converting Sky and Cloud Colors...
SkyColor_R=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Sky | .R ')
SkyColor_G=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Sky | .G ')
SkyColor_B=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Sky | .B ')
CloudColor_R=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Cloud | .R ')
CloudColor_G=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Cloud | .G ')
CloudColor_B=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Cloud | .B ')

echo 'minetest.register_on_joinplayer(function(player)' >> output/worldmods/$1/init.lua
echo '	player:set_sky({r='$SkyColor_R', g='$SkyColor_G', b='$SkyColor_B'}, "plain", {})' >> output/worldmods/$1/init.lua
echo '	player:set_clouds({' >> output/worldmods/$1/init.lua
echo '		color = {r='$CloudColor_R', g='$CloudColor_G', b='$CloudColor_B'}' >> output/worldmods/$1/init.lua
echo '	})' >> output/worldmods/$1/init.lua
echo 'end)' >> output/worldmods/$1/init.lua

echo ClassiCube2Minetest: Convert to MT Mod: Converting Blocks...
find extracted_custom/blocks/. -name "*.json*" -exec scripts/converttomtmod_1sub_blocks.sh {} \; >> output/worldmods/$1/init.lua

mkdir output/worldmods/$1/textures
cp extracted_custom/texture_block/* output/worldmods/$1/textures/
