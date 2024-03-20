import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def create_rain_plot():
    rainyday_start = pd.to_datetime("2023-10-13 00:00:00")
    rainyday_end = pd.to_datetime("2023-10-15 00:00:00")
    rainyday_data = data_cleaned_uos[(data_cleaned_uos["timestamp_start"] >= rainyday_start) & (data_cleaned_uos["timestamp_start"] < rainyday_end)]
    
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(8, 9), sharex=True)
    ax1.plot(rainyday_data["timestamp_start"], rainyday_data["rain"], label="rain")
    ax1.set_ylabel('Rain [mm]')
    ax1.legend(loc="upper right")

    ax2.plot(rainyday_data["timestamp_start"], rainyday_data["download"], color="green", label="download")
    ax2.set_ylabel('Throughput [Mbit/s]')
    ax2.legend(loc="upper right")

    ax3.plot(rainyday_data["timestamp_start"], rainyday_data["upload"], color="red", label="upload")
    ax3.set_ylabel('Throughput [Mbit/s]')
    ax3.legend(loc="upper right")

    ax4.plot(rainyday_data["timestamp_start"], rainyday_data["ping_avg"], color="grey", label="RTT")
    ax4.set_ylabel('RTT [ms]')
    ax4.legend(loc="upper right")

    ax5.plot(rainyday_data["timestamp_start"], rainyday_data["ping_packet_loss"], color="brown", label="packet loss")
    ax5.set_ylabel('Packet Loss [%]')
    ax5.legend(loc="upper right")

    #plt.legend()
    plt.xlabel('Time in MM-DD HH')
    #plt.ylabel('Rain [mm]')
    #plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("Plots/weather_day_uos.pdf", format="pdf")
    plt.close()
    #plt.show()

def correlation_analysis():
    data_keys = ["download", "upload", "ping_packet_loss", "ping_avg", "ping_worst", "ping_best", "ping_stddev", "temp", "humidity", "dewpt", "windchill", "winddir", "windspeed", "windgust", "rain", "solarradiation", "uv", "barom"]
    for data, location in zip([data_cleaned_uos, data_cleaned_twente], ["uos", "twente"]):
        correlation_data = data[data_keys]
        correlation_matrix = correlation_data.corr()
        print(correlation_matrix)

        # Create a heatmap using matplotlib
        fig, ax = plt.subplots(figsize=(7,6))

        # Plot the heatmap
        cax = ax.matshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1)

        # Add a colorbar
        fig.colorbar(cax, label="correlation")

        # Set labels and title
        plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=90)
        plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
        #plt.title('Correlation Matrix')
        plt.tight_layout()
        # Show the plot
        if location == "uos":
            plt.savefig("Plots/Fig9a.pdf", format="pdf")
        else:
            plt.savefig("Plots/Fig9b.pdf", format="pdf")
        #plt.show()
        

#read data
data_uos = pd.read_csv("Preprocessed_Data/analysis_data_Osnabrück.csv")
data_twente = pd.read_csv("Preprocessed_Data/analysis_data_Enschede.csv")

#convert timing information to datetimes
data_uos["timestamp_start"] = pd.to_datetime(data_uos["timestamp_start"])
data_uos["timestamp_end"] = pd.to_datetime(data_uos["timestamp_end"])
data_twente["timestamp_start"] = pd.to_datetime(data_twente["timestamp_start"])
data_twente["timestamp_end"] = pd.to_datetime(data_twente["timestamp_end"])

#convert throughputs to Mbit/s
modifier = 1e6
data_uos["download"] = data_uos["download"] / modifier
data_uos["download_std"] = data_uos["download_std"] / modifier
data_uos["upload"] = data_uos["upload"] / modifier
data_uos["upload_std"] = data_uos["upload_std"] / modifier

data_twente["download"] = data_twente["download"] / modifier
data_twente["download_std"] = data_twente["download_std"] / modifier
data_twente["upload"] = data_twente["upload"] / modifier
data_twente["upload_std"] = data_twente["upload_std"] / modifier

#clean data
data_cleaned_uos = data_uos.dropna()
data_cleaned_twente = data_twente.dropna()

data_cleaned_twente = data_cleaned_twente[data_cleaned_twente["windspeed"] >= 0]
data_cleaned_uos = data_cleaned_uos[data_cleaned_uos["windspeed"] >= 0]

#create_rain_plot()
correlation_analysis()
