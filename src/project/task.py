from importlib import resources
import polars as pl


def get_data_file():
    """Get path to the raw data file."""
    data_file = resources.files("project").joinpath("data/exp1.csv")
    return data_file


def read_data(data_file):
    """Read data and fix formatting."""
    raw = pl.read_csv(data_file)
    columns = [
        "subj",
        "cycle",
        "trial",
        "phase",
        "type",
        "word1",
        "word2",
        "response",
        "RT",
        "correct",
        "lag",
    ]
    df = raw.select(pl.col(columns)).with_columns(
        pl.col("response", "RT", "correct", "lag").replace(-1, None)
    )
    return df


def exclude_fast_responses(df, thresh=0.2):
    """Exclude responses that were too quick to be reactions."""
    df_filt = (
        df.with_columns(
            RT=pl.when(pl.col("RT") < thresh)
            .then(None)
            .otherwise(pl.col("RT"))
        )
        .with_columns(
            response=pl.when(pl.col("RT").is_null())
            .then(None)
            .otherwise(pl.col("response"))
        )
    )
    return df_filt
