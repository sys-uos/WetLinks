import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

twente_data = pd.read_csv("Preprocessed_Data/analysis_data_Enschede.csv")
uos_data = pd.read_csv("Preprocessed_Data/analysis_data_Osnabrück.csv")

twente_data["download"] = twente_data["download"]/1e6
twente_data["upload"] = twente_data["upload"]/1e6
uos_data["download"] = uos_data["download"]/1e6
uos_data["upload"] = uos_data["upload"]/1e6

twente_data["timestamp_start"] = pd.to_datetime(twente_data["timestamp_start"])
twente_data["timestamp_end"] = pd.to_datetime(twente_data["timestamp_end"])
uos_data["timestamp_start"] = pd.to_datetime(uos_data["timestamp_start"])
uos_data["timestamp_end"] = pd.to_datetime(uos_data["timestamp_end"])

twente_data = twente_data.dropna(subset=["download", "upload"])
uos_data = uos_data.dropna(subset=["download", "upload"])

plt.figure(figsize=(3, 2.5))
plt.boxplot([uos_data["download"], twente_data["download"]], widths=0.5, notch=True, labels=["Osnabrück", "Enschede"])
plt.ylabel('Throughput [Mbit/s]')
plt.tight_layout()
plt.savefig("Plots/Fig4a.pdf", format="pdf")
plt.close()
#plt.show()

plt.figure(figsize=(3, 2.5))
plt.boxplot([uos_data["upload"], twente_data["upload"]], widths=0.5, notch=True, labels=["Osnabrück", "Enschede"])
plt.ylabel('Throughput [Mbit/s]')
plt.tight_layout()
plt.savefig("Plots/Fig4b.pdf", format="pdf")
plt.close()

#print some data
print("-------Download-------")
print("UOS:", "Mean:",np.mean(uos_data["download"]), "Median:", np.median(uos_data["download"]), "25-percentile:", np.percentile(uos_data["download"], 25), "75-percentile:", np.percentile(uos_data["download"], 75))
print("TWT:", "Mean:",np.mean(twente_data["download"]), "Median:", np.median(twente_data["download"]), "25-percentile:", np.percentile(twente_data["download"], 25), "75-percentile:", np.percentile(twente_data["download"], 75))
print("-------Upload-------")
print("UOS:", "Mean:",np.mean(uos_data["upload"]), "Median:", np.median(uos_data["upload"]), "25-percentile:", np.percentile(uos_data["upload"], 25), "75-percentile:", np.percentile(uos_data["upload"], 75))
print("TWT:", "Mean:",np.mean(twente_data["upload"]), "Median:", np.median(twente_data["upload"]), "25-percentile:", np.percentile(twente_data["upload"], 25), "75-percentile:", np.percentile(twente_data["upload"], 75))
# y=1