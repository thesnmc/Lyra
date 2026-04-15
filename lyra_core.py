import numpy as np
import streamlit as st
import pandas as pd
import requests
import lightkurve as lk
from scipy.io import wavfile
from scipy import signal
import plotly.graph_objects as go # NEW: For the glowing interactive charts

# 1. Setup the UI Layout
st.set_page_config(page_title="Lyra Command Center", layout="wide")

# --- HACKER TERMINAL CSS INJECTION ---
st.markdown("""
<style>
    /* Deep space black background and hacker green text */
    .stApp {
        background-color: #050505;
        color: #00ff41;
        font-family: 'Courier New', Courier, monospace;
    }
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #00ff41 !important;
        text-shadow: 0px 0px 5px #00ff41;
    }
    /* Hide standard Streamlit UI elements to make it look like standalone software */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Style the sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #00ff41;
    }
</style>
""", unsafe_allow_html=True)

st.title("LYRA: ASTRO-ACOUSTIC ENGINE v2.0")
st.markdown("---")

# --- DATA PIPELINES ---
@st.cache_data(ttl=3600) 
def load_solar_wind():
    url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data[1:], columns=data[0]).dropna()
    df['density'] = pd.to_numeric(df['density'], errors='coerce')
    df['speed'] = pd.to_numeric(df['speed'], errors='coerce')
    return df.dropna()

@st.cache_data
def load_kepler():
    search_result = lk.search_lightcurve('KIC 8692861', author='Kepler', quarter=15)
    lc = search_result.download().remove_nans()
    return np.array(lc.flux.value, dtype=float)[:1500] 

# --- HELPER: NEON CHART BUILDER ---
def plot_neon_chart(y_data, title, y_label):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=y_data, mode='lines', line=dict(color='#00ff41', width=2)))
    fig.update_layout(
        title=title,
        paper_bgcolor='#050505',
        plot_bgcolor='#050505',
        font=dict(color='#00ff41', family='Courier New'),
        xaxis=dict(showgrid=True, gridcolor='#1a1a1a', title="Time (Frames)"),
        yaxis=dict(showgrid=True, gridcolor='#1a1a1a', title=y_label),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- SIDEBAR: THE WORKBENCH CONTROLS ---
st.sidebar.header("1. Target Selection")
data_source = st.sidebar.selectbox("Astrophysical Target", [
    "NOAA Live Solar Wind", 
    "Kepler-69 Exoplanet",
    "LIGO Gravitational Wave (GW150914 Model)", 
    "Upload Custom CSV"
])

st.sidebar.header("2. Synthesizer Patch")
instrument = st.sidebar.selectbox("Sound Profile", [
    "Sine Wave (Smooth & Haunting)", 
    "Square Wave (8-Bit & Glitchy)", 
    "Sawtooth Wave (Aggressive & Buzzy)",
    "Cinematic Granular Swarm (Sci-Fi Texture)" 
])

st.sidebar.header("3. Sonification Controls")
playback_speed = st.sidebar.slider("Playback Speed (ms per point)", 5, 100, 20)
f_min = st.sidebar.slider("Base Pitch (Hz)", 50, 500, 150)
f_max = st.sidebar.slider("Peak Pitch (Hz)", 500, 2000, 800)

st.sidebar.header("4. Science Officer")
enable_ai = st.sidebar.checkbox("Enable Anomaly Detection", value=True)

# --- ROUTING THE DATA ---
st.write(f"### [ SYSTEM INTERCEPT ]: {data_source}")

if data_source == "NOAA Live Solar Wind":
    df_solar = load_solar_wind()
    data_array = df_solar['speed'].values
    volume_array = df_solar['density'].values
    plot_neon_chart(data_array, "LIVE TELEMETRY: SOLAR WIND SPEED", "km/s")
    y_label = "km/s"

elif data_source == "Kepler-69 Exoplanet":
    data_array = load_kepler()
    volume_array = np.full_like(data_array, 0.5) 
    plot_neon_chart(data_array, "ARCHIVE RECORD: STARLIGHT FLUX", "Photons")
    y_label = "photons"

elif data_source == "LIGO Gravitational Wave (GW150914 Model)":
    x = np.linspace(0, 4, 1500)
    data_array = np.exp(x) 
    volume_array = np.exp(x) / np.exp(4) 
    
    # SPECIAL 3D VISUALIZER FOR THE BLACK HOLE
    st.write("#### 3D SINGULARITY STRAIN VISUALIZER")
    z_3d = np.linspace(0, 10, 1500)
    x_3d = data_array * np.cos(z_3d * 10)
    y_3d = data_array * np.sin(z_3d * 10)
    
    fig3d = go.Figure(data=[go.Scatter3d(
        x=x_3d, y=y_3d, z=z_3d, mode='lines', 
        line=dict(color=data_array, colorscale='Viridis', width=4)
    )])
    fig3d.update_layout(
        paper_bgcolor='#050505',
        scene=dict(bgcolor='#050505', xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False)),
        margin=dict(l=0, r=0, t=0, b=0),
        height=500
    )
    st.plotly_chart(fig3d, use_container_width=True)
    y_label = "Hz Strain"

else:
    uploaded_file = st.file_uploader("UPLOAD EXTERNAL DATABANK (CSV)", type="csv")
    if uploaded_file is not None:
        df_custom = pd.read_csv(uploaded_file)
        
        col1, col2 = st.columns(2)
        with col1:
            pitch_col = st.selectbox("MAP TO FREQUENCY (PITCH)", df_custom.columns)
        with col2:
            vol_options = ["Constant Volume"] + list(df_custom.columns)
            vol_col = st.selectbox("MAP TO AMPLITUDE (VOLUME)", vol_options)
            
        df_custom[pitch_col] = pd.to_numeric(df_custom[pitch_col], errors='coerce')
        df_custom = df_custom.dropna(subset=[pitch_col])
        data_array = df_custom[pitch_col].values
        
        if vol_col == "Constant Volume":
            volume_array = np.full_like(data_array, 0.5)
        else:
            df_custom[vol_col] = pd.to_numeric(df_custom[vol_col], errors='coerce').fillna(0.5)
            volume_array = df_custom[vol_col].values
            
        plot_neon_chart(data_array, f"CUSTOM DATASTREAM: {pitch_col.upper()}", pitch_col)
        y_label = pitch_col
    else:
        st.error("[ WAITING FOR FILE UPLOAD ]")
        st.stop() 

# --- THE AI SCIENCE OFFICER ---
if enable_ai:
    st.markdown("---")
    st.markdown("### 🤖 [ SCIENCE OFFICER LOG ]")
    
    mean_val = np.mean(data_array)
    std_dev = np.std(data_array)
    
    if std_dev > 0:
        max_val = np.max(data_array)
        min_val = np.min(data_array)
        z_score_max = (max_val - mean_val) / std_dev
        z_score_min = (mean_val - min_val) / std_dev
        
        if z_score_min > 3.0 and data_source == "Kepler-69 Exoplanet":
            st.error(f"> CRITICAL DIP DETECTED: Starlight dropped to {min_val:.1f} {y_label}. Exact signature of a planetary transit.")
        elif data_source == "LIGO Gravitational Wave (GW150914 Model)":
            st.error("> SINGULARITY MERGER DETECTED: Exponential strain frequency indicates two black holes have collided. Prepare for maximum amplitude 'chirp'.")
        elif z_score_max > 3.0:
            st.error(f"> CRITICAL SPIKE DETECTED: Value surged to {max_val:.1f} {y_label}. Brace for extreme audio modulation.")
        elif z_score_max > 2.0 or z_score_min > 2.0:
            st.warning("> WARNING: Moderate anomaly detected. Data has deviated by 2 standard deviations.")
        else:
            st.success("> ALL SYSTEMS NOMINAL. Data is flowing within standard deviations.")
    else:
        st.info("> DATA STREAM FLATLINE.")

# --- THE 3D AUDIO COMPOSER ---
st.markdown("---")
if st.sidebar.button("INITIATE SONIFICATION"):
    st.write(f"> CALCULATING SPATIAL ACOUSTICS [ {instrument.upper()} ]...")
    
    d_min, d_max = np.min(data_array), np.max(data_array)
    if d_min == d_max: d_max = d_min + 1
    frequencies = f_min + (data_array - d_min) * (f_max - f_min) / (d_max - d_min)
    
    v_min, v_max = np.min(volume_array), np.max(volume_array)
    if v_min == v_max: v_max = v_min + 1
    amplitudes = 0.1 + (volume_array - v_min) * 0.9 / (v_max - v_min)

    sample_rate = 44100
    duration_per_point = playback_speed / 1000.0
    
    left_ear, right_ear = [], []
    total_points = len(frequencies)

    for i, (freq, amp) in enumerate(zip(frequencies, amplitudes)):
        t = np.linspace(0, duration_per_point, int(sample_rate * duration_per_point), False)
        
        if "Sine" in instrument:
            base_tone = amp * np.sin(freq * t * 2 * np.pi)
        elif "Square" in instrument:
            base_tone = amp * signal.square(freq * t * 2 * np.pi)
        elif "Sawtooth" in instrument:
            base_tone = amp * signal.sawtooth(freq * t * 2 * np.pi)
        elif "Granular Swarm" in instrument:
            tone1 = np.sin(freq * t * 2 * np.pi)
            tone2 = 0.5 * np.sin((freq * 1.02) * t * 2 * np.pi) 
            tone3 = 0.5 * np.sin((freq * 0.98) * t * 2 * np.pi) 
            noise = np.random.normal(0, 0.1, len(t)) 
            window = np.hanning(len(t)) 
            base_tone = amp * (tone1 + tone2 + tone3 + noise) * window * 0.6
            
        progress = i / total_points
        angle = progress * (np.pi / 2)
        left_ear.extend(base_tone * np.cos(angle))
        right_ear.extend(base_tone * np.sin(angle))

    stereo_wave = np.column_stack((left_ear, right_ear))
    audio_data = np.int16(stereo_wave * 32767)
    
    wavfile.write("lyra_master.wav", sample_rate, audio_data)
    st.audio("lyra_master.wav")
    
    # NEW: ACOUSTIC SPECTROGRAM (See the Sound)
    st.write("> AUDIO RENDER COMPLETE. VISUALIZING SPECTROGRAM:")
    
    # We downsample the array so we don't crash the browser rendering the image
    f_spec, t_spec, Sxx = signal.spectrogram(stereo_wave[::4, 0], fs=sample_rate/4, nperseg=256)
    
    fig_spec = go.Figure(data=go.Heatmap(
        z=10 * np.log10(Sxx + 1e-10), # Convert to decibels
        x=t_spec, y=f_spec, colorscale='Viridis'
    ))
    # Cap the Y-axis so we only see the relevant musical frequencies, not empty static
    fig_spec.update_layout(
        paper_bgcolor='#050505', plot_bgcolor='#050505',
        font=dict(color='#00ff41', family='Courier New'),
        yaxis=dict(title="Frequency (Hz)", range=[0, f_max * 1.5]),
        xaxis=dict(title="Time (Seconds)"),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig_spec, use_container_width=True)