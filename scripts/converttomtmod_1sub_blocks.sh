#!/bin/bash
function signedtounsigned (
	if [[ $@ -lt "0" ]]; then
	    output=$((256+$@))
	else
	    output=$@
	fi
	echo $output
)

ID=$(cat $@ | jq '.[] | select(.name == "ID2") | .value')
CollideType=$(cat $@ | jq '.[] | select(.name == "CollideType") | .value')
Speed=$(cat $@ | jq '.[] | select(.name == "Speed") | .value')
TextureNum1_signed=$(cat $@ | jq '.[] | select(.name == "Textures") | .value[0]')
TextureNum2_signed=$(cat $@ | jq '.[] | select(.name == "Textures") | .value[1]')
TextureNum3_signed=$(cat $@ | jq '.[] | select(.name == "Textures") | .value[2]')
TextureNum4_signed=$(cat $@ | jq '.[] | select(.name == "Textures") | .value[3]')
TextureNum5_signed=$(cat $@ | jq '.[] | select(.name == "Textures") | .value[4]')
TextureNum6_signed=$(cat $@ | jq '.[] | select(.name == "Textures") | .value[5]')
Textures256_1_signed=$(cat $@ | jq '.[] | select(.name == "Textures") | .value[6]')
Textures256_2_signed=$(cat $@ | jq '.[] | select(.name == "Textures") | .value[7]')
Textures256_3_signed=$(cat $@ | jq '.[] | select(.name == "Textures") | .value[8]')
Textures256_4_signed=$(cat $@ | jq '.[] | select(.name == "Textures") | .value[9]')
Textures256_5_signed=$(cat $@ | jq '.[] | select(.name == "Textures") | .value[10]')
Textures256_6_signed=$(cat $@ | jq '.[] | select(.name == "Textures") | .value[11]')
TransmitsLight=$(cat $@ | jq '.[] | select(.name == "TransmitsLight") | .value')
WalkSound=$(cat $@ | jq '.[] | select(.name == "WalkSound") | .value')
FullBright=$(cat $@ | jq '.[] | select(.name == "FullBright") | .value')
Shape=$(cat $@ | jq '.[] | select(.name == "Shape") | .value')
BlockDraw=$(cat $@ | jq '.[] | select(.name == "BlockDraw") | .value')
FogR_signed=$(cat $@ | jq '.[] | select(.name == "Fog") | .value[0]')
FogG_signed=$(cat $@ | jq '.[] | select(.name == "Fog") | .value[1]')
FogB_signed=$(cat $@ | jq '.[] | select(.name == "Fog") | .value[2]')
#Coords=$(cat $@ | jq '.[] | select(.name == "Coords") | .value')
Coords1=$(cat $@ | jq '.[] | select(.name == "Coords") | .value[0]')
Coords2=$(cat $@ | jq '.[] | select(.name == "Coords") | .value[1]')
Coords3=$(cat $@ | jq '.[] | select(.name == "Coords") | .value[2]')
Coords4=$(cat $@ | jq '.[] | select(.name == "Coords") | .value[3]')
Coords5=$(cat $@ | jq '.[] | select(.name == "Coords") | .value[4]')
Coords6=$(cat $@ | jq '.[] | select(.name == "Coords") | .value[5]')
NameP=$(cat $@ | jq '.[] | select(.name == "Name") | .value')

BlockName=$(echo $NameP | sed 's/"//g') 
TextureNum1=$(signedtounsigned $TextureNum1_signed)
TextureNum2=$(signedtounsigned $TextureNum2_signed)
TextureNum3=$(signedtounsigned $TextureNum3_signed)
TextureNum4=$(signedtounsigned $TextureNum4_signed)
TextureNum5=$(signedtounsigned $TextureNum5_signed)
TextureNum6=$(signedtounsigned $TextureNum6_signed)
Textures256_1=$(signedtounsigned $Textures256_1_signed)
Textures256_2=$(signedtounsigned $Textures256_2_signed)
Textures256_3=$(signedtounsigned $Textures256_3_signed)
Textures256_4=$(signedtounsigned $Textures256_4_signed)
Textures256_5=$(signedtounsigned $Textures256_5_signed)
Textures256_6=$(signedtounsigned $Textures256_6_signed)
FogR=$(signedtounsigned $FogR_signed)
FogB=$(signedtounsigned $FogB_signed)
FogG=$(signedtounsigned $FogG_signed)

TextureNum1=$(expr $Textures256_1 \* 256 + $TextureNum1)
TextureNum2=$(expr $Textures256_2 \* 256 + $TextureNum2)
TextureNum3=$(expr $Textures256_3 \* 256 + $TextureNum3)
TextureNum4=$(expr $Textures256_4 \* 256 + $TextureNum4)
TextureNum5=$(expr $Textures256_5 \* 256 + $TextureNum5)
TextureNum6=$(expr $Textures256_6 \* 256 + $TextureNum6)

CoordsString=$(python3 scripts/converttomtmod_1sub_blocksize.py $Coords1 $Coords2 $Coords3 $Coords4 $Coords5 $Coords6)

echo 'minetest.register_node("classicubeconverted:'$ID'", {'
echo '	inventory_image = minetest.inventorycube("texture.png"),'
if [ "$CollideType" = 0 ] || [ "$CollideType" = 1 ] || [ "$CollideType" = 2 ] || [ "$CollideType" = 3 ];
	then
	echo '	drawtype = "nodebox",'
	fi
if [ "$CollideType" = 4 ] || [ "$CollideType" = 5 ];
	then
	echo '	drawtype = "liquid",'
	fi
echo '	tiles = { "'$TextureNum1'.png", "'$TextureNum2'.png", "'$TextureNum3'.png", "'$TextureNum4'.png", "'$TextureNum6'.png", "'$TextureNum5'.png" },'
echo '	alpha = 255,'
echo '	paramtype = "light",'

if [ "$CollideType" = 1 ] || [ "$CollideType" = 2 ] || [ "$CollideType" = 3 ];
	then
	echo '	walkable = true,'
	echo '	pointable = true,'
	echo '	diggable = true,'
	echo '	buildable_to = false,'
	fi
if [ "$CollideType" = 0 ] || [ "$CollideType" = 4 ] || [ "$CollideType" = 5 ];
	then
	echo '	walkable = false,'
	echo '	pointable = false,'
	echo '	diggable = false,'
	echo '	buildable_to = true,'
	fi
if [ "$CollideType" = 1 ];
	then
	echo '	walkable = false,'
	echo '	pointable = true,'
	echo '	diggable = true,'
	echo '	buildable_to = false,'
	fi

echo '	is_ground_content = false,'
echo '	use_texture_alpha = true,'
echo '	drop = "",'
echo '	post_effect_color = {a=255, r='$FogR', g='$FogG', b='$FogB'},'
echo '	node_box = {'
echo '		type = "fixed",'
echo '		fixed = {'$CoordsString'},'
echo '	},'
echo '})'