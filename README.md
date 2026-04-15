# Lyra: Astro-Acoustic Discovery Engine 🌌🔭

Lyra is a Python-based sonification workbench that translates multi-dimensional astrophysical data into immersive 3D audio. 

Historically, astronomy has relied heavily on visual data. Lyra unlocks a new "sensory bandwidth," utilizing mathematical parameter mapping and binaural spatialization to help researchers "listen" to the cosmos and detect statistical anomalies that might be invisible in standard graphs.

## Features
* **Live Telemetry Sonification:** Streams real-time solar wind plasma data from NOAA's DSCOVR satellite.
* **Exoplanet Transit Detection:** Analyzes Kepler space telescope light curves.
* **3D Binaural Audio:** Calculates phase and amplitude panning to place data in physical space around the listener's head.
* **AI Science Officer:** Actively calculates rolling Z-Scores to flag 3-sigma anomalies (like Coronal Mass Ejections or planetary transits) in real-time.
* **Multiple Synth Patches:** Toggle between Sine, Square, and Sawtooth wave generators.

## Installation
To run Lyra on your local machine, you need Python installed. 

1. Clone or download this repository.
2. Open your terminal and install the required dependencies:
   ```bash
   pip install -r requirements.txt
3. Boot the Lyra engine:

Bash
streamlit run lyra_core.py
Usage
Once the local server boots, a web interface will open in your browser.

Select your Astrophysical Target from the sidebar.

Adjust the Pitch and Playback Speed to your liking.

Put on headphones (required for 3D spatialization).

Click Generate & Play 3D Audio.