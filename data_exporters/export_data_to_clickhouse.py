if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import sqlalchemy as sa
from clickhouse_sqlalchemy import (engines, get_declarative_base, make_session, types)

from demo_project.utils.sqlalchemy_utils import TableBase

uri = "clickhouse+native://localhost/default"

engine = sa.create_engine(uri)
metadata = sa.MetaData(bind=engine)

Base = get_declarative_base(metadata=metadata)



class TableCity(TableBase, Base):
    __tablename__ = "city"
    __table_args__ = (
        engines.ReplacingMergeTree(
            version="version",
            partition_by="city",
            order_by=("city", "district"),
        ),
        {
            "schema": "default",
            #  'clickhouse_cluster': 'my_cluster',
            "extend_existing": True,
        },
    )

    city = sa.Column(types.String, primary_key=True)
    district = sa.Column(types.String, primary_key=True)
    notes = sa.Column(types.Nullable(types.String))
    active = sa.Column(types.Nullable(types.Int32))
    confirmed = sa.Column(types.Nullable(types.Int32))
    migratedother = sa.Column(types.Nullable(types.Int32))
    deceased = sa.Column(types.Nullable(types.Int32))
    recovered = sa.Column(types.Nullable(types.Int32))
    delta_confirmed = sa.Column("delta.confirmed", types.Nullable(types.Int32))
    delta_deceased = sa.Column("delta.deceased", types.Nullable(types.Int32))
    delta_recovered = sa.Column("delta.recovered", types.Nullable(types.Int32))
    version = sa.Column(types.UInt64)


@data_exporter
def export_data(df, *args, **kwargs):
    print("sqlalchemy:", sa.__version__)
    
    TableCity.create(checkfirst=True)

    if len(df) > 0:
        df.to_sql(
            name=TableCity.table_name(),
            con=engine,
            schema="default",
            if_exists="append",
            index=False,
            chunksize=1_000,
        )


# Add Unit test
