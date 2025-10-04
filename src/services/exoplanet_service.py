from pathlib import Path
from unittest import result
from models.exoplanet import ExoplanetData, Response
from fastapi import UploadFile
import logging
import joblib
import pandas as pd
import io

logger = logging.getLogger(__name__)
model_path = Path().parent / "utils" / "xgb_pipeline.pkl"
model = joblib.load(model_path)
encoder_path = Path().parent / "utils" / "label_encoder.pkl"
encoder = joblib.load(encoder_path)


class ExoplanetService:
    @staticmethod
    async def process_exoplanet_data(data: ExoplanetData) -> Response:
        try:
            logger.info(f"Processing exoplanet data: RA={data.ra}, DEC={data.dec}")

            # Calculation needed before sending the data to the model will happen here!
            planet_to_star_ratio = data.pl_rade / data.st_rad
            duration_to_period = data.pl_trandurh / data.pl_orbper
            depth_to_radius = data.pl_trandep / data.pl_rade
            insolation_eff_ratio = data.pl_insol / (data.st_teff * 4)
            eqt_to_insol = data.pl_eqt / (data.pl_insol * 0.25)
            tran_snr_proxy = data.pl_trandep / data.pl_trandeperr1

            data_dict = data.model_dump()
            data_dict.update(
                {
                    "planet_to_star_ratio": planet_to_star_ratio,
                    "duration_to_period": duration_to_period,
                    "depth_to_radius": depth_to_radius,
                    "insolation_eff_ratio": insolation_eff_ratio,
                    "eqt_to_insol": eqt_to_insol,
                    "tran_snr_proxy": tran_snr_proxy,
                }
            )

            df = pd.DataFrame(data_dict, index=[0])

            probs = model.predict_proba(df)[0]
            predicted_index = probs.argmax()
            predicted_prob = float(probs[predicted_index])

            result = {
                "predicted_class": f"{encoder.inverse_transform([predicted_index])[0]}",
                "predicted_proba": f"{round(predicted_prob,2)}",
            }

            response = Response(
                success=True,
                data=result,
                message="Exoplanet data processed successfully",
            )

            logger.info("Exoplanet data processed successfully")
            return response

        except Exception as e:
            logger.error(f"Error processing exoplanet data: {str(e)}")
            raise

    @staticmethod
    async def process_exoplanet_file(file: UploadFile) -> Response:
        try:
            logger.info(f"Processing uploaded file: {file.filename}")

            contents = await file.read()

            if file.filename.endswith(".csv"):
                df = pd.read_csv(io.BytesIO(contents))
            elif file.filename.endswith((".xlsx", ".xls")):
                df = pd.read_excel(io.BytesIO(contents))
            else:
                raise ValueError(
                    "Unsupported file format. Only CSV and Excel are supported."
                )
            if df.empty:
                raise ValueError("The uploaded file is empty")

            # Process the first row (or you can modify to process all rows)
            result = []
            for index, row in df.iterrows():
                exoplanet_data = ExoplanetData(**row.to_dict())
                response = await ExoplanetService.process_exoplanet_data(exoplanet_data)
                result.append(response.data)

            logger.info("File processed successfully")
            return Response(
                success=True,
                data=result,
                message="Exoplanet file processed successfully",
            )

        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            raise
