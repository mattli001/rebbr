#!/bin/bash

set +x
# This script simple copys experimental results into the data folder.

FILES="figure8.png experiment1_figure.png experiment2_figure.png experiment3_figure.png"

for $file in FILES; do
  echo "Copying $file..."
  cp -f $file figures/$file

  
echo "Figure copy complete"
