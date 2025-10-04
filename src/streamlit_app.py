import streamlit as st
import requests
import pandas as pd
import io
import json
from typing import Dict, Any

# Page configuration
st.set_page_config(
    page_title="ExoHunter - Exoplanet Classification",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.3rem;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.3rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# API configuration
API_BASE_URL = st.sidebar.text_input(
    "API Base URL", value="http://localhost:8000", help="Enter your FastAPI backend URL"
)

# Header
st.markdown('<h1 class="main-header">🪐 ExoHunter</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Exoplanet Classification System</p>', unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/planet.png", width=80)
    st.title("Navigation")
    app_mode = st.radio(
        "Choose Mode:", ["Single Prediction", "Batch Upload", "API Health Check"]
    )

    st.markdown("---")
    st.markdown("### About")
    st.info(
        "ExoHunter uses machine learning to classify exoplanets based on "
        "their physical and orbital characteristics."
    )


# API Health Check Function
def check_api_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        return False, None
    except Exception as e:
        return False, str(e)


# Single Prediction Function
def predict_single(data: Dict[str, Any]):
    try:
        response = requests.post(f"{API_BASE_URL}/exoplanet/", json=data, timeout=30)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()
    except Exception as e:
        return False, str(e)


# Batch Upload Function
def predict_batch(file):
    try:
        files = {"file": (file.name, file, file.type)}
        response = requests.post(
            f"{API_BASE_URL}/exoplanet/upload", files=files, timeout=60
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()
    except Exception as e:
        return False, str(e)


# Mode: API Health Check
if app_mode == "API Health Check":
    st.header("🔍 API Health Check")

    if st.button("Check API Status", type="primary"):
        with st.spinner("Checking API health..."):
            is_healthy, result = check_api_health()

            if is_healthy:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ API is healthy and running!")
                st.json(result)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error("❌ API is not reachable")
                st.write(f"Error: {result}")
                st.markdown("</div>", unsafe_allow_html=True)

# Mode: Single Prediction
elif app_mode == "Single Prediction":
    st.header("🔮 Single Exoplanet Prediction")

    st.markdown("### Enter Exoplanet Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Positional Data")
        ra = st.number_input("Right Ascension (RA)", value=0.0, format="%.6f")
        dec = st.number_input("Declination (DEC)", value=0.0, format="%.6f")

        st.subheader("Planetary Radius & Mass")
        pl_rade = st.number_input(
            "Planet Radius (Earth radii)", value=1.0, min_value=0.0, format="%.4f"
        )
        pl_bmasse = st.number_input(
            "Planet Mass (Earth masses)", value=1.0, min_value=0.0, format="%.4f"
        )

    with col2:
        st.subheader("Orbital Parameters")
        pl_orbper = st.number_input(
            "Orbital Period (days)", value=365.0, min_value=0.0, format="%.4f"
        )
        pl_orbsmax = st.number_input(
            "Semi-Major Axis (AU)", value=1.0, min_value=0.0, format="%.6f"
        )
        pl_orbeccen = st.number_input(
            "Orbital Eccentricity",
            value=0.0,
            min_value=0.0,
            max_value=1.0,
            format="%.6f",
        )

        st.subheader("Transit Properties")
        pl_trandurh = st.number_input(
            "Transit Duration (hours)", value=1.0, min_value=0.0, format="%.4f"
        )
        pl_trandep = st.number_input(
            "Transit Depth (ppm)", value=100.0, min_value=0.0, format="%.2f"
        )
        pl_trandeperr1 = st.number_input(
            "Transit Depth Error", value=1.0, min_value=0.0, format="%.4f"
        )

    with col3:
        st.subheader("Planetary Environment")
        pl_insol = st.number_input(
            "Insolation Flux (Earth flux)", value=1.0, min_value=0.0, format="%.4f"
        )
        pl_eqt = st.number_input(
            "Equilibrium Temperature (K)", value=288.0, min_value=0.0, format="%.2f"
        )
        pl_dens = st.number_input(
            "Planet Density (g/cm³)", value=5.5, min_value=0.0, format="%.4f"
        )

        st.subheader("Stellar Properties")
        st_rad = st.number_input(
            "Stellar Radius (Solar radii)", value=1.0, min_value=0.0, format="%.4f"
        )
        st_mass = st.number_input(
            "Stellar Mass (Solar masses)", value=1.0, min_value=0.0, format="%.4f"
        )
        st_teff = st.number_input(
            "Stellar Effective Temperature (K)",
            value=5778.0,
            min_value=0.0,
            format="%.2f",
        )

    st.markdown("---")

    if st.button("🚀 Classify Exoplanet", type="primary", use_container_width=True):
        # Prepare data
        exoplanet_data = {
            "ra": ra,
            "dec": dec,
            "pl_rade": pl_rade,
            "pl_bmasse": pl_bmasse,
            "pl_orbper": pl_orbper,
            "pl_orbsmax": pl_orbsmax,
            "pl_orbeccen": pl_orbeccen,
            "pl_insol": pl_insol,
            "pl_eqt": pl_eqt,
            "pl_trandurh": pl_trandurh,
            "pl_trandep": pl_trandep,
            "pl_trandeperr1": pl_trandeperr1,
            "pl_trandur": pl_trandurh * 24,  # Convert to minutes if needed
            "pl_dens": pl_dens,
            "st_rad": st_rad,
            "st_mass": st_mass,
            "st_teff": st_teff,
        }

        with st.spinner("Classifying exoplanet..."):
            success, result = predict_single(exoplanet_data)

            if success:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ Classification Complete!")
                st.markdown("</div>", unsafe_allow_html=True)

                # Display results
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        label="Predicted Class", value=result["data"]["predicted_class"]
                    )
                with col2:
                    st.metric(
                        label="Confidence",
                        value=f"{float(result['data']['predicted_proba']) * 100:.1f}%",
                    )

                # Show full response
                with st.expander("View Full Response"):
                    st.json(result)
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error("❌ Classification Failed")
                st.write(result)
                st.markdown("</div>", unsafe_allow_html=True)

# Mode: Batch Upload
elif app_mode == "Batch Upload":
    st.header("📊 Batch Exoplanet Classification")

    st.markdown(
        """
    Upload a CSV or Excel file containing exoplanet data for batch classification.
    
    **Required columns:**
    - `ra`, `dec` (positional data)
    - `pl_rade`, `pl_bmasse`, `pl_orbper`, `pl_orbsmax`, `pl_orbeccen` (planetary parameters)
    - `pl_insol`, `pl_eqt`, `pl_trandurh`, `pl_trandep`, `pl_trandeperr1`, `pl_trandur`, `pl_dens` (planetary environment)
    - `st_rad`, `st_mass`, `st_teff` (stellar properties)
    """
    )

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["csv", "xlsx", "xls"],
        help="Upload a CSV or Excel file with exoplanet data",
    )

    if uploaded_file is not None:
        # Preview the file
        st.subheader("📋 Data Preview")
        try:
            if uploaded_file.name.endswith(".csv"):
                df_preview = pd.read_csv(uploaded_file)
                uploaded_file.seek(0)  # Reset file pointer
            else:
                df_preview = pd.read_excel(uploaded_file)
                uploaded_file.seek(0)  # Reset file pointer

            st.dataframe(df_preview.head(10), use_container_width=True)
            st.info(f"Total rows: {len(df_preview)}")

        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

        st.markdown("---")

        if st.button(
            "🚀 Classify All Exoplanets", type="primary", use_container_width=True
        ):
            with st.spinner("Processing batch classification..."):
                success, result = predict_batch(uploaded_file)

                if success:
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.success("✅ Batch Classification Complete!")
                    st.markdown("</div>", unsafe_allow_html=True)

                    # Convert results to DataFrame
                    if "data" in result and isinstance(result["data"], list):
                        results_df = pd.DataFrame(result["data"])

                        # Display summary
                        st.subheader("📊 Classification Summary")
                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric("Total Classified", len(results_df))

                        with col2:
                            if "predicted_class" in results_df.columns:
                                st.write("**Class Distribution:**")
                                st.write(results_df["predicted_class"].value_counts())

                        # Display results table
                        st.subheader("🔍 Detailed Results")
                        st.dataframe(results_df, use_container_width=True)

                        # Download results
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv,
                            file_name="exoplanet_classifications.csv",
                            mime="text/csv",
                            use_container_width=True,
                        )
                    else:
                        st.json(result)
                else:
                    st.markdown('<div class="error-box">', unsafe_allow_html=True)
                    st.error("❌ Batch Classification Failed")
                    st.write(result)
                    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ using Streamlit | Powered by FastAPI & XGBoost</p>
    </div>
    """,
    unsafe_allow_html=True,
)
