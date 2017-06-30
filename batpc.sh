#!/bin/zsh
echo "`date`, `date +"%s"`, `acpi -b | grep -Po "\d{1,3}(?=%)"`" >> /home/sourec/Documents/compstats/batpc.csv
