# 🚀 Lyra: Astro-Acoustic Engine
> A multimodal research workbench translating complex deep-space telemetry into immersive, 3D-spatialized audio to break the visual bottleneck of modern astronomy.

[![License]()](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Web%20%7C%20Python-lightgrey)]()
[![Architecture](https://img.shields.io/badge/Architecture-Data%20Sonification-success)]()

---

## 📖 Overview
Modern telescopes generate terabytes of data nightly, and the human eye is easily overwhelmed by visual noise. Lyra bypasses this bottleneck by utilizing the human ear's natural superiority in pattern recognition. By converting complex digital signals from deep space into high-fidelity sound, Lyra unlocks a new "sensory bandwidth" for detecting patterns—like rhythmic planetary transits or gravitational wave "chirps"—that are often lost in messy, unreadable visual static.

Unlike static audio clips released for public outreach, Lyra is a fully interactive, scriptable engine. It allows researchers to map multi-parameters (e.g., starlight flux to pitch, solar wind density to volume) and explore datasets in real-time. To bridge the gap between raw data and human understanding, the engine integrates a True AI Science Officer powered by Google Gemini, which mathematically monitors data streams and generates plain-English diagnostic reports of cosmic events.

**The Core Mandate:** Radical accessibility and multidimensional interpretation. Lyra treats digital access to scientific information as a human right, specifically bridging the gap for Blind and Low Vision (BLV) researchers, while simultaneously providing sighted researchers a more intuitive understanding of complex physics through binaural 3D spatialization.

## ✨ Key Features
* **Multi-Source Telemetry Routing:** Instant access to Live NOAA Solar Wind, Kepler-69 exoplanet light curves, and LIGO Gravitational Wave (GW150914) mathematical models.
* **Acoustic Magnifying Glass (Radar Scan):** An interactive targeting system that allows users to upload JWST/HST galaxy images, use X/Y crosshairs to target specific star clusters, and sonify the matrix column-average luminosity.
* **Cinematic Granular Synthesis:** A high-performance spatial audio engine generating true stereo `.wav` files. Includes Sine, Square, Sawtooth, and a custom Hanning-windowed Granular Swarm patch for sci-fi textures.
* **True AI Science Officer:** Automated mathematical anomaly detection (monitoring for 3-sigma spikes/dips). Integrates a "Dynamic Model Radar" to ping the Google Gemini API for real-time scientific reporting.
* **Hacker Terminal UI:** A custom CSS-injected command center featuring neon Plotly oscilloscopes, acoustic spectrograms, and a 3D interactive singularity strain visualizer.

## 🛠️ Tech Stack
* **Language:** Python (3.10+)
* **Framework:** Streamlit (Reactive Web UI)
* **Environment:** VS Code / Local Virtual Environment
* **Key Libraries/APIs:** * `SciPy` & `NumPy` (Digital Signal Processing & Audio Synthesis)
  * `Plotly` (Interactive 2D/3D Data Visualization)  
  * `Lightkurve` & `Requests` (NASA/NOAA Data Ingestion)  
  * `google-generativeai` (Gemini 1.5 Flash API for Diagnostics)

## ⚙️ Architecture & Data Flow
Lyra operates on a decoupled data-to-audio processing pipeline designed to handle high-density scientific arrays without blocking the main UI thread.

* **Input:** Data streams are intercepted via REST APIs (NOAA), Python packages (Kepler), mathematical functions (LIGO), or direct user upload (Images/Custom CSVs), and standardized into NumPy arrays.
* **Processing:** The math engine normalizes parameters, calculates Z-scores to identify statistical anomalies, and applies a Hanning-windowed mapping of physical data (flux/speed) to a frequency/amplitude domain.
* **Output:** SciPy synthesizes stereo channels point-by-point to render a spatialized `.wav` file alongside visual spectrograms. If an anomaly is triggered, the metadata is pushed to the Gemini LLM for diagnostic output.

## 🔒 Privacy & Data Sovereignty
* **Data Collection:** Zero telemetry. Lyra does not collect, log, or track user activity.
* **Permissions Required:** Network access is required solely for fetching external space API data and communicating with the Google Gemini LLM. Local file access is only required if the user uploads custom CSVs or images.
* **Cloud Connectivity:** The core audio synthesis, UI, and mathematical engines run **100% locally on your machine**. Cloud connectivity is strictly limited to the external data fetch requests and the optional AI Science Officer diagnostic pings.

## 🚀 Getting Started

### Prerequisites
* Minimum OS: Windows 10/11, macOS, or Linux.
* Required runtime: Python 3.10 or higher.
* A free Gemini API Key from [Google AI Studio](https://aistudio.google.com/) (Required only for the AI Science Officer feature).

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/Lyra.git](https://github.com/yourusername/Lyra.git)
   ```

2. **Open the project in your IDE and navigate to the directory:**
   ```bash
   cd Lyra
   ```

3. **Install the required dependencies:**
   ```bash
   python -m pip install streamlit numpy pandas requests lightkurve scipy plotly pillow google-generativeai
   ```

4. **Build and run the local web server:**
   ```bash
   python -m streamlit run lyra_core.py
   ```

## 🤝 Contributing
Contributions, issues, and feature requests are highly welcome! We are actively looking to expand the engine's capabilities with real-time alert brokers (LSST/ZTF), VR mode overlays, and Csound/SuperCollider integration. Feel free to check the issues page if you want to contribute to the Astro-Acoustic frontier.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.  
Built by an independent developer in Chennai, India.
