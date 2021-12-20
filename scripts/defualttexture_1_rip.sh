mkdir extracted
mkdir extracted/textures
cd extracted/textures
7za x ../../defualt/default.zip 
cd ../../

size=$(identify -format '%w %h' extracted/textures/terrain.png)
TerrainSizeX=$(echo $size | cut -d ' ' -f 1)
TerrainSizeY=$(echo $size | cut -d ' ' -f 2)
BlockSizeX=$(expr $TerrainSizeX / 16)
BlockSizeY=$(expr $TerrainSizeY / 16)

CurrentBlockX=1
CurrentBlockY=1

mkdir extracted/texture_block
#convert extracted/textures/terrain.png -crop 16x16+0+0 cropped.jpg
BlockNumber=1
while [ $CurrentBlockY -le $BlockSizeY ]; 
do 
	echo $CurrentBlockX $CurrentBlockY $BlockNumber
	PixelCropX=$(expr $CurrentBlockX \* 16)
	PixelCropX=$(expr $PixelCropX - 16)
	PixelCropY=$(expr $CurrentBlockY \* 16)
	PixelCropY=$(expr $PixelCropY - 16)
	convert extracted/textures/terrain.png -crop 16x16+$PixelCropX+$PixelCropY extracted/texture_block/$BlockNumber.png

	BlockNumber=$(($BlockNumber+1))
	CurrentBlockX=$(($CurrentBlockX+1))
	if (( $CurrentBlockX > $BlockSizeX )); then
	CurrentBlockY=$(($CurrentBlockY+1))
	CurrentBlockX=1
    fi
done
