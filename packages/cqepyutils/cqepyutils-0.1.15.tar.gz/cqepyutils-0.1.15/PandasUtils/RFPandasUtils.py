import pandas as pd
import numpy as np
from robot.api import logger
from robot.api.deco import keyword


@keyword(name="Create Dataframe from file")
def create_dataframe_from_file(file_path, delimiter=',', has_header=True, width=None, encoding='ISO-8859-1',
                               on_bad_lines='warn', skiprows=0, skipfooter=0):
    """
    Creates a Pandas DataFrame from a CSV, PSV, or fixed-width file.

    Parameters:
        file_path (str): The path to the input file.
        delimiter (str): The delimiter character used in the input file. Default is ','.
        has_header (bool): Whether the input file has headers. Default is True.
        width (list or tuple): A list or tuple of integers specifying the width of each fixed-width field.
                              Required when reading a fixed-width file. Default is None.
        encoding (str): The encoding of the input file. Default is 'ISO-8859-1'.
        on_bad_lines (str): What to do with bad lines encountered in the input file.
                            Valid values are 'raise', 'warn', and 'skip'. Default is 'warn'.
        skiprows (int or list-like): Line numbers to skip (0-indexed) or number of lines to skip (int) at the start of the file. Default is 0.
        skipfooter (int): Number of lines to skip at the end of the file. Default is 0.

    Returns:
        pandas.DataFrame: The DataFrame created from the input file.

    Examples:
    | Create Dataframe from file | /path/to/file.csv |
    | Create Dataframe from file | /path/to/file.psv | delimiter='|', has_header=False |
    | Create Dataframe from file | /path/to/file.xlsx | has_header=False |
    | Create Dataframe from file | /path/to/file.fwf | width=[10, 20, 30] |
    | Create Dataframe from file | /path/to/file.csv | encoding='utf-8', on_bad_lines='raise' |

    """
    # Determine the file type based on the file extension
    file_ext = file_path.split('.')[-1].lower()
    if file_ext == 'csv':
        # Log info message
        logger.info(f"Step 1: Reading CSV file '{file_path}' with delimiter '{delimiter}' and encoding '{encoding}'")
        # Read CSV file into a DataFrame
        if has_header:
            df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding, on_bad_lines=on_bad_lines,
                             skiprows=skiprows, skipfooter=skipfooter)
        else:
            df = pd.read_csv(file_path, delimiter=delimiter, header=None, encoding=encoding, on_bad_lines=on_bad_lines,
                             skiprows=skiprows, skipfooter=skipfooter)
    elif file_ext == 'psv':
        # Log info message
        logger.info(f"Step 1: Reading PSV file '{file_path}' with delimiter '|'")
        # Read PSV file into a DataFrame
        if has_header:
            df = pd.read_csv(file_path, delimiter='|', encoding=encoding, on_bad_lines=on_bad_lines, skiprows=skiprows,
                             skipfooter=skipfooter)
        else:
            df = pd.read_csv(file_path, delimiter='|', header=None, encoding=encoding, on_bad_lines=on_bad_lines,
                             skiprows=skiprows, skipfooter=skipfooter)
    elif file_ext == 'xlsx':
        # Log info message
        logger.info(f"Step 1: Reading Excel file '{file_path}'")
        # Read Excel file into a DataFrame
        if has_header:
            df = pd.read_excel(file_path, skiprows=skiprows, skipfooter=skipfooter)
        else:
            df = pd.read_excel(file_path, header=None, skiprows=skiprows, skipfooter=skipfooter)
    elif file_ext == 'dat':
        # Log info message
        logger.info(f"Step 1: Reading fixed-width file '{file_path}' with width {width}")
        # Read fixed-width file into a DataFrame
        df = pd.read_fwf(file_path, widths=width, header=None, encoding=encoding, on_bad_lines=on_bad_lines,
                         skiprows=1, skipfooter=1)
    else:
        # Log error message and raise exception
        logger.error(
            f"Error: Unsupported file type '{file_ext}'. Supported file types are 'csv', 'psv', 'xlsx', and 'dat'.")
        raise Exception(f"Unsupported file type '{file_ext}'")

    # Log info message
    logger.info(f"Step 2: DataFrame created with {df.shape[0]} rows and {df.shape[1]} columns")
    # Return the DataFrame
    return df


@keyword("Write DataFrame to CSV file")
def write_df_to_csv(df_to_write: pd.DataFrame, file_path: str, file_name: str, index: bool = False):
    """
    This method is to write the df to csv file
    :param df_to_write: DataFrame to write to CSV file
    :param file_path: Path where the CSV file needs to be created
    :param file_name: Name of the CSV file to be created
    :param index: Whether to include the index in the CSV file
    :return: None
    """
    logger.info('Step 1: Writing DataFrame to CSV file...')
    try:
        df_to_write.to_csv(path_or_buf=file_path + '/' + file_name, mode='w', index=index)
        logger.info('Step 2: Writing DataFrame to CSV file completed successfully.')
    except Exception as e:
        logger.error(f'Step 2: Writing DataFrame to CSV file failed with error: {e}')


@keyword("Write DataFrame to PSV file")
def write_df_to_psv(df_to_write: pd.DataFrame, file_path: str, file_name: str):
    """
    This method is to write the df to psv file
    :param df_to_write: DataFrame to write to PSV file
    :param file_path: Path where the PSV file needs to be created
    :param file_name: Name of the PSV file to be created
    :return: None
    """
    logger.info('Step 1: Writing DataFrame to PSV file...')
    try:
        df_to_write.to_csv(path_or_buf=file_path + '/' + file_name, mode='w', sep='|', index=False)
        logger.info('Step 2: Writing DataFrame to PSV file completed successfully.')
    except Exception as e:
        logger.error(f'Step 2: Writing DataFrame to PSV file failed with error: {e}')


@keyword("Compare two DataFrames and show differences")
def df_diff(actual_file_path_name: str, expected_file_path_name: str, key_columns: list = None,
            ignore_columns: list = None):
    """
    This method is used to find the differences between two data frame
    :param actual_file_path_name: r'C://Desktop//Comparison//data//actual//'
    :param expected_file_path_name: r'C://Desktop//Comparison//data//baseline//'
    :param key_columns: unique key columns names as list ['Key_Column1', 'Key_Column2']
    :param ignore_columns: columns to ignore ['Ignore_Column1', 'Ignore_Column2']
    :return:
    """
    logger.info('****************************************************************************************************')
    logger.info('PandasUtil Data Frame Comparison - Cell by Cell comparison with detailed mismatch report')
    logger.info('****************************************************************************************************')
    logger.info('Step-01 : Based on file format create the data frames with delimiter(sep)')

    df1 = create_dataframe_from_file(actual_file_path_name)
    df2 = create_dataframe_from_file(expected_file_path_name)

    # Store total records in actual and expected df
    total_expected = round(len(df1))
    total_actual = round(len(df2))
    total_mismatch = total_expected - total_actual

    logger.info('Step-02 : Remove the columns based on ignore columns list')
    # If ignore columns are specified, remove those columns from comparison
    if len(ignore_columns) > 0:
        # Get column index type
        col_idx = df1.columns.get_loc(df1.columns.tolist()[0])

        # Iterate all the columns in ignore column list and if the column exist delete the column
        for col in ignore_columns:
            # Based on the column index type delete the column
            if isinstance(col_idx, int):
                if int(col) in df1.columns.tolist():
                    df1.drop(df1.columns[int(col)], axis=1, inplace=True)
            elif isinstance(col_idx, str):
                if col in df1.columns.tolist():
                    df1.drop(df1.columns[col], axis=1, inplace=True)

            if isinstance(col_idx, int):
                if int(col) in df2.columns.tolist():
                    df2.drop(df2.columns[int(col)], axis=1, inplace=True)
            elif isinstance(col_idx, str):
                if col in df2.columns.tolist():
                    df1.drop(df2.columns[col], axis=1, inplace=True)

    logger.info('Step-03 : Check for duplicate rows in both actual and expected')

    # Check for column differences in df1 and df2
    df1_col_diff = set(df1.columns) - set(df2.columns)
    df2_col_diff = set(df2.columns) - set(df1.columns)

    logger.info(df1_col_diff)
    df1_col_diff = set(df1.columns) - set(df2.columns)

    # If key column is not specified then consider all columns except last column
    if len(key_columns) == 0:
        key_columns = df1.columns.tolist()
        key_columns.pop()

    # Sort both expected and actual data frame
    df1.sort_values(by=key_columns, ascending=True, inplace=True)
    df2.sort_values(by=key_columns, ascending=True, inplace=True)

    # Check for duplicate key columns in expected and actual data frame
    df1_dup_df = df1[df1[key_columns].duplicated()]
    df2_dup_df = df2[df2[key_columns].duplicated()]

    logger.debug(df1_dup_df)
    logger.debug(df2_dup_df)
    logger.debug(len(df1_dup_df))
    logger.debug(len(df2_dup_df))

    total_expected_dup = round(len(df1_dup_df))
    total_actual_dup = round(len(df2_dup_df))

    logger.info('Step-04 : Remove duplicate records from actual and expected')

    # Get the duplicate key columns
    dup_expected_df = df1_dup_df.copy()
    dup_actual_df = df2_dup_df.copy()
    dup_expected_df['source'] = 'Expected'
    dup_actual_df['source'] = 'Actual'

    # Combine the duplicate keys from expected and actual data frame
    dup_cons_df = pd.concat([dup_expected_df, dup_actual_df], axis=0)
    dup_cons_df.reset_index(inplace=True)
    dup_cons_df.drop('index', axis=1, inplace=True)

    # Drop the duplicate columns before detailed comparison
    df1.drop_duplicates(key_columns, inplace=True)
    df2.drop_duplicates(key_columns, inplace=True)

    logger.debug(dup_expected_df)
    logger.debug(dup_actual_df)
    logger.debug(dup_cons_df)

    logger.info('Step-05 : Sort the actual and expected based on key columns and reset the index')

    # Sort df1 and df2 based on key columns and reset the index
    df1.sort_values(by=key_columns, ascending=True, inplace=True)
    df2.sort_values(by=key_columns, ascending=True, inplace=True)
    df1.reset_index(inplace=True)
    df2.reset_index(inplace=True)

    # Set the index based on key columns in df1 and df2. Remove the default index column
    df1 = df1.set_index(key_columns, drop=True, append=False, inplace=False, verify_integrity=True)
    df2 = df2.set_index(key_columns, drop=True, append=False, inplace=False, verify_integrity=True)
    df1 = df1.drop('index', axis=1)
    df2 = df2.drop('index', axis=1)

    logger.info('Step-06 : Identify the rows matching based on key in both actual and expected')

    # Identify the rows matching based on key in both df1 and df2
    merge_outer_df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True, indicator='source')
    # merge_outer_df = pd.merge(df1_key_columns, df2_key_columns, how='outer', on=key_columns, indicator='source')

    # Based on the key columns create key matched and mismatched details
    key_matched_df = merge_outer_df.loc[merge_outer_df['source'] == 'both'].copy()
    logger.debug(len(key_matched_df))
    key_mismatched_df = merge_outer_df.loc[merge_outer_df['source'] != 'both'].copy()
    key_mismatched_df = key_mismatched_df[['source']]

    key_matched_df['source'] = 'Matched'
    key_mismatched_df['source'] = 'MisMatched'
    logger.debug(key_mismatched_df)

    # Update the source column left_only to actual and right_only to expected
    # key_mismatched_df.loc[key_mismatched_df['source'] == 'left_only', 'source'] = 'Actual'

    expected_key_mismatch = len(key_mismatched_df[key_mismatched_df.source == 'left_only'])
    actual_key_mismatch = len(key_mismatched_df[key_mismatched_df.source == 'right_only'])

    logger.info('Step-07 : Create the summary report based on count diff, duplicate rows and key mismatches')

    # Create the executive summary df
    exec_summary_col = ['Summary', 'Expected', 'Actual', 'Mismatch']

    exec_summary_df = pd.DataFrame(columns=exec_summary_col)
    exec_summary_df.loc[1] = ['Total_Records', total_expected, total_actual, total_mismatch]
    exec_summary_df.loc[2] = ['Duplicates', total_expected_dup, total_actual_dup, 0]
    exec_summary_df.loc[3] = ['Key_Mismatch', expected_key_mismatch, actual_key_mismatch, 0]

    logger.debug(exec_summary_df)

    logger.info('Step-08 : Remove the mismatched key values and proceed further in validation')
    df1.drop(key_mismatched_df.loc[key_mismatched_df['source'] == 'left_only'].index, inplace=True)
    df2.drop(key_mismatched_df.loc[key_mismatched_df['source'] == 'right_only'].index, inplace=True)

    logger.info('Step-09 : Started cell by cell comparison for key values that exist in both actual and expected')
    # Verify if columns in both df1 and df2 are same
    assert (df1.columns == df2.columns).all(), logger.debug('Failed - Column mismatch determined')

    logger.info('Step-10 : Verify column data types in both the files, if not convert based on actual')
    if any(df1.dtypes != df2.dtypes):
        logger.debug('Data Types are different, trying to convert')
        df2 = df2.astype(df1.dtypes)

    logger.info('Step-11 : Verify cell by cell data in both the data frame and generate mismatch report')
    # df to hold cell by cell comparison results
    cell_comp_df = pd.DataFrame([])

    # Verify if all the cell data are identical
    if df1.equals(df2):
        logger.info('          Passed : Cell by Cell comparison')
    else:
        logger.info('          Failed : Cell by Cell comparison ..Started to extract mismatched column values')
        # create new data frame with mismatched columns
        diff_mask = (df1 != df2) & ~(df1.isnull() & df2.isnull())
        ne_stacked = diff_mask.stack()
        changed = ne_stacked[ne_stacked]
        key_columns.append('Mismatch_Column')
        changed.index.names = key_columns
        difference_locations = np.where(df1 != df2)
        changed_from = df1.values[difference_locations]
        changed_to = df2.values[difference_locations]
        cell_comp_df = pd.DataFrame({'Expected_Data': changed_from, 'Actual_Data': changed_to}, index=changed.index)
    logger.info('Step-12 : Comparison completed and generated info for reports(summary, keys mismatch, cell by cell')
    logger.info('****************************************************************************************************')
    return exec_summary_df, dup_cons_df, key_matched_df, key_mismatched_df, cell_comp_df

#
# *** Test Cases ***
# Test Write DataFrame to CSV file
#     ${df}=  Create Dataframe  1,2,3\n4,5,6\n7,8,9
#     Write DataFrame to CSV file  ${df}  ./  test.csv
#     ${written_df}=  Read CSV  ./test.csv
#     Should Be True  ${df}.equals(${written_df})
#
# Test Write DataFrame to PSV file
#     ${df}=  Create Dataframe  1,2,3\n4,5,6\n7,8,9
#     Write DataFrame to PSV file  ${df}  ./  test.psv
#     ${written_df}=  Read CSV  ./test.psv  delimiter=|
#     Should Be True  ${df}.equals(${written_df})
#
# Test Compare two DataFrames and show differences
#     ${actual_file_path}=  Set Variable  ./test_data/
#     ${expected_file_path}=  Set Variable  ./baseline_data/
#     ${actual_file_name}=  Set Variable  actual_file
#     ${expected_file_name}=  Set Variable  expected_file
#     ${file_format}=  Set Variable  csv
#     ${key_columns}=  Create List  Key_Column1  Key_Column2
#     ${ignore_columns}=  Create List  Ignore_Column1  Ignore_Column2
#     ${expected_df}=  Read CSV  ${expected_file_path}${expected_file_name}.${file_format}
#     ${actual_df}=  Read CSV  ${actual_file_path}${actual_file_name}.${file_format}
#     Compare two DataFrames and show differences  ${actual_file_path}  ${expected_file_path}  ${actual_file_name}  ${expected_file_name}  ${file_format}  ${key_columns}  ${ignore_columns}

# *** Settings ***
# Library  RFPandasUtils.py
#
# *** Test Cases ***
# Test Write DataFrame to CSV file
#    ${df}=  Create Dataframe  1,2,3\n4,5,6\n7,8,9
#    Write DataFrame to CSV file  ${df}  ./  test.csv
#    ${written_df}=  Read CSV  ./test.csv
#    Should Be True  ${df}.equals(${written_df})
#
# Test Write DataFrame to PSV file
#    ${df}=  Create Dataframe  1,2,3\n4,5,6\n7,8,9
#    Write DataFrame to PSV file  ${df}  ./  test.psv
#    ${written_df}=  Read CSV  ./test.psv  delimiter=|
#    Should Be True  ${df}.equals(${written_df})
#
# Test Compare two DataFrames and show differences
#    ${actual_file_path}=  Set Variable  ./test_data/
#    ${expected_file_path}=  Set Variable  ./baseline_data/
#    ${actual_file_name}=  Set Variable  actual_file
#    ${expected_file_name}=  Set Variable  expected_file
#    ${file_format}=  Set Variable  csv
#    ${key_columns}=  Create List  Key_Column1  Key_Column2
#    ${ignore_columns}=  Create List  Ignore_Column1  Ignore_Column2
#    ${expected_df}=  Read CSV  ${expected_file_path}${expected_file_name}.${file_format}
#    ${actual_df}=  Read CSV  ${actual_file_path}${actual_file_name}.${file_format}
#    Compare two DataFrames and show differences  ${actual_file_path}  ${expected_file_path}  ${actual_file_name}  ${expected_file_name}  ${file_format}  ${key_columns}  ${ignore_columns}
#

# *** Test Cases ***
# Read CSV file with header
#     [Documentation]    Read data from a CSV file with header
#     ${dataframe}=    Create Dataframe from file    ../tests/5m Sales Records.csv
#     Log    ${dataframe}
#
# Read CSV file without header
#     [Documentation]    Read data from a CSV file without header
#     ${dataframe}=    Create Dataframe from file    ../tests/5m Sales Records_without_header.csv    has_header=False
#     Log    ${dataframe}
#
# Read Excel file with header
#     [Documentation]    Read data from an Excel file with header
#     ${dataframe}=    Create Dataframe from file    ../tests/5m Sales Records.xlsx
#     Log    ${dataframe}
#
# Read Excel file without header
#     [Documentation]    Read data from an Excel file without header
#     ${dataframe}=    Create Dataframe from file    ../tests/5m Sales Records_without_header.xlsx    has_header=False
#     Log    ${dataframe}
#
# Read PSV file with header
#     [Documentation]    Read data from a PSV file with header
#     ${dataframe}=    Create Dataframe from file    ../tests/10000 Sales Records.psv    delimiter='|'
#     Log    ${dataframe}
#
# Read PSV file without header
#     [Documentation]    Read data from a PSV file without header
#     ${dataframe}=    Create Dataframe from file    ../tests/10000 Sales Records_without_header.psv    delimiter='|'    has_header=False
#     Log    ${dataframe}
