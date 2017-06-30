#!/usr/bin/python3
from dateutil import parser as dateparser
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np
import csv
import sys


def get_time_grid(batterydata, start, end, resolution, entryfilter=lambda x: False):
	"""Get a properly formatted time grid based on given information. Resolution is the number of samples per hour in the
	resulting array, and the entryfilter is a lambda that can be used to filter out data points from inclusion."""
	minutes_per_sample = 60/resolution
	maxusage = 0.0

	data = [[0.0]*7 for i in range(0, 24*resolution)]  # weird formatting so matplotlib plots things the right way
	for entry in batterydata:
		if entry[0] < start or entry[0] > end or entryfilter(entry):
			continue
		day = entry[0].weekday()
		timeslot = (entry[0].hour * resolution) + int(entry[0].minute / minutes_per_sample)
		data[timeslot][day] += 1.0
		if data[timeslot][day] > maxusage:
			maxusage = data[timeslot][day]

	# Normalize the data
	for timeslot in range(0, len(data)):
		for day in range(0, len(data[timeslot])):
			data[timeslot][day] /= maxusage

	return data


def generate_heatmap(data, start_date, end_date, resolution=30, width=600, height=800, style="afmhot",
																					entryfilter=lambda x: False):
	"""Place a heatmap on the selected subplot. data should be generated using get_time_grid, resolution is how many
	samples per hour to evaluate, style is a style defined by matplotlib, entryfilter can be used to filter out data
	points from inclusion in the graph, and the other parmeters are self explanatory"""

	# "Constant" data that there has to be a better way of setting up
	weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	times = [str(i) for i in range(1, 12)]*2
	times.insert(0, "12")
	times.insert(12, "12")
	for i in range(0, len(times)):
		times[i] += " AM" if i <= 11 else " PM"

	figure, ax = plt.subplots()
	ax.imshow(get_time_grid(data, start_date, end_date, resolution, entryfilter), extent=[0, width, 0, height], cmap=style,
											alpha=0.75, origin="upper")
	ax.set_frame_on(False)
	ax.xaxis.tick_top()
	plt.xticks(np.arange(0, width - (width/7), width/7)+(width/14), weekdays)
	plt.yticks(np.arange(0, height, height/24)+(height/24), reversed(times))

if len(sys.argv) < 4:
	print("Usage: ./usage-vs-health.py [batpc.csv] [start date] [end date] [title]")
	sys.exit(1)
if len(sys.argv) == 4:
	sys.argv.append("Usage Heatmap")  # default title

# Parse batpc. date,battery%
batpc = []
with open(sys.argv[1], "r") as batpcsv:
	reader = csv.reader(batpcsv)
	for line in reader:
		batpc.append([dateparser.parse(line[0]).replace(tzinfo=None), int(line[2])])


startDate = dateparser.parse(sys.argv[2])
endDate = dateparser.parse(sys.argv[3])
print("Showing heatmap from " + startDate.ctime() + " to " + endDate.ctime())
generate_heatmap(batpc, startDate, endDate, resolution=30, width=600, height=800)
figure = plt.gcf()
figure.set_size_inches(8, 10)
figure.suptitle(sys.argv[4])
plt.show()
