#!/bin/bash

for TMP in fullload*
do
  NEW=${TMP}.tar.xz;
  echo "tar -cvJpf $NEW $TMP";
  tar -cvJpf $NEW $TMP;
done;

for TMP in onelevel*
do
  NEW=${TMP}.tar.xz;
  echo "tar -cvJpf $NEW $TMP";
  tar -cvJpf $NEW $TMP;
done;

for TMP in twolevel*
do
  NEW=${TMP}.tar.xz;
  echo "tar -cvJpf $NEW $TMP";
  tar -cvJpf $NEW $TMP;
done;
