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

if [ -f 'extracted_custom/textures/skybox.png' ]; then
	echo ClassiCube2Minetest: Convert to MT Mod: Converting Skybox...
	echo '	player:set_sky({' >> output/worldmods/$1/init.lua
	echo '		type = "skybox",' >> output/worldmods/$1/init.lua
	echo '		textures = {"skybox1.png", "skybox2.png^[transformR180", "skybox4.png", "skybox6.png^[transformR180", "skybox3.png^[transformR180", "skybox5.png^[transformR180"},' >> output/worldmods/$1/init.lua
	echo '		clouds = false' >> output/worldmods/$1/init.lua
	echo '	})' >> output/worldmods/$1/init.lua
	echo '	player:set_sun({visible = false, sunrise_visible = false})' >> output/worldmods/$1/init.lua
	echo '	player:set_moon({visible = false})' >> output/worldmods/$1/init.lua
	echo '	player:set_stars({visible = false})' >> output/worldmods/$1/init.lua
else
	echo '	player:set_sky({r='$SkyColor_R', g='$SkyColor_G', b='$SkyColor_B'}, "plain", {})' >> output/worldmods/$1/init.lua
fi

echo '	player:set_clouds({' >> output/worldmods/$1/init.lua
echo '		color = {r='$CloudColor_R', g='$CloudColor_G', b='$CloudColor_B'}' >> output/worldmods/$1/init.lua
echo '	})' >> output/worldmods/$1/init.lua
echo 'end)' >> output/worldmods/$1/init.lua

echo ClassiCube2Minetest: Convert to MT Mod: Converting Blocks...
find extracted_custom/blocks/. -name "*.json*" -exec python3 scripts/converttomtmod_1sub_blocks.py {} $TextureName \; >> output/worldmods/$1/init.lua

mkdir output/worldmods/$1/textures

if [ -f 'extracted_custom/textures/skybox.png' ]; then
    convert extracted_custom/textures/skybox.png -crop 1024x1024+1024+0 output/worldmods/$1/textures/skybox1.png
    convert extracted_custom/textures/skybox.png -crop 1024x1024+2048+0 output/worldmods/$1/textures/skybox2.png
    convert extracted_custom/textures/skybox.png -crop 1024x1024+0+1024 output/worldmods/$1/textures/skybox3.png
    convert extracted_custom/textures/skybox.png -crop 1024x1024+1024+1024 output/worldmods/$1/textures/skybox4.png
    convert extracted_custom/textures/skybox.png -crop 1024x1024+2048+1024 output/worldmods/$1/textures/skybox5.png
    convert extracted_custom/textures/skybox.png -crop 1024x1024+3072+1024 output/worldmods/$1/textures/skybox6.png
fi

cp extracted_custom/texture_block/* output/worldmods/$1/textures/
