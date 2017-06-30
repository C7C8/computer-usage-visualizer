# Laptop Usage Visualizer

![C17.png](C17-small.png?raw=true)

These python scripts will parse datasets provided to them and generate visualizations
of their data using matplotlib and numpy. batpc.csv should be a CSV file containing
records of laptop battery charge tied to a time, while bathealth.csv should list the
laptop battery's health over time. For examples of this, see the existing batpc.csv
and bathealth.csv files provided in this repository.

## Current visualizations

* usage-vs-health.py will generate a simple line graph that shows the relationship
between hours of usage and battery health, as reported by the `acpi -V` command. It
is functional but not polished, you may have to edit the code if you want to further
bend it to your will.

* weekly-heatmaps.py will show a heatmap of usage between specified dates. By far the
most interesting visualization that will come of this project, it allows you to see
"hot spots" or dead zones in the data where the computer was frequently used or rarely
used, respectively. For instance, a strong deadzone is 6-6:30 PM, the time I usually go
to dinner.

## About the dataset

At the time of this writing, I'm a college student studying computer science. I bring
a laptop with me everywhere I go, for anything from notes to work to bashing people
over the head. Before I started the year, I thought it would be interesting to write
a few cronjobs to collect some data about my laptop's battery, so I could see how it
was used over time and how its health decayed. I wrote the scripts in August 2016 and
set the scripts whirring away, collecting battery health data every 24 hours and
battery charge data every 2 minutes. The data was promptly forgotten about until June
2017, at which point some 38,000 data points had been collected, spanning 1200 hours
of laptop usage.

Turns out, that data reveals more than just battery health and charge info! The data
was only recorded when the laptop was in use, so every point in batpc.csv represents
a moment when the laptop is in use. This lets you do some pretty interesting data
analyses, like a heatmap showing when the laptop was most often used. The only anomalous
data from early mid-February/early-March to late April, where I shifted from working
on my laptop to working on my desktop, pushing the laptop into a notes-only role.

### Technical

The two scripts (one-liners) used can be found in `bathealth.sh` and `batpc.sh`. The crontab
used to run them is also very simple:

    */2 * * * * /home/sourec/Documents/compstats/batpc.sh
    0 12 * * * /home/sourec/Documents/compstats/bathealth.sh
