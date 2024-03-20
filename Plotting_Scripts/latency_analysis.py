"""
Analyzes the bent-pipe latency based on the first hop of the traceroute
The overall RTT is not that interesting to analyze!
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import statsmodels.api as sm

#read the data
twente_traceroutes = pd.read_csv("Raw_Data/Enschede/net_traceroute.csv")
uos_traceroutes = pd.read_csv("Raw_Data/Osnabrück/net_traceroute.csv")

twente_merged = pd.read_csv("Preprocessed_Data/analysis_data_Enschede.csv")
uos_merged = pd.read_csv("Preprocessed_Data/analysis_data_Osnabrück.csv")

#convert timestamps
twente_traceroutes["timestamp_start"] = pd.to_datetime(twente_traceroutes["timestamp_start"])
twente_traceroutes["timestamp_end"] = pd.to_datetime(twente_traceroutes["timestamp_end"])
uos_traceroutes["timestamp_start"] = pd.to_datetime(uos_traceroutes["timestamp_start"])
uos_traceroutes["timestamp_end"] = pd.to_datetime(uos_traceroutes["timestamp_end"])
twente_merged["timestamp_start"] = pd.to_datetime(twente_merged["timestamp_start"])
twente_merged["timestamp_end"] = pd.to_datetime(twente_merged["timestamp_end"])
uos_merged["timestamp_start"] = pd.to_datetime(uos_merged["timestamp_start"])
uos_merged["timestamp_end"] = pd.to_datetime(uos_merged["timestamp_end"])

#filter nans
twente_merged = twente_merged.dropna(subset=["ping_avg"])
uos_merged = uos_merged.dropna(subset=["ping_avg"])
twente_merged = twente_merged.sort_values(by="timestamp_start")
uos_merged = uos_merged.sort_values(by="timestamp_start")

#cutoff data from uos before cutoff date
cutoffdate_traceroute = pd.to_datetime('2023-09-14 15:12:00') # cutoff 2-hop measurements over dedicated link
uos_traceroutes = uos_traceroutes[uos_traceroutes["timestamp_start"] >= cutoffdate_traceroute]

#filter outliers with 1-hop route
uos_traceroutes = uos_traceroutes[uos_traceroutes["hops"] > 2]
twente_traceroutes = twente_traceroutes[twente_traceroutes["hops"] > 2]
outlier = twente_traceroutes[twente_traceroutes["ping_avg"] > 1000]

#filter for only first hop in uos and 2. hop in twente as these represent the bent-pipe
twente_bentpipe = twente_traceroutes[twente_traceroutes["hop"] == 2]
uos_bentpipe = uos_traceroutes[uos_traceroutes["hop"] == 1]

#Normal RTT
print("Normal RTT ...")
#data = [uos_merged["ping_avg"], twente_merged["ping_avg"]]
mean_uos = np.mean(uos_merged["ping_avg"])
std_uos = np.std(uos_merged["ping_avg"])
lb_uos = mean_uos - std_uos
ub_uos = mean_uos + std_uos
mean_twente = np.mean(twente_merged["ping_avg"])
std_twente = np.std(twente_merged["ping_avg"])
lb_twente = mean_twente - std_twente
ub_twente = mean_twente + std_twente
print("median UOS:", np.median(uos_merged["ping_avg"]), "mean:", mean_uos, "std:", std_uos, "lowerbound:", lb_uos, "upperbound:", ub_uos)
print("median Twente:", np.median(twente_merged["ping_avg"]), "mean:", mean_twente, "std:", std_twente, "lowerbound:", lb_twente, "higherbound:", ub_twente)

uos_rtt_in_std = uos_merged[(uos_merged["ping_avg"] <= ub_uos) & (uos_merged["ping_avg"] >= lb_uos)]
twente_rtt_in_std = twente_merged[(twente_merged["ping_avg"] <= ub_twente) & (twente_merged["ping_avg"] >= lb_twente)]
print("Measurements in one std:")
print("UOS:", (uos_rtt_in_std.shape[0] / uos_merged.shape[0]) * 100)
print("Twente:", (twente_rtt_in_std.shape[0] / twente_merged.shape[0]) * 100)

plt.figure(figsize=(3, 2.5))
plt.boxplot([uos_merged["ping_avg"], twente_merged["ping_avg"]], widths=0.5, notch=True, labels=["Osnabrück", "Enschede"])
#plt.xlabel('Hour of the Day')
plt.ylabel('RTT [ms]')
plt.yscale("log")
additional_ticks = [15, 25, 50, 100, 200]
additional_tick_labels = ['15', '25', '50', '100', '200']
plt.yticks(additional_ticks, labels=additional_tick_labels)
plt.tight_layout()
plt.ylim(15, 220)
plt.savefig("Plots/Fig7a.pdf", format="pdf")
plt.close()
#plt.show()

#bent pipe
print("bent-pipe ...")
data = [uos_bentpipe["ping_avg"], twente_bentpipe["ping_avg"]]
mean_uos = np.mean(data[0])
std_uos = np.std(data[0])
lb_uos = mean_uos - std_uos
ub_uos = mean_uos + std_uos
mean_twente = np.mean(data[1])
std_twente = np.std(data[1])
lb_twente = mean_twente - std_twente
ub_twente = mean_twente + std_twente
print("median UOS:", np.median(data[0]), "mean:", mean_uos, "std:", std_uos, "lowerbound:", lb_uos, "upperbound:", ub_uos)
print("median Twente:", np.median(data[1]), "mean:", mean_twente, "std:", std_twente, "lowerbound:", lb_twente, "higherbound:", ub_twente)

uos_rtt_in_std = uos_bentpipe[(uos_bentpipe["ping_avg"] <= ub_uos) & (uos_bentpipe["ping_avg"] >= lb_uos)]
twente_rtt_in_std = twente_bentpipe[(twente_bentpipe["ping_avg"] <= ub_twente) & (twente_bentpipe["ping_avg"] >= lb_twente)]
print("Measurements in one std:")
print("UOS:", (uos_rtt_in_std.shape[0] / uos_bentpipe.shape[0]) * 100)
print("Twente:", (twente_rtt_in_std.shape[0] / twente_bentpipe.shape[0]) * 100)

plt.figure(figsize=(3, 2.5))
plt.boxplot(data, widths=0.5, notch=True, labels=["Osnabrück", "Enschede"])
plt.ylabel('RTT [ms]')
plt.yscale("log")
plt.ylim(15, 220)
# Add additional ticks to the y-axis with labels
additional_ticks = [15, 25, 50, 100, 200]
additional_tick_labels = ['15', '25', '50', '100', '200']
plt.yticks(additional_ticks, labels=additional_tick_labels)

plt.tight_layout()
plt.savefig("Plots/Fig7b.pdf", format="pdf")
plt.close()
#plt.show()
