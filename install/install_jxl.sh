#!/usr/bin/env zsh

source_DIR=${JXL_root_DIR}/repo/libjxl
build_DIR=${JXL_root_DIR}/build/libjxl
root_DIR=${JXL_root_DIR}/root

if [[ -d ${build_DIR} ]]
then
	rm -rf ${build_DIR}
fi
mkdir ${build_DIR}

pushd ${build_DIR}
	cmake --install-prefix=${root_DIR} \
		-DCMAKE_CXX_FLAGS="-O3 -march=native -mtune=native" \
		-DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF \
		${source_DIR}
	make
	make install
popd
