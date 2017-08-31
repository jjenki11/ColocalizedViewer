#!/bin/bash

# read in file names and rename based on last space entry


# The command we are running
#           kdu_expand -i PTM726-F90-2015.06.04-15.39.37_PTM726_1_0268.jp2 -o f_268.tif -reduce 4


#       $1 is input directory
#       $2 is reduction amount
#       $3 is output directory

bin_dir=/stbb_home/jenkinsjc/dev/DTIREG/DTIReg/bin

dirr="$1"
echo "the directory -> $dirr"

red_dir=$2
green_dir=$3
blue_dir=$4

$bin_dir/CreateVolumeFromSlices -i $red_dir -o /raid2/data/jenkinsjc/CSHL/jp2000_reduced/fluorescent/reduce_6_RGB_Split_Nifti/reduce_6_red.nii -f 1 -l 359 -t tif
$bin_dir/CreateVolumeFromSlices -i $green_dir -o /raid2/data/jenkinsjc/CSHL/jp2000_reduced/fluorescent/reduce_6_RGB_Split_Nifti/reduce_6_green.nii -f 1 -l 359 -t tif
$bin_dir/CreateVolumeFromSlices -i $blue_dir -o /raid2/data/jenkinsjc/CSHL/jp2000_reduced/fluorescent/reduce_6_RGB_Split_Nifti/reduce_6_blue.nii -f 1 -l 359 -t tif

echo "DONE"

exit

for entry in "$dirr"/*
do
    filename="${entry##*/}"
    echo "filename -> $filename"
    extension="${entry##*.}"
    echo "extension -> $extension"
    file_number="${filename##*_}"
    newFile=$3/$file_number
    new_file_r=${newFile%%.*}\.tif
    #echo "kakadu now reducing $entry by a factor of $2 to $new_file then normalizing intensities"
    
    rimg=$red_dir$file_number
    gimg=$green_dir$file_number
    bimg=$blue_dir$file_number
    echo "Splitting rgb of $entry into "$rimg" "$gimg" "$bimg"."
    $bin_dir/jSplitRGBImage -i "$entry" -r $rimg -g $gimg -b $bimg

done


