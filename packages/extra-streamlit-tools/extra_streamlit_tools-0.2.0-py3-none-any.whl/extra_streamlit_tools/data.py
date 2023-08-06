import pandas as pd
from typing import Any, Type
import numpy as np
from extra_streamlit_tools._logging import logging as logger


def series_to_value(series_value: pd.Series) -> Any:
    """
    The series_to_value function takes a pandas series and returns the value of that series.
    If there is more than one row in the series, it raises an error.

    Parameters
    ----------
        series_value:pd.Series
            Pass the series object to the function

    Returns
    -------
        Any
            A single value from a pd.Series

    Examples
    --------
    >>> series_to_value(pd.Series([1]))
    1

    >>> series_to_value(pd.Series([1, 2]))
    ValueError: Found more than one row
    """  # noqa
    if len(series_value) > 1:
        raise ValueError("Found more than one row")

    value = series_value.values[0]

    if value is None:
        return ""

    if isinstance(value, str):
        return value.replace(
            "#", ""
        )  # remove hashtag to prevent markdown titles

    if isinstance(value, float):
        try:
            return int(value)
        except ValueError:
            if np.isnan(value):
                return ""
    return value


def get_unique_sorted_values(
    df: pd.DataFrame, column: str, astype: Type = str
) -> list[Any]:
    """
    The get_unique_sorted_values function returns a list of sorted unique values for the given column.

    Parameters
    ----------
        df:pd.DataFrame
            Specify the dataframe that is used in the function
        column:str
            Specify the column name of the dataframe to get the values from
        astype:Type=str
            Specify the type to convert the values to

    Returns
    -------
        list[Any]
            A list of unique and sorted values for a given column

    Examples
    --------
    >>> df = pd.DataFrame({'col1': ['a', 'b', 'c'], 'col2': [1, 2, 3]})
    >>> get_unique_sorted_values(df, 'col1')
    ['a', 'b', 'c']

    >>> get_unique_sorted_values(df, 'col2', astype=float)
    [1.0, 2.0, 3.0]
    """  # noqa
    unique_sorted_values = sorted(df[column].astype(astype).unique().tolist())
    logger.debug(
        f"{len(unique_sorted_values)} unique values "
        "found for column: '{column}'"  #
    )
    return unique_sorted_values


def get_values_based_on_other_value(
    df: pd.DataFrame,
    based_column: str,
    based_value: any,
    new_values_column: str,
) -> list[any]:
    """
    The get_values_based_on_other_value function takes a dataframe, a column name, and a value.
    It returns the unique values of another column in the same dataframe where that first column has
    the given value.

    Parameters
    ----------
        df:pd.DataFrame
            Specify the dataframe that is being used
        based_column:str
            Specify the column that will be used to filter the dataframe
        based_value:any
            Specify the value that is used to filter the based column with
        new_values_column:str
            Specify the column that we want to get values from

    Returns
    -------
        list[any]
            The values in the new_values_column column

    Examples
    --------
    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': ['a', 'b', 'c']})
    >>> get_values_based_on_other_value(df, 'A', 1, 'C')
    ['a']

    >>> get_values_based_on_other_value(df, 'B', 6, 'C')
    ['c']
    """  # noqa
    return sorted(
        df.loc[lambda d: d[based_column] == based_value, new_values_column]
        .unique()
        .tolist()
    )


def get_concat_columns(df: pd.DataFrame, columns, join_with: str) -> list[str]:
    """
    The get_concat_columns function takes a dataframe, a list of columns to concatenate, and the string to join them with.
    It returns a list of strings that are the concatenated values from each row in the specified columns.

    Parameters
    ----------
        df:pd.DataFrame
            Specify the dataframe that is being passed into the function
        columns
            Specify the columns that will be concatenated
        join_with:str
            Specify the join string that will be used to join the row values into a string

    Returns
    -------
        list[str]
            A list of strings

    Examples
    --------
    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': ['a', 'b', 'c']})
    >>> get_concat_columns(df, ['A', 'B'], '-')
    ['1-4', '2-5', '3-6']

    >>> get_concat_columns(df, ['A', 'C'], '.')
    ['1.a', '2.b', '3.c']
    """  # noqa
    return df[columns].astype(str).agg(join_with.join, axis=1).tolist()
