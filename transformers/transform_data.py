if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

import datetime

import pandas as pd
import pandera as pa


@transformer
def transform(d, *args, **kwargs) -> pd.DataFrame:
    # Transform
    d_ = []
    for city, v in d.items():
        for district, v_ in v["districtData"].items():
            d_i = {}
            d_i["city"] = city
            d_i["district"] = district
            d_i.update(v_)
            d_.append(d_i)
    df = pd.json_normalize(d_, errors="raise", sep=".", max_level=2)
    df["version"] = int(datetime.datetime.timestamp(datetime.datetime.now()) * 1000)
    # Add version to control update
    return df


@test
def test_output(df, *args) -> None:
    assert df is not None, "The output is undefined"

    ## Unit test
    CitySchema = pa.DataFrameSchema(
        columns={
            "city": pa.Column(str),
            "district": pa.Column(str),
            "notes": pa.Column(str, nullable=True),
            "active": pa.Column(int, nullable=True),
            "confirmed": pa.Column(
                int, checks=pa.Check.greater_than_or_equal_to(0), nullable=True
            ),
            "migratedother": pa.Column(int, nullable=True),
            "deceased": pa.Column(int, nullable=True),
            "recovered": pa.Column(int, nullable=True),
            "delta.confirmed": pa.Column(int, nullable=True),
            "delta.deceased": pa.Column(int, nullable=True),
            "delta.recovered": pa.Column(int, nullable=True),
            "version": pa.Column(int, checks=pa.Check.greater_than_or_equal_to(0)),
        },
        coerce=True,
        strict=True,
    )

    CitySchema.validate(df)
