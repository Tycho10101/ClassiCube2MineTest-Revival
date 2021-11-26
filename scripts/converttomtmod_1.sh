mkdir output
mkdir output/worldmods
TextureURLParsed=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvMapAppearance| .TextureURL')
export TextureName=$(basename $TextureURLParsed | sed 's/\(.*\)\..*/\1/' | tr '[:upper:]' '[:lower:]')

mkdir output/worldmods/$TextureName

rm output/worldmods/$TextureName/init.lua
rm output/worldmods/$TextureName/depends.txt

echo default > output/worldmods/$TextureName/depends.txt

echo ClassiCube2Minetest: Convert to MT Mod: Converting Sky and Cloud Colors...
SkyColor_R=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Sky | .R ')
SkyColor_G=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Sky | .G ')
SkyColor_B=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Sky | .B ')
CloudColor_R=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Cloud | .R ')
CloudColor_G=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Cloud | .G ')
CloudColor_B=$(cat extracted_custom/Metadata.json | jq '.CPE | .EnvColors | .Cloud | .B ')

echo 'minetest.register_on_joinplayer(function(player)' >> output/worldmods/$TextureName/init.lua
echo '	player:set_sky({r='$SkyColor_R', g='$SkyColor_G', b='$SkyColor_B'}, "plain", {})' >> output/worldmods/$TextureName/init.lua
echo '	player:set_clouds({' >> output/worldmods/$TextureName/init.lua
echo '		color = {r='$CloudColor_R', g='$CloudColor_G', b='$CloudColor_B'}' >> output/worldmods/$TextureName/init.lua
echo '	})' >> output/worldmods/$TextureName/init.lua
echo 'end)' >> output/worldmods/$TextureName/init.lua

echo ClassiCube2Minetest: Convert to MT Mod: Converting Blocks...
find extracted_custom/blocks/. -name "*.json*" -exec scripts/converttomtmod_1sub_blocks.sh {} \; >> output/worldmods/$TextureName/init.lua

mkdir output/worldmods/$TextureName/textures
cp extracted_custom/texture_block/* output/worldmods/$TextureName/textures/
