# ExoHunter

ExoHunter is an advanced application developed for the 2025 NASA Space Apps Challenge. It leverages artificial intelligence and machine learning (AI/ML) to automatically analyze open-source exoplanet datasets from NASA's Kepler, K2, and TESS missions. The application identifies exoplanets by processing transit method data and provides a user-friendly web interface for researchers and enthusiasts to interact with the model, visualize results, and explore exoplanet data.

## Instructions to Run the API

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
