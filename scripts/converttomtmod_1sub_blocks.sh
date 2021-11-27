#!/bin/bash
function signedtounsigned (
	if [[ $@ -lt "0" ]]; then
	    output=$((256+$@))
	else
	    output=$@
	fi
	echo $output
)

ID=$(cat $@ | jq '.ID2')
CollideType=$(cat $@ | jq '.CollideType')
Speed=$(cat $@ | jq '.Speed')
TextureNum1_signed=$(cat $@ | jq '.Textures[0]')
TextureNum2_signed=$(cat $@ | jq '.Textures[1]')
TextureNum3_signed=$(cat $@ | jq '.Textures[2]')
TextureNum4_signed=$(cat $@ | jq '.Textures[3]')
TextureNum5_signed=$(cat $@ | jq '.Textures[4]')
TextureNum6_signed=$(cat $@ | jq '.Textures[5]')
Textures256_1_signed=$(cat $@ | jq '.Textures[6]')
Textures256_2_signed=$(cat $@ | jq '.Textures[7]')
Textures256_3_signed=$(cat $@ | jq '.Textures[8]')
Textures256_4_signed=$(cat $@ | jq '.Textures[9]')
Textures256_5_signed=$(cat $@ | jq '.Textures[10]')
Textures256_6_signed=$(cat $@ | jq '.Textures[11]')
TransmitsLight=$(cat $@ | jq '.TransmitsLight')
WalkSound=$(cat $@ | jq '.WalkSound')
FullBright=$(cat $@ | jq '.FullBright')
Shape=$(cat $@ | jq '.Shape')
BlockDraw=$(cat $@ | jq '.BlockDraw')
FogR_signed=$(cat $@ | jq '.Fog[0]')
FogG_signed=$(cat $@ | jq '.Fog[1]')
FogB_signed=$(cat $@ | jq '.Fog[2]')
Coords1=$(cat $@ | jq '.Coords[0]')
Coords2=$(cat $@ | jq '.Coords[1]')
Coords3=$(cat $@ | jq '.Coords[2]')
Coords4=$(cat $@ | jq '.Coords[3]')
Coords5=$(cat $@ | jq '.Coords[4]')
Coords6=$(cat $@ | jq '.Coords[5]')
NameP=$(cat $@ | jq '.Name')

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

echo 'minetest.register_node("'$TextureName':'$ID'", {'
echo '	description =  "'$TextureName' '$BlockName'",'
echo '	inventory_image = minetest.inventorycube("'$TextureNum1'.png", "'$TextureNum2'.png", "'$TextureNum3'.png"),'

if [ "$Shape" != 0 ]; then
	if [ "$CollideType" = 0 ] || [ "$CollideType" = 2 ] || [ "$CollideType" = 3 ] || [ "$CollideType" = 7 ];
		then
		echo '	drawtype = "nodebox",'
		fi
	if [ "$CollideType" = 1 ] || [ "$CollideType" = 4 ] || [ "$CollideType" = 5 ];
		then
		echo '	drawtype = "liquid",'
		fi
	else
		echo '	drawtype = "plantlike",'
	fi	

if [ "$Shape" != 0 ]; then
		echo '	tiles = { "'$TextureNum1'.png", "'$TextureNum2'.png", "'$TextureNum3'.png", "'$TextureNum4'.png", "'$TextureNum6'.png", "'$TextureNum5'.png" },'
	else
		echo '	tiles = { "'$TextureNum1'.png" },'
	fi

echo '	paramtype = "light",'

if [ "$CollideType" = 2 ] || [ "$CollideType" = 3 ] || [ "$CollideType" = 4 ]; then
	echo '	walkable = true,'
	echo '	pointable = true,'
	echo '	diggable = true,'
	echo '	buildable_to = false,'
	fi
if [ "$CollideType" = 1 ]; then
	echo '	walkable = false,'
	echo '	pointable = true,'
	echo '	diggable = true,'
	echo '	buildable_to = true,'
	echo '	climbable = true,'
	fi
if [ "$CollideType" = 0 ] || [ "$CollideType" = 1 ] || [ "$CollideType" = 5 ] || [ "$CollideType" = 6 ]; then
	echo '	walkable = false,'
	echo '	pointable = false,'
	echo '	diggable = false,'
	echo '	buildable_to = true,'
	fi
if [ "$CollideType" = 7 ]; then
	echo '	walkable = false,'
	echo '	pointable = true,'
	echo '	diggable = true,'
	echo '	buildable_to = false,'
	echo '	climbable = true,'
	fi

echo '	is_ground_content = false,'
echo '	use_texture_alpha = "clip",'
echo '	drop = "",'
if [ "$FogR" != 0 ]; then
	if [ "$FogG" != 0 ]; then
		if [ "$FogB" != 0 ]; then
			echo '	post_effect_color = {a=128, r='$FogR', g='$FogG', b='$FogB'},'
			fi
		fi
	fi

if [ "$Shape" != 0 ]; then
	echo '	selection_box = {'
	echo '		type = "fixed",'
	echo '		fixed = {'$CoordsString'}'
	echo '	},'
	fi

echo '	node_box = {'
echo '		type = "fixed",'
echo '		fixed = {'$CoordsString'},'
echo '	},'

if [ "$WalkSound" = 1 ]; then
	echo '	sounds = default.node_sound_wood_defaults(),'
	fi
if [ "$WalkSound" = 2 ]; then
	echo '	sounds = default.node_sound_gravel_defaults(),'
	fi
if [ "$WalkSound" = 3 ]; then
	echo '	sounds = default.node_sound_leaves_defaults(),'
	fi
if [ "$WalkSound" = 4 ]; then
	echo '	sounds = default.node_sound_stone_defaults(),'
	fi
if [ "$WalkSound" = 5 ]; then
	echo '	sounds = default.node_sound_metal_defaults(),'
	fi
if [ "$WalkSound" = 6 ]; then
	echo '	sounds = default.node_sound_glass_defaults(),'
	fi
if [ "$WalkSound" = 8 ]; then
	echo '	sounds = default.node_sound_sand_defaults(),'
	fi
if [ "$WalkSound" = 9 ]; then
	echo '	sounds = default.node_sound_snow_defaults(),'
	fi

if [ "$CollideType" = 5 ] || [ "$CollideType" = 6 ]; then
	echo '	drowning = 1,'
	echo '	liquidtype = "source",'
	echo '	liquid_viscosity = 1,'
	fi

if [ "$Shape" != 0 ]; then
	if [ "$CollideType" = 0 ] || [ "$CollideType" = 2 ] || [ "$CollideType" = 3 ] || [ "$CollideType" = 4 ] || [ "$CollideType" = 7 ];
		then
		echo '	groups = {cracky = 3, oddly_breakable_by_hand = 3},'
		fi
	if [ "$CollideType" = 5 ];
		then
		echo '	groups = {water = 3, liquid = 3, puts_out_fire= 1},'
		fi
	if [ "$CollideType" = 6 ];
		then
		echo '	groups = {liquid = 2},'
		fi
	else
		echo '	groups = {cracky = 3, oddly_breakable_by_hand = 3},'
	fi	

echo '})'
