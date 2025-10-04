# ExoHunter

ExoHunter is an advanced application developed for the 2025 NASA Space Apps Challenge. It leverages artificial intelligence and machine learning (AI/ML) to automatically analyze open-source exoplanet datasets from NASA's Kepler, K2, and TESS missions. The application identifies exoplanets by processing transit method data and provides a user-friendly web interface for researchers and enthusiasts to interact with the model, visualize results, and explore exoplanet data.

## Running the application

### Starting the FastAPI backend

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI application using uvicorn:

   ```bash
   python src/main.py
   ```

### Starting the Streamlit Web Interface

1. Open a new terminal window and activate your virtual environment

2. Run the Streamlit application:

   ```bash
   streamlit run src/streamlit_app.py
   ```

## API Documentation

### Base URL

```bash
http://localhost:8000
```

## API Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API is running and healthy.

**Status Codes:**

- `200 OK`: API is healthy and running

---

### 2. Single Exoplanet Classification

**Endpoint:** `POST /exoplanet/`

**Description:** Classify a single exoplanet based on its physical and orbital characteristics.

**Request Body:**

```json
{
  "ra": 112.357708,
  "dec": -12.69596,
  "st_pmra": -5.964,
  "st_pmraerr1": 0.085,
  "st_pmdec": -0.076,
  "st_pmdecerr1": 0.072,
  "pl_tranmid": 2459229.630046,
  "pl_tranmiderr1": 0.001657,
  "pl_orbper": 2.1713484,
  "pl_orbpererr1": 0.0002637,
  "pl_trandurh": 2.0172196,
  "pl_trandurherr1": 0.3195879,
  "pl_trandep": 656.8860989,
  "pl_trandeperr1": 37.77821,
  "pl_rade": 5.8181633,
  "pl_radeerr1": 1.9105465,
  "pl_insol": 22601.9485814,
  "pl_eqt": 3127.2040524,
  "st_tmag": 9.604,
  "st_tmagerr1": 0.013,
  "st_dist": 485.735,
  "st_disterr1": 11.9515,
  "st_tefferr1": 264.7,
  "st_logg": 4.19,
  "st_loggerr1": 0.07,
  "st_rad": 2.16986,
  "st_raderr1": 0.0725729,
  "planet_to_star_ratio": 0.02563,
  "duration_to_period": 0.03869,
  "depth_to_radius": 5.8181633,
  "st_teff": 4.4343
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "predicted_class": "CONFIRMED",
    "predicted_proba": "0.95"
  },
  "message": "Exoplanet data processed successfully"
}
```

### 3. Batch File Upload

**Endpoint:** `POST /exoplanet/upload`

**Description:** Upload a CSV or Excel file containing multiple exoplanet records for batch classification.

**Request:**

- **Content-Type:** `multipart/form-data`
- **File Parameter:** `file` (CSV or Excel file)

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "predicted_class": "CONFIRMED",
      "predicted_proba": "0.95"
    },
    {
      "predicted_class": "CANDIDATE",
      "predicted_proba": "0.78"
    }
  ],
  "message": "Exoplanet file processed successfully"
}
```
