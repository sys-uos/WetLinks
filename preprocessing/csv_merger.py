"""
reads all the different csv files and merges them into one for further analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

#read the data
dirs = ["Osnabrück", "Enschede"]
for dir in dirs:
    raw_datadir = "Raw_Data/"+dir+"/"
    preprocessed_datadir = "Preprocessed_Data/"
    iperf_data = pd.read_csv(preprocessed_datadir + "iperf_cleaned_means_"+dir+".csv")
    ping_data = pd.read_csv(raw_datadir + "net_ping.csv")
    froggit_data = pd.read_csv(raw_datadir + "froggit.csv")
    traceroute_data = pd.read_csv(raw_datadir + "net_traceroute.csv")
    starlink_data = pd.read_csv(raw_datadir + "starlink.csv")

    #convert timestamps
    iperf_data["timestamp_start"] = pd.to_datetime(iperf_data["timestamp_start"])
    iperf_data["timestamp_end"] = pd.to_datetime(iperf_data["timestamp_end"])
    ping_data["timestamp_start"] = pd.to_datetime(ping_data["timestamp_start"], format='ISO8601')
    ping_data["timestamp_end"] = pd.to_datetime(ping_data["timestamp_end"], format='ISO8601')
    froggit_data["timestamp"] = pd.to_datetime(froggit_data["timestamp"])
    traceroute_data["timestamp_start"] = pd.to_datetime(traceroute_data["timestamp_start"])
    traceroute_data["timestamp_end"] = pd.to_datetime(traceroute_data["timestamp_end"])
    starlink_data["timestamp"] = pd.to_datetime(starlink_data["timestamp"])

    #cut data for twente to speed processing up significantly
    if dir == "twente":
        cutoffdate = iperf_data.iloc[iperf_data.shape[0]-1]["timestamp_end"]
        froggit_data = froggit_data[froggit_data["timestamp"] <= cutoffdate]
        ping_data = ping_data[ping_data["timestamp_end"] <= cutoffdate]

    max_acceptable_timediff = 600  # 10min
    #search the matching ping measurement and weather measurement for each throughput measurement
    for index_iperf, row_iperf in iperf_data.iterrows():
        if index_iperf % 1000 == 0:
           print(index_iperf)
        #print(index_iperf)
        #merge the pings
        closest_ping = ping_data.loc[(ping_data["timestamp_start"] - row_iperf["timestamp_end"]).abs().idxmin()] #finds the closest entry based on time
        timediff = (closest_ping["timestamp_start"] - row_iperf["timestamp_end"]).total_seconds()
        if timediff <= max_acceptable_timediff:
            iperf_data.loc[index_iperf, "ping_target"] = closest_ping["target"]
            iperf_data.loc[index_iperf, "ping_ip_protocol"] = closest_ping["ip_protocol"]
            iperf_data.loc[index_iperf, "ping_packet_loss"] = closest_ping["packet_loss"]
            iperf_data.loc[index_iperf, "ping_packets_send"] = closest_ping["packets_send"]
            iperf_data.loc[index_iperf, "ping_avg"] = closest_ping["ping_avg"]
            iperf_data.loc[index_iperf, "ping_worst"] = closest_ping["ping_worst"]
            iperf_data.loc[index_iperf, "ping_best"] = closest_ping["ping_best"]
            iperf_data.loc[index_iperf, "ping_stddev"] = closest_ping["ping_stddev"]
        else:
            iperf_data.loc[index_iperf, "ping_target"] = np.nan
            iperf_data.loc[index_iperf, "ping_ip_protocol"] = np.nan
            iperf_data.loc[index_iperf, "ping_packet_loss"] = np.nan
            iperf_data.loc[index_iperf, "ping_packets_send"] = np.nan
            iperf_data.loc[index_iperf, "ping_avg"] = np.nan
            iperf_data.loc[index_iperf, "ping_worst"] = np.nan
            iperf_data.loc[index_iperf, "ping_best"] = np.nan
            iperf_data.loc[index_iperf, "ping_stddev"] = np.nan
        
        #merge the weather data
        timestamp = row_iperf["timestamp_start"]
        diff_df = (froggit_data["timestamp"] - row_iperf["timestamp_start"]).abs()
        smallest_indices = np.argsort(diff_df)[:3]
        closest_weatherdatas = froggit_data.loc[smallest_indices]
        diffs = (closest_weatherdatas["timestamp"] - row_iperf["timestamp_start"]).abs()
        larger = False
        for dif in diffs:
            if dif.total_seconds() > max_acceptable_timediff:
                larger = True
        if not larger:
            iperf_data.loc[index_iperf, "temp"] = closest_weatherdatas["temp"].mean()
            iperf_data.loc[index_iperf, "humidity"] = closest_weatherdatas["humidity"].mean()
            iperf_data.loc[index_iperf, "dewpt"] = closest_weatherdatas["dewpt"].mean()
            iperf_data.loc[index_iperf, "windchill"] = closest_weatherdatas["windchill"].mean()
            iperf_data.loc[index_iperf, "winddir"] = closest_weatherdatas["winddir"].mean()
            iperf_data.loc[index_iperf, "windspeed"] = closest_weatherdatas["windspeed"].mean()
            iperf_data.loc[index_iperf, "windgust"] = closest_weatherdatas["windgust"].mean()
            iperf_data.loc[index_iperf, "rain"] = closest_weatherdatas["rain"].mean()
            iperf_data.loc[index_iperf, "solarradiation"] = closest_weatherdatas["solarradiation"].mean()
            iperf_data.loc[index_iperf, "uv"] = closest_weatherdatas["uv"].mean()
            iperf_data.loc[index_iperf, "barom"] = closest_weatherdatas["barom"].mean()
        else:
            iperf_data.loc[index_iperf, "temp"] = np.nan
            iperf_data.loc[index_iperf, "humidity"] = np.nan
            iperf_data.loc[index_iperf, "dewpt"] = np.nan
            iperf_data.loc[index_iperf, "windchill"] = np.nan
            iperf_data.loc[index_iperf, "winddir"] = np.nan
            iperf_data.loc[index_iperf, "windspeed"] = np.nan
            iperf_data.loc[index_iperf, "windgust"] = np.nan
            iperf_data.loc[index_iperf, "rain"] = np.nan
            iperf_data.loc[index_iperf, "solarradiation"] = np.nan
            iperf_data.loc[index_iperf, "uv"] = np.nan
            iperf_data.loc[index_iperf, "barom"] = np.nan

    iperf_data.to_csv(preprocessed_datadir+"analysis_data_"+dir+".csv", index=False)