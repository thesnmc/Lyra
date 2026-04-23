# 🏗️ Architecture & Design Document: Lyra Astro-Acoustic Engine
**Version:** 3.1.0 | **Date:** 2026-04-23 | **Author:** [Sujay / thesnmc]

---

## 1. Executive Summary
This document outlines the architecture for Lyra, a multimodal scientific workbench designed to process massive astronomical telemetry and visual datasets. The overarching technical goal is to break the visual bottleneck of modern astronomy by implementing a stateless data pipeline that translates raw astrophysical phenomena (solar wind, exoplanet light curves, gravitational strains) into immersive, spatialized 3D audio, effectively acting as an "acoustic magnifying glass."

## 2. Architectural Drivers
**What forces shaped this architecture?**
* **Primary Goals:** High-fidelity data sonification, modularity for multiple disparate data streams, and automated AI diagnostic reporting for statistical anomalies.
* **Technical Constraints:** Must run entirely locally on a standard machine using Python, requiring zero complex client-side setups or external database dependencies.
* **Non-Functional Requirements (NFRs):** * **Security/Privacy:** API keys (Google Gemini) must be held strictly in volatile memory and never logged or written to disk.
    * **Reliability:** The engine must gracefully handle external API failures (e.g., NOAA timeouts) without crashing the main UI thread.    
    * **Performance:** High-density array math (1500+ data points) must be calculated in fractions of a second using vectorized operations.

## 3. System Architecture (The 10,000-Foot View)

```text
[ External APIs ] ---> (Ingestion Layer) ---> (Domain Layer) ---> (Presentation Layer)
  NOAA / NASA               requests             NumPy / SciPy         Streamlit / Plotly
  Gemini LLM              lightkurve             Math Engine            Hacker UI CSS
```

* **Presentation Layer:** Built with Streamlit, utilizing a unidirectional data flow. The UI state is highly reactive; any change to the sidebar parameters immediately triggers a re-render of the underlying acoustic state.
* **Domain Layer:** Pure Python business logic. Houses the core mathematical normalization algorithms, Z-score anomaly detection, and the Digital Signal Processing (DSP) pipeline that handles granular synthesis.
* **Data/Hardware Layer:** Direct API interceptors mapping JSON/FITS data into standardized Pandas DataFrames and NumPy arrays, completely bypassing standard cloud-syncing databases for a zero-disk footprint.

## 4. Design Decisions & Trade-Offs (The "Why")

* **Decision 1: Streamlit over React/WebAudio API**
    * **Rationale:** Streamlit allows for lightning-fast prototyping and deep, native integration with the Python data science ecosystem (Pandas, SciPy, Lightkurve).
    * **Trade-off:** We sacrifice granular, low-level control over the browser's audio buffer. Instead of streaming audio in true real-time, the engine "batch processes" the audio into a `.wav` file and serves it to the front end.

* **Decision 2: SciPy for Audio Synthesis over a Dedicated Audio Server (SuperCollider)**
    * **Rationale:** Keeps the installation footprint incredibly small. Users only need a standard `pip install` to run the engine, making it highly accessible to citizen scientists.
    * **Trade-off:** CPU-bound synthesis in Python is slower than compiled C++ audio engines, limiting our ability to do zero-latency live scrubbing of the data.

* **Decision 3: Volatile State Management for API Keys**
    * **Rationale:** Adhering to strict security mandates. The Gemini API key is collected via a masked password input and only exists in RAM during runtime.
    * **Trade-off:** The user must manually paste their API key every time they launch the application, but it ensures total security against credential scraping.

## 5. Data Flow & Lifecycle

* **Ingestion:** Raw telemetric data is fetched via REST APIs or file uploads. Streamlit's `@st.cache_data` caches the payload (TTL 3600s) to prevent API rate-limiting.
* **Processing (Math):** The domain layer standardizes the data into NumPy arrays. Z-scores are calculated to identify 2-sigma and 3-sigma events.
* **Processing (Acoustics):** The DSP engine maps physical data (flux/speed) to a frequency domain (Hz) and calculates panning matrices for binaural spatialization using Hanning-windowed granular swarms.
* **Execution/Output:** The visual spectrogram and 3D Plotly charts are injected into the DOM. Simultaneously, if an anomaly was detected, the metadata is serialized and pushed to the Gemini LLM for a plain-English diagnostic report.

## 6. Security & Privacy Threat Model

* **Data at Rest:** No persistent storage. The `.wav` master file is routinely overwritten, and all API keys and telemetry arrays exist only in volatile RAM.
* **Data in Transit:** External connections to NOAA, NASA, and Google use strictly encrypted HTTPS protocols.
* **Mitigated Risks:** * **Malformed Payloads:** We implemented an API Key Sanitization check (regex/prefix matching for `AIza`) to prevent the application from sending malformed requests to Google's servers, mitigating potential IP blacklisting.

## 7. Future Architecture Roadmap

* **Asynchronous Task Queuing:** Transitioning data ingestion to Celery or Redis. Currently, a slow API fetch (like the Vera Rubin broker) blocks the main thread. Decoupling this will allow the UI to remain highly responsive during data pulls.
* **External Audio Server (OSC):** Refactoring the SciPy batch-renderer into an Open Sound Control (OSC) bridge, allowing Lyra to send control voltages to a dedicated C++ SuperCollider server for zero-latency, live audio streaming.
* **Data Version Control (DVC):** Implementing an automated "snapshot" system that records the exact raw data, parameters, and AI diagnostic whenever a 3-sigma anomaly is found, ensuring 100% scientific reproducibility.
