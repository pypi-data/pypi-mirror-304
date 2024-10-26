import re

from ..global_setup.engine import density_model_info_file_name

split_engine_pattern = re.compile(
    r"(?P<device_type>\w{2,7})_"
    r"(?P<engine>split)_"
    r"v(?P<engine_v>.*)_"
    r"(?P<release_date>\d{4})"
)
split_engine_pattern_example = r"jetson_split_v4.10.7.46_1705"

density_model_info_file_pattern = re.compile(rf"{density_model_info_file_name}")

aws_engine_pattern = re.compile(
    r"aws_cloud_"
    r"v(?P<engine_v>.*)_"
    r"(?P<client>.*)_"
    r"(?P<breed_type>.*)_"
    r"(?P<gender>.*)_"
    r"(?P<release_date>\d{4})_final"
)
aws_engine_pattern_example = "aws_cloud_v4.10.7.45_CGTHBG_Arbor-Acres_female_2704_final"

# allows you to define age from fname
s3_explicit_pattern = re.compile(r"ForwardRunViz_explicit_\d{1,2}_\d{1,2}_\d{1,2}_Capture_(?P<age>\d{1,2}).txt")
s3_parquet_pattern = re.compile(r"ForwardRunViz_explicit_.*.txt.parquet")

pattern_image_name_output_folder = re.compile(r"output_.*_age_(?P<age>\d{1,2})")
