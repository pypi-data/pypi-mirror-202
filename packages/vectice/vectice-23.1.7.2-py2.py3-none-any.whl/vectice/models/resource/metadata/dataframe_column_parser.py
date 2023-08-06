from __future__ import annotations

from pandas import DataFrame, Series, api

from vectice.models.resource.metadata.column_metadata import Column, StatValue

# mypy: ignore-errors


def capture_columns(init_columns: list[Column] | None, dataframe: DataFrame | None) -> dict:
    init_columns = init_columns if init_columns is not None else []
    if dataframe is None:
        return [column.asdict() for column in init_columns]

    columns: list[Column] = []
    column_names_with_types = dataframe.dtypes.astype(str).to_dict()
    for idx, (name, d_type) in enumerate(column_names_with_types.items()):
        if idx >= 100:
            break
        df_column = dataframe[name]
        stats = capture_column_stats(df_column)
        try:
            column = next(column for column in init_columns if column.name == name)
            column.stats = stats
        except StopIteration:
            column = Column(
                name=name,
                data_type=d_type if d_type != "object" else "string",
                stats=stats,
            )
            columns.append(column)

    return [column.asdict() for column in columns]


def capture_column_stats(series: Series) -> list[StatValue] | None:
    if api.types.is_bool_dtype(series):
        return compute_boolean_column_statistics(series)  # type: ignore[no-any-return]
    elif api.types.is_numeric_dtype(series):
        return compute_numeric_column_statistics(series)  # type: ignore[no-any-return]
    elif api.types.is_string_dtype(series):
        return compute_string_column_statistics(series)  # type: ignore[no-any-return]
    return None


def compute_boolean_column_statistics(series: Series) -> list[StatValue]:
    """Parse a dataframe series and return statistics about it.

    The computed statistics are:
    - the series count (size)
    - the top value
    - the frequence of the value
    Parameters:
        series: The pandas series to get information from.

    Returns:
        A list of StatValue.
    """
    value_counts = series.value_counts()
    count = series.count()
    top = value_counts.idxmax()
    freq = value_counts.max()
    return [
        StatValue(key="count", value=int(count)),
        StatValue(key="top", value=float(top) if isinstance(top, float) else int(top)),
        StatValue(key="freq", value=float(freq) if isinstance(freq, float) else int(freq)),
    ]


def compute_numeric_column_statistics(series: Series) -> list[StatValue]:
    """Parse a dataframe series and return statistics about it.

    The computed statistics are:
    - the series count (size)
    - the mean
    - the median
    - the variance
    - the standard deviation
    - the min value
    - the 25% percentiles
    - the 50% percentiles
    - the 75% percentiles
    - the max value
    Parameters:
        series: The pandas series to get information from.

    Returns:
        A list of StatValue.
    """
    var = series.var()
    stats = [
        StatValue("median", series.median()),
        StatValue("variance", float(var) if isinstance(var, float) else int(var)),
    ]
    stats.extend(
        [
            StatValue(str(name), float(value) if isinstance(value, float) else int(value))
            for name, value in series.describe().items()
        ]
    )
    return stats


def compute_string_column_statistics(series: Series) -> list[StatValue]:
    """Parse a dataframe series and return statistics about it.

    The computed statistics are:
    - the null count
    - the series count (size)
    - the unique number of value
    - the most frequent value (top)
    - the frequency of the top value
    Parameters:
        series: The pandas series to get information from.

    Returns:
        A list of StatValue.
    """
    stats = [StatValue("null", int(series.isna().sum()))]
    for name, value in series.describe(include="all").items():
        stats.extend([StatValue(str(name), int(value) if not isinstance(value, str) else str(value))])

    return stats
