# WetLinks: a Large-Scale Longitudinal Starlink Dataset with Contiguous Weather Data
This dataset corresponds to the paper "WetLinks: a Large-Scale Longitudinal Starlink Dataset with Contiguous Weather Data" ([https://arxiv.org/abs/2402.16448](https://arxiv.org/abs/2402.16448 "https://arxiv.org/abs/2402.16448"))

Please take a look into the paper for detailed info about the measurement setup, software used, as well as analysis results.

## Structure
- Raw_Data/ - Contains the unfiltered raw measurement data. The .csv files contain the data and the corresponding .txt files contain descriptions of all features.
	- froggit: Weather data from the Froggit DP2000 weather stations placed directly next to the dishes
	- metadata: detailed version information about the software that we used. This includes, e.g., python modules as well as system libraries
	- net_iperf: the iperf throughput measurement results
	- net_ping: the RTT measurements
	- net_traceroute: the traceroute measurements
	- starlink: Starlink metadata provided by the dish
- preprocessing/ - Scripts that do preprocessing steps on the raw data. 
	- throughput_merger.py: Reads the net_iperf.csv file and merges matching measurement entries based on their timestamps. Calculates the mean throughput as well as standard deviation. Then writes the resulting dataframe to a new csv file.
	- csv.merger.py: takes the data from different csv files (net_iperf, net_ping, froggit) and merges them based on their timestamps to one csv can is the input for our analysis.
- Preprocessed_Data/ - Contains the output files from the preprocessing scripts
	- analysis_data: the main file for our analysis. COntains merged throughput, RTT and weather data
	- iperf_cleaned_seconds: contains the second-level iperf measurements. The data is filtered that only measurements running exactly 15 seconds are included. the raw iperf data contains occasional measurements that run significantly longer
	- iperf_cleaned_means: the measurements of iperf_cleaned_seconds are aggregated by their means
- Plotting_Scripts/ - The scripts that create the plots of our paper
- Plots/ - Contains the plots of our paper
- Weather_Data/ - Contains the raw data from DWD (for Osnabrück) and KNMI (for Enschede)

## Citation
D. Laniewski, E. Lanfer, B. Meijerink, R. van Rijswijk-Deij, N. Aschenbruck, "WetLinks: a Large-Scale Longitudinal Starlink Dataset with Contiguous Weather Data," arXiv preprint arXiv:2402.16448, 2024.
```
@article{laniewski2024wetlinks,
  	title={{WetLinks: a Large-Scale Longitudinal Starlink Dataset with Contiguous Weather Data}},
 	author={Laniewski, Dominic and Lanfer, Eric and Meijerink, Bernd and van Rijswijk-Deij, Roland and Aschenbruck, Nils},
  	journal={arXiv preprint arXiv:2402.16448},
  	year={2024}
}
```

## License
This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).