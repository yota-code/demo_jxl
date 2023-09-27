#!/usr/bin/env zsh

working_dir="${0:A}/.."
source_dir=${working_dir:A:h}

###########################
###  build the site part
###########################

site_dir=${source_dir}/wasm_site

mkdir ${site_dir}

python3 ${source_dir}/tools/wasm_demo/build_site.py ${source_dir}/tools/wasm_demo/ ${source_dir}/build-wasm32/tools/wasm_demo/ ${site_dir}

pushd ${site_dir}
	convert -pointsize 72 label:image00 image00.png
	${source_dir}/build/tools/cjxl image00.png image00.jxl -d 0
	convert -pointsize 72 label:image01 image01.png
	${source_dir}/build/tools/cjxl image01.png image01.jxl -d 1
	
	python3 -m http.server --bind 127.0.0.1
popd

