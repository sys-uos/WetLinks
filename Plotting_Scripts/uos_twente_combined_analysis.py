"""
Analyzes the datasets of twente and uos together
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import statsmodels.api as sm


def packetloss_analysis():
    number_measurements_with_loss_twente = twente_data[twente_data["ping_packet_loss"] > 0]
    twente_measurements = twente_data.shape[0]
    twente_measurements_with_loss = number_measurements_with_loss_twente.shape[0]
    percent_measurements_with_loss_twente = (twente_measurements_with_loss/twente_measurements)*100 
    
    number_measurements_with_loss_uos = uos_data[uos_data["ping_packet_loss"] > 0]
    uos_measurements = uos_data.shape[0]
    uos_measurements_with_loss = number_measurements_with_loss_uos.shape[0]
    percent_measurements_with_loss_uos = (uos_measurements_with_loss/uos_measurements)*100

    print("uos measurements with loss:", percent_measurements_with_loss_uos, "mean PLR:", number_measurements_with_loss_uos["ping_packet_loss"].mean(), "std PLR:", number_measurements_with_loss_uos["ping_packet_loss"].std(), "min PLR:", number_measurements_with_loss_uos["ping_packet_loss"].min(), "max PLR:", number_measurements_with_loss_uos["ping_packet_loss"].max())
    print("twente measurements with loss:", percent_measurements_with_loss_twente, "mean PLR:", number_measurements_with_loss_twente["ping_packet_loss"].mean(), "std PLR:", number_measurements_with_loss_twente["ping_packet_loss"].std(), "min PLR:", number_measurements_with_loss_twente["ping_packet_loss"].min(), "max PLR:", number_measurements_with_loss_twente["ping_packet_loss"].max())
    
    a = twente_data[twente_data["ping_packet_loss"] == 0.4].shape[0]

    PLR04_twente = (twente_data[twente_data["ping_packet_loss"] == 0.4].shape[0] / number_measurements_with_loss_twente.shape[0]) * 100
    PLR04_uos = (uos_data[uos_data["ping_packet_loss"] == 0.4].shape[0] / number_measurements_with_loss_uos.shape[0]) * 100
    print(PLR04_uos, "% of the Measurements with packet loss at UOS are with 0.4%")
    print(PLR04_twente, "% of the Measurements with packet loss at Twente are with 0.4%")

    PLR1_twente = (twente_data[(twente_data["ping_packet_loss"] > 0) & (twente_data["ping_packet_loss"] < 1.0) ].shape[0] / number_measurements_with_loss_twente.shape[0]) * 100
    PLR1_uos = (uos_data[(uos_data["ping_packet_loss"] > 0) & (uos_data["ping_packet_loss"] < 1.0)].shape[0] / number_measurements_with_loss_uos.shape[0]) * 100
    print(PLR1_uos, "% of the Measurements with packet loss at UOS are with < 1%")
    print(PLR1_twente, "% of the Measurements with packet loss at Twente are with < 1%")

    PLR5_twente = (twente_data[twente_data["ping_packet_loss"] >= 5.0].shape[0] / number_measurements_with_loss_twente.shape[0]) * 100
    PLR5_uos = (uos_data[uos_data["ping_packet_loss"] >= 5.0].shape[0] / number_measurements_with_loss_uos.shape[0]) * 100
    print(PLR5_uos, "% of the Measurements with packet loss at UOS are with >=5%")
    print(PLR5_twente, "% of the Measurements with packet loss at Twente are with >=5%")

    # plot course of multiple days

    day_start = pd.to_datetime("2023-10-25 00:00:00")
    day_end = pd.to_datetime("2023-10-26 00:00:00")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 3), sharex=True)

    day_data_twente = twente_data[(twente_data["timestamp_start"] >= day_start) & (twente_data["timestamp_start"] < day_end)]
    day_data_uos = uos_data[(uos_data["timestamp_start"] >= day_start) & (uos_data["timestamp_start"] < day_end)]
    ax1.plot(day_data_uos["timestamp_start"], day_data_uos["ping_packet_loss"], label="Osnabrück")
    ax1.legend(loc="upper right")
    ax1.set_ylabel('PLR [%]')
    ax1.set_ylim(0,10)
    #ax1.set_xlabel('Time in MM-DD HH')

    ax2.plot(day_data_twente["timestamp_start"], day_data_twente["ping_packet_loss"], color="orange", label="Enschede")
    ax2.legend(loc="upper right")
    ax2.set_ylabel('PLR [%]')
    ax2.set_ylim(0, 10)
    plt.xlabel('Time in MM-DD HH')
    plt.tight_layout()
    #ax1.legend(loc="upper right")
    plt.savefig("Plots/Fig5.pdf", format="pdf")
    plt.close()
    #plt.show()

    #plot ecdfs of the packet loss to see how severe they are 
    #Calculate the ECDF
    twente_ecdf = sm.distributions.ECDF(number_measurements_with_loss_twente["ping_packet_loss"])
    uos_ecdf = sm.distributions.ECDF(number_measurements_with_loss_uos["ping_packet_loss"])
    # Generate x values between the minimum and maximum of the data
    x_values = np.linspace(0, 15, num=1000)

    # Calculate the y values of the ECDF
    twente_y_values = twente_ecdf(x_values)
    uos_y_values = uos_ecdf(x_values)
    # Plot the ECDF
    plt.step(x_values, uos_y_values, label='Osnabrück')
    plt.step(x_values, twente_y_values, label='Enschede')
    plt.xlim(0,15)
    # Add labels and title
    plt.xlabel('Packet Loss Rate (PLR) [%]')
    plt.ylabel('ECDF')

    # Show the plot
    plt.legend()
    plt.tight_layout()
    #plt.show()
    plt.savefig("Plots/Fig6.pdf", format="pdf")

def daytime_analysis():
    twente_data["hour"] = twente_data["timestamp_start"].dt.hour
    uos_data["hour"] = uos_data["timestamp_start"].dt.hour

    #Create bins for every hour and plot boxplots over the course of a day
    download_data_by_hour_twente = [twente_data[twente_data['hour'] == hour]['download'].values for hour in range(24)]
    download_data_by_hour_uos = [uos_data[uos_data['hour'] == hour]['download'].values for hour in range(24)]
    upload_data_by_hour_twente = [twente_data[twente_data['hour'] == hour]['upload'].values for hour in range(24)]
    upload_data_by_hour_uos = [uos_data[uos_data['hour'] == hour]['upload'].values for hour in range(24)]
    rtt_by_hour_twente = [twente_data[twente_data['hour'] == hour]['ping_avg'].values for hour in range(24)]
    rtt_by_hour_uos = [uos_data[uos_data['hour'] == hour]['ping_avg'].values for hour in range(24)]
    
    loss_twente = twente_data[twente_data["ping_packet_loss"] > 0]
    loss_uos = uos_data[uos_data["ping_packet_loss"] > 0]
    loss_by_hour_twente = [loss_twente[loss_twente['hour'] == hour]['ping_packet_loss'].values for hour in range(24)] 
    loss_by_hour_uos = [loss_uos[loss_uos['hour'] == hour]['ping_packet_loss'].values for hour in range(24)] 

    #download analysis
    print("-----Download Analysis-----")
    print("\t UOS \t Twente")
    for i in range(24):
        print(i, "\t", np.median(download_data_by_hour_uos[i]), "\t", np.median(download_data_by_hour_twente[i]))
    
    #upload analysis
    print("-----Upload Analysis-----")
    print("\t UOS \t Twente")
    for i in range(24):
        print(i, "\t", np.median(upload_data_by_hour_uos[i]), "\t", np.median(upload_data_by_hour_twente[i]))

    #RTT analysis
    print("-----RTT Analysis-----")
    print("\t UOS \t Twente")
    for i in range(24):
        print(i, "\t", np.median(rtt_by_hour_uos[i]), "\t", np.median(rtt_by_hour_twente[i]))
    
    #Loss analysis
    print("-----Loss Analysis-----")
    print("\t UOS \t Twente")
    for i in range(24):
        print(i, "\t", np.median(loss_by_hour_uos[i]), "\t", np.median(loss_by_hour_twente[i]))

    def plot_throughput(data, filename, ul, twente):
        plt.figure(figsize=(6, 3))
        boxes = plt.boxplot(data, notch=True, labels=[f'{hour}' for hour in range(24)], patch_artist=True)
        plt.xlabel('Hour of the Day')
        plt.ylabel('Throughput [Mbit/s]')

        if ul:
            plt.ylim(-2, 55)
        else:
            plt.ylim(-15, 450)
        
        #color the boxes
        if not ul and not twente:
            [box.set(facecolor='burlywood') for box in boxes['boxes'][0:6]]
            [box.set(facecolor='cadetblue') for box in boxes['boxes'][6:16]]
            [box.set(facecolor='slategrey') for box in boxes['boxes'][16:21]]
        elif not ul and twente:
            [box.set(facecolor='burlywood') for box in boxes['boxes'][0:6]]
            [box.set(facecolor='cadetblue') for box in boxes['boxes'][6:17]]
            [box.set(facecolor='slategrey') for box in boxes['boxes'][17:22]]
        elif ul and not twente:
            [box.set(facecolor='burlywood') for box in boxes['boxes'][0:6]]
            [box.set(facecolor='cadetblue') for box in boxes['boxes'][6:]]
        elif ul and twente:
            [box.set(facecolor='burlywood') for box in boxes['boxes'][0:6]]
            [box.set(facecolor='cadetblue') for box in boxes['boxes'][6:]]

        plt.tight_layout()
        plt.savefig("Plots/"+filename, format="pdf")
        plt.close()
        #plt.show()

    plot_throughput(download_data_by_hour_twente, "Fig8b.pdf", False, True)
    plot_throughput(download_data_by_hour_uos, "Fig8a.pdf", False, False)
    plot_throughput(upload_data_by_hour_twente, "Fig8d.pdf", True, True)
    plot_throughput(upload_data_by_hour_uos, "Fig8c.pdf", True, False)

twente_data = pd.read_csv("Preprocessed_Data/analysis_data_Enschede.csv")
uos_data = pd.read_csv("Preprocessed_Data/analysis_data_Osnabrück.csv")

merged = pd.concat([uos_data, twente_data], ignore_index=True)

twente_data["download"] = twente_data["download"]/1e6
twente_data["upload"] = twente_data["upload"]/1e6
uos_data["download"] = uos_data["download"]/1e6
uos_data["upload"] = uos_data["upload"]/1e6

twente_data["timestamp_start"] = pd.to_datetime(twente_data["timestamp_start"])
twente_data["timestamp_end"] = pd.to_datetime(twente_data["timestamp_end"])
uos_data["timestamp_start"] = pd.to_datetime(uos_data["timestamp_start"])
uos_data["timestamp_end"] = pd.to_datetime(uos_data["timestamp_end"])

twente_data = twente_data.dropna()
uos_data = uos_data.dropna()


packetloss_analysis()
daytime_analysis()
