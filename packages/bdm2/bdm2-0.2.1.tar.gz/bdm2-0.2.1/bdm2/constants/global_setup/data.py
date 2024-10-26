from pydantic import BaseModel

from .data_columns import *

max_age = 60
struct_levels = [farm_column, cycle_column, flock_column, house_column, device_column]
device_match_columns = [farm_column, cycle_column, house_column, device_column]
house_match_columns = [farm_column, cycle_column, house_column]
standards_match_columns = [client_column, breed_type_column, gender_column]


class Combination(BaseModel):
    client: str
    breed_type: str
    gender: str


valuable_reliability_columns = [
    reliability_column,
    common_reliability_column,
    private_reliability_column,
    tilt_reliability_column,
    missing_reliability_column,
]

default_flock_name = "Flock 1"

not_critical_params = [
    "RPrepFactoryParams_imagery_folder",
    "ObjectQualityEstimatorParams_save_explicit_result_imagery",
    "ObjectQualityEstimatorParams_save_prediction_result_imagery",
]

reader_filters = ["detroi", "eccentricity", "extent"]

sess_folder_date_format = "output_%Y_%m_%d_%H_%M_%S"
image_date_format = "%Y.%m.%d.%H.%M.%S.%f"

WEIGHTS_SRC_TYPE = {
    "DOC": "DOC",
    "Farmers": "Farmers",
    "SLT": "SLT",
    "PIWFHA": "PIWFHA",
    "Targets": "Targets",
    "Likely_targets": "Likely_targets",
    # old
    "Likely": "Likely",
    "Manuals": "Manuals",
    "Mahender": "Mahender",
}
