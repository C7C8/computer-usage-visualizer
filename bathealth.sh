#!/bin/zsh
echo "`date`, `acpi -bi | grep -Po "mAh\s=\s\d{1,3}" | grep -Po "\d+"`" >> /home/sourec/Documents/compstats/bathealth.csv

