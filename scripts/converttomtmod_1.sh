mkdir output
mkdir output/worldmods
mkdir output/worldmods/classicubeconverted

rm output/worldmods/classicubeconverted/init.lua
rm output/worldmods/classicubeconverted/depends.txt

echo default > output/worldmods/classicubeconverted/depends.txt

echo ClassiCube2Minetest: Convert to MT Mod: Converting Sky and Cloud Colors...
SkyColor_R=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Sky | .R ')
SkyColor_G=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Sky | .G ')
SkyColor_B=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Sky | .B ')
CloudColor_R=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Cloud | .R ')
CloudColor_G=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Cloud | .G ')
CloudColor_B=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Cloud | .B ')

echo 'minetest.register_on_joinplayer(function(player)' >> output/worldmods/classicubeconverted/init.lua
echo '	player:set_sky({r='$SkyColor_R', g='$SkyColor_G', b='$SkyColor_B'}, "plain", {})' >> output/worldmods/classicubeconverted/init.lua
echo '	player:set_clouds({' >> output/worldmods/classicubeconverted/init.lua
echo '		color = {r='$CloudColor_R', g='$CloudColor_G', b='$CloudColor_B'}' >> output/worldmods/classicubeconverted/init.lua
echo '	})' >> output/worldmods/classicubeconverted/init.lua
echo 'end)' >> output/worldmods/classicubeconverted/init.lua

echo ClassiCube2Minetest: Convert to MT Mod: Converting Blocks...
find extracted_custom/blocks/. -name "*.json*" -exec scripts/converttomtmod_1sub_blocks.sh {} \; >> output/worldmods/classicubeconverted/init.lua

mkdir output/worldmods/classicubeconverted/textures
cp extracted_custom/texture_block/* output/worldmods/classicubeconverted/textures/
