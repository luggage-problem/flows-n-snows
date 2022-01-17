import ulmo
import pandas as pd
import numpy as np
import matplotlib
from datetime import datetime


def fetch_snotel_to_df(site_id: str, start_date: str, end_date: str) -> pd.DataFrame:
    WSDL_URL = "https://hydroportal.cuahsi.org/Snotel/cuahsi_1_1.asmx?WSDL"
    SNOW_WATER_EQUIV = "SNOTEL:WTEQ_D"
    snow_data = ulmo.cuahsi.wof.get_values(
        WSDL_URL,
        site_id,
        SNOW_WATER_EQUIV,
        start="1980-01-01",
        end=datetime.today().strftime("%Y-%m-%d"),
    )

    values_df = pd.DataFrame.from_dict(snow_data["values"])
    values_df["datetime"] = pd.to_datetime(values_df["datetime"], utc=True)
    values_df = values_df.set_index("datetime")
    values_df["value"] = pd.to_numeric(values_df["value"]).replace(-9999, np.nan)
    values_df = values_df[values_df["quality_control_level_code"] == "1"]

    return values_df


def fetch_river_flows(
    river_id: int, start_date: str, end_date: str, interval: str = "daily"
) -> pd.DataFrame:
    flow_data = ulmo.usgs.nwis.get_site_data(
        river_id,
        service=interval,
        start=start_date,
        end=end_date,
    )
    ####???? parsing???? ###
    flow_data = flow_data["00060:00003"]["values"]
    values_df = pd.DataFrame.from_dict(flow_data)

    return values_df