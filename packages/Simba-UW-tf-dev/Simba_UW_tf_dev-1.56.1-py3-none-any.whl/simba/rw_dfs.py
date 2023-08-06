import os.path
import pandas as pd
from simba.utils.errors import InvalidFileTypeError, NoFilesFoundError

def read_df(file_path: str,
            file_type: str,
            idx=0,
            remove_columns: list or None=None,
            usecols: list or None=None):
    """
    Helper function to read single data file into memory.

    Parameters
    ----------
    file_path: str
        Path to data file.
    file_type: str
        Type of data. OPTIONS: 'parquet' or 'csv'.
    idx: int,
        Index column location. Default: 0.
    remove_columns: list or None,
        If list, remove columns
    usecols: list or None,
        If list, keep columns

    Returns
    -------
    df: pd.DataFrame

    """
    try:
        if file_type == 'csv':
            try:
                df = pd.read_csv(file_path, index_col=idx, low_memory=False, sep=',')
            except Exception as e:
                if type(e).__name__ == 'ParserError':
                    raise InvalidFileTypeError(msg=f' SimBA tried to read {file_path} as a comma delimited CSV file and failed. Make sure {os.path.basename(file_path)} is a utf-8 encoded comma delimited CSV file.')
                if type(e).__name__ == 'UnicodeDecodeError':
                    raise InvalidFileTypeError(msg=f'{file_path} is not a valid CSV file')
        elif file_type == 'parquet':
            df = pd.read_parquet(file_path)
        else:
            raise InvalidFileTypeError(msg=f'The file type ({file_type}) is not recognized. Please set the workflow file type to either csv or parquet')
        if remove_columns:
            df = df[df.columns[~df.columns.isin(remove_columns)]]
        if usecols:
            df = df[df.columns[df.columns.isin(usecols)]]
        else:
            pass
        return df
    except FileNotFoundError:
        raise NoFilesFoundError(msg=f'The CSV file could not be located at the following path: {file_path}. It may be that you missed a step in the analysis. Please generate the file before proceeding.')

def save_df(df: pd.DataFrame,
            file_type: str,
            save_path: str):
    """
    Helper function to save single data file from memory.

    Parameters
    ----------
    df: pd.DataFrame
        Pandas dataframe to save to disk.
    file_type: str
        Type of data. OPTIONS: 'parquet' or 'csv'.
    save_path: str,
        Location where to store the data.

    Returns
    -------
    None

    """

    if file_type == 'csv':
        df = df.drop('scorer', axis=1, errors='ignore')
        df.to_csv(save_path, index=True)
    elif file_type == 'parquet':
        df.to_parquet(file_type)
    else:
        raise InvalidFileTypeError(msg='The file type is not recognized. Please set the workflow file type to either csv or parquet')