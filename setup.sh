#!/bin/bash

wd=$PWD
# Setup Driver for hardware
wget  https://files.waveshare.com/upload/8/80/IT8951_20200319_Release.7z
7z x IT8951_20200319_Release.7z -O./IT8951
cp -r epaper_driver IT8951
cd IT8951/

rm Makefile
mv epaper_driver/Makefile .

make clean
make -j4

cp epaper_display $wd
cd $wd



