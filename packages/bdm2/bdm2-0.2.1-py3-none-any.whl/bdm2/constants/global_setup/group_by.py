from dataclasses import dataclass


@dataclass
class GroupByConfig:
    do_grouping: bool
    reliability: str
    use_median: bool = False


group_by_methods = {
    "v0": {
        "group_by_track": GroupByConfig(do_grouping=False, reliability=""),
        "group_by_sess": GroupByConfig(do_grouping=False, reliability=""),
        "group_by_age": GroupByConfig(do_grouping=True, reliability=""),
        "group_by_house": GroupByConfig(do_grouping=True, reliability=""),
    },
    "v3": {
        "group_by_track": GroupByConfig(
            do_grouping=True, reliability="private_reliability"
        ),
        "group_by_sess": GroupByConfig(do_grouping=False, reliability=""),
        "group_by_age": GroupByConfig(do_grouping=True, reliability="reliability"),
        "group_by_house": GroupByConfig(do_grouping=False, reliability=""),
    },
    "v4": {
        "group_by_track": GroupByConfig(
            do_grouping=True, reliability="private_reliability"
        ),
        "group_by_sess": GroupByConfig(do_grouping=True, reliability=""),
        "group_by_age": GroupByConfig(do_grouping=True, reliability=""),
        "group_by_house": GroupByConfig(do_grouping=False, reliability=""),
    },
}

active_group_by_method = "v4"

group_by_track_reliability = group_by_methods[active_group_by_method][
    "group_by_track"
].reliability
group_by_age_reliability = group_by_methods[active_group_by_method][
    "group_by_age"
].reliability
group_by_house_reliability = group_by_methods[active_group_by_method][
    "group_by_house"
].reliability
