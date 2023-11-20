#!/usr/bin/env zsh

mkdir v_d2.0

for file in ref/*.png
do
	cjxl -d 2.0 $file v_d2.0/${file:t:r}.jxl
	djxl v_d2.0/${file:t:r}.jxl v_d2.0/${file:t:r}.png
	rm v_d2.0/*.jxl
done

mkdir v_d3.0

for file in ref/*.png
do
	cjxl -d 3.0 $file v_d3.0/${file:t:r}.jxl
	djxl v_d3.0/${file:t:r}.jxl v_d3.0/${file:t:r}.png
	rm v_d3.0/*.jxl
done

