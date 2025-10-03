from models.exoplanet import ExoplanetData, Response
import logging

logger = logging.getLogger(__name__)


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
            data_dict.update({
                "planet_to_star_ratio": planet_to_star_ratio,
                "duration_to_period": duration_to_period,
                "depth_to_radius": depth_to_radius,
                "insolation_eff_ratio": insolation_eff_ratio,
                "eqt_to_insol": eqt_to_insol,
                "tran_snr_proxy": tran_snr_proxy
            })
            
            response = Response(
                success=True,
                data=data_dict,
                message="Exoplanet data processed successfully"
            )
            
            logger.info("Exoplanet data processed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error processing exoplanet data: {str(e)}")
            raise
