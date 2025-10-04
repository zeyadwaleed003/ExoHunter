from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Any, Optional


class ExoplanetData(BaseModel):
    pl_eqt: Optional[float] = None
    st_tmag: Optional[float] = None
    st_dist: Optional[float] = None
    pl_rade: Optional[float] = None
    pl_trandurherr1: Optional[float] = None
    pl_orbper: Optional[float] = None
    pl_trandurh: Optional[float] = None
    pl_radeerr1: Optional[float] = None
    st_loggerr1: Optional[float] = None
    pl_trandeperr1: Optional[float] = None
    pl_orbpererr1: Optional[float] = None
    st_teff: Optional[float] = None
    pl_insol: Optional[float] = None
    planet_to_star_ratio: Optional[float] = None
    duration_to_period: Optional[float] = None
    depth_to_radius: Optional[float] = None
    insolation_eff_ratio: Optional[float] = None
    eqt_to_insol: Optional[float] = None
    tran_snr_proxy: Optional[float] = None
    st_raderr1: Optional[float] = None
    st_disterr1: Optional[float] = None
    st_pmdecerr1: Optional[float] = None
    st_pmraerr1: Optional[float] = None
    st_pmdec: Optional[float] = None
    st_pmra: Optional[float] = None
    st_logg: Optional[float] = None
    ra: Optional[float] = None
    dec: Optional[float] = None
    st_rad: Optional[float] = None
    pl_trandep: Optional[float] = None


class Response(BaseModel):
    success: bool
    message: Optional[str] = None
    prediction: Optional[str] = None
    confidence: Optional[float] = None
    data: Optional[Any] = None
