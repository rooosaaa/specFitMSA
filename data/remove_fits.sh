#!/bin/bash
base_dir="/raid/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/data/project_mphys_ultrablue/pymc_outputs_prism"

while read -r file; do
  if [ -f "$base_dir/$file" ]; then
    echo "Removing $file"
    rm "$base_dir/$file"
  else
    echo "File not found: $file"
  fi
done < bad_outputs.txt