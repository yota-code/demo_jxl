#!/usr/bin/env zsh

source_DIR=${JXL_root_DIR}/repo/libavif
build_DIR=${JXL_root_DIR}/build/libavif
root_DIR=${JXL_root_DIR}/root

if [[ -d ${build_DIR} ]]
then
	rm -rf ${build_DIR}
fi
mkdir ${build_DIR}

pushd ${build_DIR}
	cmake --install-prefix=${root_DIR} \
		-DCMAKE_CXX_FLAGS="-O3 -march=native -mtune=native" \
		-DAVIF_CODEC_AOM=SYSTEM -DAVIF_BUILD_APPS=ON -DAVIF_LIBYUV=SYSTEM\
		${source_DIR}
	make
	make install
popd
