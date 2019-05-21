# random-gnuradio-stuff
Random GNURadio stuff. Bunch of unfinished / dirty code fragments.

Have nothing really useful here (just for personal research), but take 'em if you want - under GPL v3.0 license (one that GNURadio project uses - since I may copy & paste source codes from the main GNU Radio repository).

* hackrf_tx_white_noise.grc: Transmits a Gaussian-noise like signal using HackRF (or with any Osmocom source).

* hackrf_tx-cw.grc: Transmits a sine wave (or cosine wave) using HackRF (or with any Osmocom source).

* Qt-FFT-*: PSD estimates plotter (using USRP2/RTL-SDR/PlutoSDR/HackRF). Similar to osmocom_fft or UHD_FFT. Uses Qt Frequency Sink or Fosphor.

* HackRF-IQ-Collector: A simple shell script for collecting I-Q data with HackRF. Not really GNURadio-ish.

* Cityscape-Related: Cityscape (cityscape.cloudapp.net) related stuff. Not necessarily GNURadio-ish scripts. 

* cal: Amplitude calibration data for USRP B210 and HackRF. Based on David Aragon's SDR Calibrator (github.com/dave-aragon/sdr-calibrator)

* blocks: GNU Radio blocks

	* vector_slicer: slices a input vector, and outputs only a part of the sliced vector.

	* fftshift: applies fftshift() to the input vector, so as the FFT data will be orderd from -pi to pi instead of 0 to 2pi.
	* vector_average: vector moving average (for older version of GNU Radio).
	* wav_file_squelch: removes "zeros" from a wav file (part of the wav file which does not actually contain audio). Very crude and slow.

* AoA: A simple phase-difference angle of arrival flowgraph.  Incomplete.

* 1ms-psd: Takes a moving window periodogram (FFT -> Mag^2 -> log10), and dumps the results into a data file. A simple data file parser is included.
