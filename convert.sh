if [ $# -eq 0 ]
then
      echo "convert.sh worldname cw_file"
      exit
fi

rm -rf extracted_custom/*
rm -rf extracted/*
rm -rf output/*
scripts/extractmetadata.sh ${@:2}
scripts/customblocks_1_extractblockdefs.sh ${@:2}
scripts/customblocks_2_blockseperatejson.sh
scripts/customtexture_1_download.sh
scripts/customtexture_2_rip.sh
scripts/converttomtmod_1.sh $1
python3 scripts/convertworld_v25.py "$1" ${@:2}
scripts/final.sh $1