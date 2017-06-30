#!/usr/bin/python3
from dateutil import parser as dateparser
from matplotlib import pyplot as plt
import sys
import csv

# This script generates a graph that graphs battery health vs. battery usage on a scatter plot, drawing a line of best
# fit if applicable. The first argument should be a CSV file containing a daily report of battery health, and the second
# CSV file containing a report of minute-by-minute battery charge (this is used to determine when the battery is in use)
# Format should be as follows:
#
# Battery health:
# weekday month day HH:MM:SS timezone year, health
#
# Battery charge:
# weekday month day HH:MM:SS timezone year, unixtime, percentage.
#
# Output is a graph as plotted by matplotlib.

if len(sys.argv) < 3:
	print("Usage: ./usage-vs-health.py [bathealth.csv] [batpc.csv]")
	sys.exit(1)


# Parse bathealth. date,health%
bathealth = []
with open(sys.argv[1], "r") as healthcsv:
	reader = csv.reader(healthcsv)
	for line in reader:
		if "100" not in line[1]:
			date = dateparser.parse(line[0])
			bathealth.append([dateparser.parse(line[0]), int(line[1])])

# Parse batpc. date,battery%
batpc = []
with open(sys.argv[2], "r") as batpcsv:
	reader = csv.reader(batpcsv)
	for line in reader:
		batpc.append([dateparser.parse(line[0]), int(line[2])])

# Get hours of usage up to point. Not the most efficient, but whatever.
hours = []
for healthrecord in bathealth:
	for i in range(0, len(batpc)):
		if batpc[i][0] > healthrecord[0]:
			hours.append((i*2) / 60)
			break

plt.plot(hours, [y[1] for y in bathealth])
plt.xlabel("Hours of use")
plt.ylabel("Battery health (%)")
plt.title("Battery health vs. hours of use")
plt.show()
