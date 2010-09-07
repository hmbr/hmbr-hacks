#!/usr/bin/env bash
GIT_DIRS=../

pushd  $GIT_DIRS;

for i in * ;
do 
	echo $i
	cd $i ; 
	git pull; 
	cd -; 
done

popd
