"""
Reads the net_iperf.csv file and merges matching measurement entries based on their timestamps.
Calculates the mean throughput as well as sd.
Then writes the resulting dataframe to a new csv file.
"""

import pandas as pd
import numpy as np

#Read data and create empty dataframes
dirs = ["Osnabrück", "Enschede"]
for dir in dirs:
    print(dir)
    datadir = "Raw_Data/"+dir
    iperf_data = pd.read_csv(datadir + "/net_iperf.csv")

    #convert timestamps to timestamps
    iperf_data["timestamp_start"] = pd.to_datetime(iperf_data["timestamp_start"])
    iperf_data["timestamp_end"] = pd.to_datetime(iperf_data["timestamp_end"])

    #find measurements that belong together, i.e. group the data from 1sec granularity to whatever long a single iperf run takes
    measurement_startindex = 0
    measurements = []  # (startindex, endindex, #measurements)
    for index, row in iperf_data.iterrows():
        if index % 100000 == 0:
            print(index)
        if index == 0:  # skip the very first index
            continue
        else:
            time_diff = (row['timestamp_start'] - iperf_data.iloc[index-1]['timestamp_end']).total_seconds()  # time difference between this measurement and the one directly before. Since iperf outputs data at 1sec intervals, if this is > 1 sec a new measurement has begun
            if time_diff >= 2:  # 2 sec for a small grace period to account for small iperf inaccuracies       
                measurements.append((measurement_startindex, index, index-measurement_startindex))
                measurement_startindex = index
    #append the very last measurement
    measurements.append((measurement_startindex, iperf_data.shape[0]-1, iperf_data.shape[0] - 1 - measurement_startindex))

    print("calculated the measurement indices")
    print("measurements:", len(measurements))

    #create the cleaned and merged csv files
    sitename = iperf_data.iloc[0]["site_name"]
    cleaned_iperf_seconds = pd.DataFrame(columns=iperf_data.columns)
    cleaned_iperf_means = pd.DataFrame()
    counter = 0
    for measurement in measurements:
        counter += 1
        if counter % 10000 == 0:
            print(counter)
        if measurement[2] == 15:  # only consider measurements that lasted for exactly 15 sec, only to increase analysis data quality
            df = iperf_data[measurement[0]:measurement[1]]
            cleaned_iperf_seconds = pd.concat([cleaned_iperf_seconds, df], ignore_index=True, sort=False)

            timestamp_start = df.iloc[0]["timestamp_start"]
            timestamp_end = df.iloc[df.shape[0]-1]["timestamp_end"]
            server = df.iloc[0]["server"]
            ip_protocol = df.iloc[0]["ip_protocol"]
            transport_protocol = df.iloc[0]["transport_protocol"]
            download_mean = df["download"].mean()
            upload_mean = df["upload"].mean()
            download_std = np.std(df["download"])
            upload_std = np.std(df["upload"])
            measurement_steps = df.shape[0]

            cleaned_iperf_means = pd.concat([cleaned_iperf_means, pd.DataFrame([[sitename, timestamp_start, timestamp_end, server, 
                                                                                 ip_protocol, transport_protocol, download_mean, 
                                                                                 download_std, upload_mean, upload_std, measurement_steps]], 
                                                                                 columns=["site_name", "timestamp_start", "timestamp_end", "server", "ip_protocol",
                                                                                          "transport_protocol", "download", "download_std", "upload", "upload_std", "measurement_steps"])], ignore_index=True)

    cleaned_iperf_means.to_csv("Preprocessed_Data/iperf_cleaned_means_"+dir+".csv")
    cleaned_iperf_seconds.to_csv("Preprocessed_Data/iperf_cleaned_seconds_"+dir+".csv")