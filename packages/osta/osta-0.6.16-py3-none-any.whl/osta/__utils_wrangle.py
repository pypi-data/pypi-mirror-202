#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import osta.__utils as utils
import pandas as pd
import warnings
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pkg_resources
import numpy as np


def clean_data(df, log_file=False, **args):
    """
    Standardize data

    This function standardize the data that is in pandas.DataFrame. The
    function expects that columns are named in specific way. If the data
    does not meet requirements, the function gives a warning.

    Arguments:
        `df`: pandas.DataFrame containing invoice data.

        `**args`: Additional arguments passes into other functions:

        `date_format`: The format of date that will be in output data.
        (By default: date_format="%d-%m-%Y")

        `dayfirst`: Boolean value or None to specify the format of date
        in input data. 'If day comes before month in the date.'
        If None, function determines the format automatically.
        (By default: dayfirst=None)

        `yearfirst`: Boolean value or None to specify the format of date
        in input data. 'If year comes first in the date.'
        If None, function determines the format automatically.
        (By default: yearfirst=None)

        `country_format`: A string speciying the format of country in the
        output data. Must be one of the following options: 'name_fin',
        'name_en', "code_2char", 'code_3char', 'code_num', or 'code_iso'.
        (By default: country_format='code_2char')

        `pattern_th`: A numeric value [0,1] specifying the threshold of
        enough good match between names, e.g., 'org_name', and database.
        Value over threshold have enough strong pattern and it is
        interpreted to be a match. (By default: pattern_th=0.7)

        `scorer`: A scorer function passed into fuzzywuzzy.process.extractOne
        function that evaluates the match between names and database.
        (By default: scorer=fuzz.partial_ratio)

        `org_data`: pd.DataFrame or None. Database for organization data.
        Data must include on of the following columns: 'name', 'code', or
        'bid' specifying the name, code and business ID of organizations,
        respectively. If None, packages default database is used.
        (By default: org_data=None)

        `suppl_data`: pd.DataFrame or None. Database for supplier data.
        Data must include on of the following columns: 'name', 'code', or
        'bid' specifying the name, code and business ID of suppliers,
        respectively. If None, no database is used.
        (By default: org_data=None)

        `account_data`: pd.DataFrame or None. Database for account data.
        Data must include on of the following columns: 'name', or
        'code' specifying the name and number of accounts,
        respectively. If None, packages default database is used.
        (By default: account_data=None)

        `subset_account_data`: None or string to specify which database is
        used for account data. Available options are 'balance_sheet' and
        'income_statement'. If None, both databases are used and the result
        value will be the first occurence.
        (By default: subset_account_data=None)

        `service_data`: pd.DataFrame or None. Database for service data.
        Data must include on of the following columns: 'name', or
        'code' specifying the name and number of service categories,
        respectively. If None, packages default database is used.
        (By default: service_data=None)

        `db_year`: Integer value or None specifying the year (2021, 2021,
        or 2023) that will be used to match account and service data.
        If None, the most current information is used and duplicates from
        previous years are removed. (By default: db_year=None)

        `disable_*`: A boolean value specifying whether * data
        is checked. * can be one of the following options: 'org',
        'suppl', 'date', 'sums', 'country', 'voucher', 'account' or
        'service'. (By default: disable_*=False)

        `thresh`: An integer specifying the number of values each observation
        should contain to preserve it. Some datasets might have rows with
        additional information such as additional rows for price. These rows
        can be dropped by specifying thresh. For example, thresh=df.shape[0]-5
        removes all rows that have over 5 empty values. (By default: thresh=0)

        `check_na`: A boolean value specifying whether to notify if there are
        missing values in organization data. (By default: check_na=False)

        `log_file`: A boolean value or a single character value for specifying
        where log file will be stored. If True, all the messages are stored to
        a log file that can be found from osta direcotry that is located
        in devices default temporary directory. When False, messages are
        printed to screen and log file is not created.
        (By default: log_file=False)

        'verbose': A boolean value specifying whteher to show a progress bar.
        Disabled when 'df' is a single pd.DataFrame. (By default: verbose=True)

    Details:
        This function standardize the data and checks that it is in correct
        format. If the data is not in expected format containing erroneous
        data that cannot be standardized, the function gives a warning.
        Moreover, empty rows and columns along with spaces before or after
        values are removed.

        The function expects that columns are in specific format.
        Not all the columns must be included in the data. Below is a
        list of columns and what type of data they should have.

        org_name: Organization name.

        org_code: Organization number.

        org_bid: Organization business ID.

        account_name: The name of account to where invoice is allocated.

        account_code: The number of account to where incoice is
        allocated.

        service_name: The name of service category to where invoice
        is allocated.

        service_code: The number of service category to where invoice is
        allocated.

        suppl_name: Supplier name.

        suppl_code: Supplier number.

        suppl_bid: Supplier business ID.

        suppl_vat_number: VAT number of supplier.

        suppl_land: Country of supplier.

        doc_id: Running identification of invoice.

        doc_date: Date of invoice.

        price_ex_vat: Price excluding VAT.

        price_vat: Amount of VAT.

        price_total: Price indluding VAT.

        Organization data (name, number, BID) is matched with database.
        Uncorrect values are replaced with correct values unless the
        specified organization matches with multiple organizations in the
        database. The user can also use own database.

        Supplier data (name, number, BID, VAT number) is not matched with
        database by default and replacements are not done. However, user
        can use own database. Like in case of organization data, the function
        checks that BID and VAT numbers are in correct format and that they
        duplicated meaning that each value specifies only one supplier.

        Account and service information. Account and service information is
        matched with database, and uncorrect values are replaced unless they
        match with multiple accounts / service categories. For account data,
        user can specify if balance sheet or income statement database is used.
        Otherwise, both are used and first occurence will be the result value.
        The user can also use own database.

        Country is identified with database containing all common land codes.
        (Finnish and English names, 2 and 3-character codes, along with
        numeric and ISO code). User can define the format of output from
        formats included in the database.

        Date is automatically identified unless user do not define the format.
        Dates are converted into format that user can specify.

        Price excluding and including VAT and VAT amount (abbreviated as sums
        in the function) are checked by calculating if values of them match
        between each other. If all three columns are not available, the
        the function only converts values in float type if possible.

    Examples:
        ```
        # Create a dummy data
        data = {"org_name": ["Turun kaupunki", "Turku", "Turku"],
                "org_code": [None, None, None],
                "doc_date": ["02.01.2023", "2-1-2023", "1.1.2023"],
                "suppl_name": ["Myyjä", "Supplier Oy", "Myyjän tuote Oy"],
                "suppl_land": ["FI", "FI", "FI"],
                "price_total": [100.21, 10.30, 50.50],
                }
        df = pd.DataFrame(data)
        df = clean_data(df, country_format="name_fin")
        ```

    Output:
        pandas.DataFrame with standardized data.

    """
    # INPUT CHECK
    # df must be pandas DataFrame
    if not utils.__is_non_empty_df(df):
        raise Exception(
            "'df' must be non-empty pandas.DataFrame."
            )
    # INPUT CHECK END
    # Remove spaces from beginning and end of the value
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    # Replace empty strings with None
    df = df.replace(r'^\s*$', None, regex=True)
    # Check if there are empty rows or columns, and remove them
    if any(df.isna().all(axis=0)) or any(df.isna().all(axis=1)):
        df = df.dropna(axis=0, how="all")
        df = df.dropna(axis=1, how="all")
        warnings.warn(
            message="'df' contained empty rows or/and columns \n" +
            "that are now removed.\n",
            category=Warning
            )
    # Check if there are rows that are missing values
    df = __check_empty_observations(df, log_file=log_file, **args)
    # Check if there are duplicated values
    df = utils.__check_duplicated(df, log_file=log_file, **args)
    # Test if voucher is correct
    __check_voucher(df, log_file=log_file, **args)
    # Check sums
    df = __clean_sums(df, log_file=log_file, **args)
    # Check dates
    df = __standardize_date(df, log_file=log_file, **args)
    # Check org information:
    df = __standardize_org(df, log_file=log_file, **args)
    # Check supplier info
    df = __standardize_suppl(df, log_file=log_file, **args)
    # Check account info
    df = __standardize_account(df, log_file=log_file, **args)
    # Check service data
    df = __standardize_service(df, log_file=log_file, **args)
    # Check country data
    df = __standardize_country(
        df, log_file=log_file, cols_to_check=["suppl_land"], **args)
    df = __standardize_country(
        df, log_file=log_file, cols_to_check=["org_land"], **args)
    return df


def __standardize_country(
        df, log_file, cols_to_check, disable_country=False,
        country_format="code_2char", **args):
    """
    This function check standardize the used country format.
    Input: df
    Output: df
    """
    # INPUT CHECK
    if not isinstance(disable_country, bool):
        raise Exception(
            "'disable_country' must be True or False."
            )
    # Check if column(s) is found as non-duplicated
    cols_to_check = utils.__not_duplicated_columns_found(df, cols_to_check)
    if disable_country or len(cols_to_check) == 0:
        return df
    # INPUT CHECK END
    # Load data base
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_land.csv")
    country_codes = pd.read_csv(path, index_col=0, dtype=str)
    # country_format must be one of the database columns
    if not (isinstance(country_format, str) and
            country_format in country_codes.columns):
        raise Exception(
            f"'country_format' must be one of the following options\n."
            f"{country_codes.columns.tolist()}"
            )
    # INPUT CHECK END
    # Get country data from df
    df_country = df[cols_to_check]
    # Get unique countries
    df_country = df_country.drop_duplicates()
    # Loop over values and add info on them
    not_found = pd.DataFrame()
    for i, x in df_country.iterrows():
        # Get the country from data base; case insensitive search
        ind = country_codes.applymap(
            lambda col: str(col).lower()).isin(
                x.astype(str).str.lower().values.tolist()).sum(axis=1) > 0
        if any(ind):
            temp = country_codes.loc[ind, :]
            # Assing result to original DF
            df.loc[df[cols_to_check[0]] == x[0], cols_to_check[0]] = temp[
                country_format].values[0]
        else:
            not_found = pd.concat([not_found, x], axis=1)
    # If some countries were not detected
    if not_found.shape[1] > 0:
        if log_file:
            msg = "The following countries were not detected. \
                Please check them for errors."
            utils.__log_to_file(not_found, log_file, "country.csv", msg)
        else:
            warnings.warn(
                message=f"The following countries were not detected. "
                f"Please check them for errors: \n{not_found}",
                category=Warning
                )
    return df


def __clean_sums(df, log_file, disable_sums=False, to_positive=False, **args):
    """
    This function checks that sums (total, vat, netsum) are in float format,
    and tries to convert them if they are not. Futhermore, if one field is
    missing, it is calculated based on others.
    Input: df
    Output: df
    """
    # INPUT CHECK
    if not isinstance(disable_sums, bool):
        raise Exception(
            "'disable_sums' must be True or False."
            )
    if not isinstance(to_positive, bool):
        raise Exception(
            "'to_positive' must be True or False."
            )
    # Check if column(s) is found as non-duplicated
    cols_df = ["price_total", "price_vat", "price_ex_vat"]
    cols_to_check = utils.__not_duplicated_columns_found(df, cols_df)
    if disable_sums or len(cols_to_check) == 0:
        return df
    # INPUT CHECK END
    # Get columns that are missing from the data
    cols_missing = [x for x in cols_df if x not in cols_to_check]

    # If data is not float, try to make it as float
    if len(cols_to_check) > 0 and not all(df.dtypes[
            cols_to_check] == "float64"):
        # Get those column names that need to be modified
        cols_not_float = df.dtypes[cols_to_check][
            df.dtypes[cols_to_check] != "float64"].index
        # Loop throug columns
        for col in cols_not_float:
            # Replace "," with "." and remove spaces
            df[col] = df[col].astype(str).str.replace(",", ".")
            # Try to convert values as float
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                warnings.warn(
                    message=f"The following column cannot be converted into "
                    f"float: {col}",
                    category=Warning
                    )
    # Calcute the expected value, and check if it's matching
    if len(cols_missing) == 0 and all(df.dtypes[cols_to_check] == "float64"):
        test = df["price_ex_vat"] + df["price_vat"]
        # Get columns that do not match
        temp = df.loc[np.round(df["price_total"], 2) != np.round(test, 2),
                      cols_to_check]
        # If any unmatching was found
        if temp.shape[0] > 0:
            temp = temp.drop_duplicates()
            if log_file:
                msg = "The sums of following rows do not match. \
                    Please check them for errors."
                utils.__log_to_file(temp, log_file, "sum.csv", msg)
            else:
                warnings.warn(
                    message=f"The sums of following rows do not match. Please "
                    f"check them for errors: \n{temp}",
                    category=Warning
                    )
    # If there are negative values, give warning
    if any(df.dtypes[cols_to_check] == "float64"):
        # Take indices of rows that have negative values
        df_temp = df.loc[:, cols_to_check]
        ind = (df_temp.loc[:, df_temp.dtypes == "float64"
                           ] < 0).sum(axis=1) > 0
        if any(ind) and log_file:
            msg = "The following rows include negative values. \
                Please check them for errors."
            utils.__log_to_file(
                df.loc[ind, cols_to_check], log_file, "sum.csv", msg)
        elif any(ind) > 0:
            warnings.warn(
                message=f"The following rows include negative values. Please "
                f"check them for errors: \n{df.loc[ind, cols_to_check]}",
                category=Warning
                )
    # Convert negative values to positive values if specified
    if any(df.dtypes[cols_to_check] == "float64") and to_positive:
        df.loc[:, df.dtypes[cols_to_check] == "float64"] = df.loc[
            :, df.dtypes[cols_to_check] == "float64"].abs()
    return df


def __standardize_date(
        df, log_file, disable_date=False, date_format="%d-%m-%Y",
        dayfirst=None, yearfirst=None, **args):
    """
    This function identifies the format of dates and standardize them.
    Input: df
    Output: df
    """
    # INPUT CHECK
    if not isinstance(disable_date, bool):
        raise Exception(
            "'disable_date' must be True or False."
            )
    # Check if column(s) is found as non-duplicated
    cols_to_check = ["doc_date"]
    cols_to_check = utils.__not_duplicated_columns_found(df, cols_to_check)
    if disable_date or len(cols_to_check) == 0:
        return df
    col_to_check = cols_to_check[0]
    # dayfirst and yearfirst must be None or boolean value
    if not (isinstance(dayfirst, bool) or dayfirst is None):
        raise Exception(
            "'dayfirst' must be True or False or None."
            )
    if not (isinstance(yearfirst, bool) or yearfirst is None):
        raise Exception(
            "'yearfirst' must be True or False or None."
            )
    # INPUT CHECK END
    convert_date = False
    # Get date column
    df_date = df.loc[:, col_to_check]
    # Split dates from separator. Result is multiple columns
    # with year, month and day separated
    df_date_mod = df_date.astype(str).str.split(r"[-/.]", expand=True)
    # If the date is in long format containing also time
    if any(df_date.astype(str).str.len() > 10):
        try:
            df_date_mod = pd.to_datetime(df_date)
            # Default settings
            yearfirst = True
            dayfirst = False
            convert_date = True
        except Exception:
            pass
    elif df_date_mod.shape[1] > 1:
        # If the split was succesful and there are only day, month, and year
        # Get format of dates if None
        if not (isinstance(dayfirst, bool) or isinstance(yearfirst, bool)):
            df_date_mod, dayfirst, yearfirst = __get_format_of_dates_w_sep(
                df_date_mod)
        convert_date = True
    # Try to reformat DDMMYYYY format
    elif utils.__test_if_date(df_date_mod.iloc[:, 0], wo_sep=True):
        # Get only the series
        df_date_mod = df_date_mod.iloc[:, 0]
        # Get format of date
        char_len = int(max(df_date_mod.astype(str).str.len()))
        # Get format of dates if None
        if dayfirst is None or yearfirst is None:
            dayfirst, yearfirst = __get_format_of_dates_wo_sep(df_date_mod)
        # If format was found, standardize
        if dayfirst is not None and yearfirst is not None:
            # Add separators to dates
            df_date_mod = __convert_dates_without_sep(
                df_date_mod,
                char_len=char_len,
                dayfirst=dayfirst,
                yearfirst=yearfirst)
            convert_date = True
    # Convert dates
    if convert_date and dayfirst is not None and yearfirst is not None:
        # Standardize dates
        df[col_to_check] = pd.to_datetime(df_date_mod, dayfirst=dayfirst,
                                          yearfirst=yearfirst,
                                          errors="coerce")
        # Change the formatting
        df[col_to_check] = df[col_to_check].dt.strftime(date_format)
        # Check if there were Nones
        df_date = df_date[df.loc[:, col_to_check].isna()]
        if df_date.shape[0] > 0:
            if log_file:
                msg = "The format of following dates were not detected, and \
                    they are converted to NaN. Please check them for errors."
                utils.__log_to_file(df_date.copy(), log_file, "date.csv", msg)
            else:
                warnings.warn(
                    message=f"The format of following dates were not"
                    f"detected, and they are converted to NaN. "
                    f"Please check them for errors: {df_date.values.tolist()}",
                    category=Warning
                    )
    else:
        warnings.warn(
            message="The format of dates where not detected, "
            "and the 'date' column is unchanged. Please check that dates "
            "have separators between days, months, and years.",
            category=Warning
            )
    return df


def __get_format_of_dates_w_sep(df):
    """
    This function identifies the format of dates that are with
    separators between days, months and years. Furthermore, date is modified so
    that year has 4 characters and separators between days, months and years
    are uniformed.
    Input: df with days months and years in own columns
    Output: Modified df, if year comes first, if day comes first
    """
    # Disable day convert by default
    dayfirst = None
    yearfirst = None
    df_date = None
    # Check if columns can be converted into int. If not, do not
    if not all([all(df[x].astype(str).str.isdigit()) for x in df.columns]):
        return [df_date, dayfirst, yearfirst]
    # Get the number of characters in each column If there are some column with
    # 4 characters, year is in longer format
    year_len = 4 if any(
        np.vectorize(len)(df.values.astype(str)).max(axis=0) == 4) else 2
    # Get values which should match
    if year_len == 4:
        year = list(range(1970, 2050))
    else:
        year = list(range(15, 50))
    month = list(range(1, 13))
    day = list(range(1, 32))

    # Loop over columns. Are the values matching with days, months or years?
    res = pd.DataFrame()
    for i, x in enumerate(df.columns):
        # Get value
        temp_val = df.iloc[:, i].astype(int)
        # Get matches
        is_day = (max(day) >= temp_val.max() and temp_val.min() >= min(day))
        is_month = (max(month) >= temp_val.max()
                    and temp_val.min() >= min(month))
        is_year = (max(year) >= temp_val.max() and temp_val.min() >= min(year))
        # Add to DF
        temp = pd.DataFrame([is_day, is_month, is_year])
        temp.index = ["is_day", "is_month", "is_year"]
        res = pd.concat([res, temp], axis=1)
    # Results to columns, rows are original dates separated from separator
    res = res.transpose()

    # If year has only 2characters, take first days. Otherwise, take years
    if year_len == 2:
        day_res = (res["is_day"].values &
                   ~res["is_month"].values & ~res["is_year"].values)
        year_res = ~res["is_month"].values & res["is_year"].values
    else:
        year_res = (~res["is_day"].values &
                    ~res["is_month"].values & res["is_year"].values)
        day_res = (res["is_day"].values & ~res["is_month"].values)

    # Get indices of matches; if this date columns has days or years?
    day_res = day_res.nonzero()[0]
    year_res = year_res.nonzero()[0]
    # If only one match per day/year was found, get the final date format
    if len(day_res) == 1 and len(year_res) == 1:
        yearfirst = True if year_res == 0 else False
        if yearfirst:
            # Get format
            dayfirst = True if day_res == 1 else False
            # Get values
            dd = (df.iloc[:, 1] if dayfirst else df.iloc[:, 2])
            dd = dd.str.zfill(2)
            mm = (df.iloc[:, 2] if dayfirst else df.iloc[:, 1])
            mm = mm.str.zfill(2)
            yyyy = (df.iloc[:, 0] if year_len == 4 else
                    "20" + df.iloc[:, 0].str.zfill(2))
            # Create a date in YYYY/XX/XX format
            df_date = ((yyyy + "/" + dd + "/" + mm) if
                       dayfirst else (yyyy + "/" + mm + "/" + dd))
        else:
            # Get format
            dayfirst = True if day_res == 0 else False
            # Get values
            dd = (df.iloc[:, 0] if dayfirst else df.iloc[:, 1])
            dd = dd.str.zfill(2)
            mm = (df.iloc[:, 1] if dayfirst else df.iloc[:, 0])
            mm = mm.str.zfill(2)
            yyyy = (df.iloc[:, 2] if year_len == 4 else
                    "20" + df.iloc[:, 2].str.zfill(2))
            # Create a date in YYYY/XX/XX format
            df_date = ((dd + "/" + mm + "/" + yyyy) if
                       dayfirst else (mm + "/" + dd + "/" + yyyy))
    df_date = pd.Series(df_date)
    return [df_date, dayfirst, yearfirst]


def __get_format_of_dates_wo_sep(df):
    """
    This function identifies the format of dates that are without
    separators between days, months and years.
    Input: series
    Output: If year comes first, if day comes first
    """
    # Get maximum number of characters
    char_len = int(max(df.astype(str).str.len()))
    yearfirst = None
    dayfirst = None
    if char_len == 8 or char_len == 6:
        # Expected year range
        years = list(range(1970, 2050)) if char_len == 8 else list(
            range(15, 50))
        # Get only those values that have maximum number of characters
        ind = df.astype(str).str.len() == char_len
        date_temp = df[ind]

        # Find place of year
        year_len = 4 if char_len == 8 else 2
        i = 0
        j = year_len
        res_year = pd.DataFrame()
        for x in range(0, char_len-1, year_len):
            i_temp = i + x
            j_temp = j + x
            temp = date_temp.astype(str).str[i_temp:j_temp]
            # Which values are between expected years?
            res = max(years) >= int(max(temp)) >= min(years)
            # Add to DF
            res = pd.DataFrame([i_temp, j_temp, res], index=["i", "j", "res"])
            res_year = pd.concat([res_year, res], axis=1)
        # Adjust column names
        res_year.columns = range(res_year.shape[1])
        # Get values based on results
        i_year = [res_year.loc["i", x] for i, x in enumerate(res_year.columns)
                  if res_year.loc["res", x]]
        j_year = [res_year.loc["j", x] for i, x in enumerate(res_year.columns)
                  if res_year.loc["res", x]]
        # Get only the individual values, if there are only one valid result
        if (len(i_year) == 1 and len(j_year) == 1):
            i_year_ind = int(i_year[0])
            j_year_ind = int(j_year[0])
            # Remove year from dates
            if i_year_ind == 0:
                date_temp = date_temp.astype(str).str[j_year_ind:]
            else:
                date_temp = date_temp.astype(str).str[:i_year_ind]
            # Get place of the year
            yearfirst = True if i_year_ind == 0 else False
    # If year was found
    if yearfirst is not None:
        # Expected day and month ranges
        months = list(range(1, 13))
        days = list(range(1, 32))
        # Ger place of the month and day
        i = 0
        j = 2
        res_day = pd.DataFrame()
        for x in range(0, char_len-year_len-1, 2):
            i_temp = i + x
            j_temp = j + x
            temp = date_temp.astype(str).str[i_temp:j_temp]
            # Which values are between expected days?
            res_d = max(days) >= int(max(temp)) >= min(days)
            # Which values are between expected months?
            res_m = max(months) >= int(max(temp)) >= min(months)
            # Add to DF
            res = pd.DataFrame([res_d, res_m], index=["day", "month"])
            res_day = pd.concat([res_day, res], axis=1)
        # Adjust column names
        res_day.columns = range(res_day.shape[1])
        # Get index of where month is located
        month_i = [i for i, x in enumerate(res_day.columns)
                   if res_day.loc["day", x] and res_day.loc["month", x]]
        if len(month_i) == 1:
            month_ind = int(month_i[0])
            # If month was the latter
            dayfirst = True if month_ind == res_day.shape[1]-1 else False
    # Combine result
    result = [dayfirst, yearfirst]
    return result


def __convert_dates_without_sep(df, char_len, dayfirst, yearfirst):
    """
    This function standardizes the dates that are without
    separators between days, months and years.
    Input: series
    Output: list of values with separators
    """
    # Create result DF and add columns
    res = pd.DataFrame(df)
    res.columns = ["original"]
    res = res.assign(mod=res["original"])
    res = res.assign(day=None)
    res = res.assign(month=None)
    res = res.assign(year=None)

    # Modify first values that have maximum amount of characters
    year_len = 4 if char_len == 8 else 2
    # Get the year based on yearfirst, and remove year from dates
    if yearfirst:
        year = res["mod"].astype(str).str[:year_len]
        res["mod"] = res["mod"].astype(str).str[year_len:]
    else:
        year = res["mod"].astype(str).str[-year_len:]
        res["mod"] = res["mod"].astype(str).str[:-year_len]
    # Add year to results
    res["year"] = year

    # Add days and months for sure cases (2 or 1 characters for both days
    # and months)
    for i in [1, 2]:
        dm_len = char_len-year_len if i == 2 else char_len-year_len-2
        ind = res["mod"].astype(str).str.len() == dm_len
        # Based on dayfirst, get values; remove them from mod column
        if dayfirst:
            day = res.loc[ind, "mod"].astype(str).str[:i]
            month = res.loc[ind, "mod"].astype(str).str[i:]
        else:
            month = res.loc[ind, "mod"].astype(str).str[:i]
            day = res.loc[ind, "mod"].astype(str).str[i:]
        # Add to data
        res.loc[ind, "day"] = day
        res.loc[ind, "month"] = month
        # Remove from mod column
        res.loc[ind, "mod"] = ""

    # For values that have 3 character, we have to do differently, because
    # we cannot be sure what values are months and what day.
    # Determine this by looking a common pattern
    # Expected day and month ranges
    if any(res["mod"] != ""):
        months = list(range(1, 13))
        days = list(range(1, 32))
        # Get indices where day+month has 3 characters
        ind = res["mod"].astype(str).str.len() == 3

        # Get tests ranges; in which range 1st and 2nd set of values should be?
        temp_test1 = days if dayfirst else months
        temp_test2 = months if dayfirst else days
        res_day = pd.DataFrame()
        # Loop over number of characters that values can have
        for i in [1, 2]:
            # Get values
            temp1 = res["mod"].astype(str).str[:i]
            temp2 = res["mod"].astype(str).str[i:]
            # Test values
            temp1 = max(temp_test1) >= int(max(temp1)) >= min(temp_test1)
            temp2 = max(temp_test2) >= int(max(temp2)) >= min(temp_test2)
            # Add to DF
            len1 = i
            len2 = max(res["mod"].astype(str).str.len())-i
            temp = pd.DataFrame([len1, len2, temp1, temp2])
            res_day = pd.concat([res_day, temp], axis=1)
        # Adjust index and column names
        index = ["day", "month"] if dayfirst else ["month", "day"]
        res_day.index = ["len1", "len2"] + index
        res_day.columns = range(res_day.shape[1])
        # Get values where the pattern is correct; how many characters
        # days and months have?
        res_i = res_day.loc[index, :].sum(axis=0) == res_day.loc[
            index, :].shape[0]
        if sum(res_i) == 1:
            res_day = res_day.loc[["len1", "len2"], res_i]
            # Get place of the month and day, based on dayfirst
            if dayfirst:
                day = res.loc[ind, "mod"].astype(str).str[
                    :res_day.loc["len1"].values[0]]
                month = res.loc[ind, "mod"].astype(str).str[
                    res_day.loc["len1"].values[0]:]
            else:
                month = res.loc[ind, "mod"].astype(str).str[
                    :res_day.loc["len1"].values[0]]
                day = res.loc[ind, "mod"].astype(str).str[
                    res_day.loc["len1"].values[0]:]
            # Add to data
            res.loc[ind, "day"] = day
            res.loc[ind, "month"] = month
            # Remove from mod column
            res.loc[ind, "mod"] = ""

    # Combine result to date with separators
    res = res["day"] + "/" + res["month"] + "/" + res["year"]
    return res


def __standardize_org(df, log_file, disable_org=False, org_data=None, **args):
    """
    This function prepares organization data to be checked, and calls
    function that checks it.
    Input: df
    Output: df with standardized organization data
    """
    # INPUT CHECK
    if not (utils.__is_non_empty_df(org_data) or org_data is None):
        raise Exception(
            "'org_data' must be non-empty pandas.DataFrame or None."
            )
    if not isinstance(disable_org, bool):
        raise Exception(
            "'disable_org' must be True or False."
            )
    # Check if column(s) is found as non-duplicated
    cols_df = ["org_bid", "org_vat_number", "org_code", "org_name"]
    cols_to_check = utils.__not_duplicated_columns_found(df, cols_df)
    if disable_org or len(cols_to_check) == 0:
        return df
    # INPUT CHECK END
    if org_data is None:
        path = pkg_resources.resource_filename(
            "osta", "resources/" + "data_municipality.csv")
        org_data = pd.read_csv(path, dtype=str)
    # Column of db that are matched with columns that are being checked
    # Subset to match with cols_to_check
    cols_to_match = ["bid", "vat_number", "code", "name"]
    cols_to_match = [cols_to_match[i] for i, x in enumerate(cols_df)
                     if x in cols_to_check]
    # Standardize organization data
    df = __standardize_based_on_db(df=df, df_db=org_data,
                                   cols_to_check=cols_to_check,
                                   cols_to_match=cols_to_match,
                                   log_file=log_file, data_type="org",
                                   **args)
    # If organization data was not in database, it is not checked.
    __check_org_data(df, cols_to_check, log_file, "org", **args)
    return df


def __standardize_account(
        df, log_file, disable_account=False, account_data=None,
        subset_account_data=None, db_year=None, **args):
    """
    This function prepares account data to be checked, and calls
    function that checks it.
    Input: df
    Output: df with standardized organization data
    """
    # INPUT CHECK
    if not (utils.__is_non_empty_df(account_data) or account_data is None):
        raise Exception(
            "'account_data' must be non-empty pandas.DataFrame or None."
            )
    if not isinstance(disable_account, bool):
        raise Exception(
            "'disable_account' must be True or False."
            )
    if not (subset_account_data is None or
            subset_account_data == "balance_sheet" or
            subset_account_data == "income_statement"):
        raise Exception(
            "'subset_account_data' must be 'balance_sheet', "
            "'income_statement' or None."
            )
    if not (db_year is None or isinstance(db_year, str) or
            isinstance(db_year, int) or isinstance(db_year, pd.Series)):
        raise Exception(
            "'db_year' must be None, string or integer specifying a year."
            )
    # Check if column(s) is found as non-duplicated
    cols_df = ["account_code", "account_name"]
    cols_to_check = utils.__not_duplicated_columns_found(df, cols_df)
    if disable_account or len(cols_to_check) == 0:
        return df
    # INPUT CHECK END
    subset_based_on_year = True
    if account_data is None:
        path = pkg_resources.resource_filename(
            "osta", "resources/" + "data_account.csv")
        account_data = pd.read_csv(path, index_col=0, dtype=str)
        # Subset by taking only specific years
        if db_year is not None:
            account_data = utils.__subset_data_based_on_year(
                df, df_db=account_data, db_year=db_year, **args)
            subset_based_on_year = False
        # If user specified balance sheet or income statement,
        # get only specified accounts
        if subset_account_data is not None:
            account_data = account_data.loc[
                :, account_data["cat_1"] == subset_account_data]
    # Column of db that are matched with columns that are being checked
    # Subset to match with cols_to_check
    cols_to_match = ["code", "name", "year"]
    cols_to_match = [cols_to_match[i] for i, x in enumerate(cols_df)
                     if x in cols_to_check]
    # Test if year can be fetched based on the data
    year = None
    if "doc_date" in df.columns and \
        "year" in account_data.columns and \
            subset_based_on_year:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                date = df["doc_date"].astype(str)
                year = pd.to_datetime(date).dt.year
        except Exception:
            pass
    # If the year was found, check data based on years
    year_not_found = []
    if year is not None:
        for y in year.drop_duplicates():
            temp_df = df.loc[year == y, :]
            temp_account = account_data.loc[account_data["year"] == y, :]
            # If year was found from the database
            if temp_account.shape[0] > 0:
                # Standardize organization data
                temp_df = __standardize_based_on_db(
                    df=temp_df, df_db=temp_account,
                    cols_to_check=cols_to_check,
                    cols_to_match=cols_to_match,
                    log_file=log_file, data_type="account",
                    disable_partial=True, **args)
                # Add data back
                df.loc[year == y, :] = temp_df
            else:
                year_not_found.append(y)
    else:
        # Standardize organization data without year information
        df = __standardize_based_on_db(
            df=df, df_db=account_data, cols_to_check=cols_to_check,
            cols_to_match=cols_to_match, disable_partial=True,
            log_file=log_file, data_type="account", **args)
    # Give warning if year was not found
    if len(year_not_found) > 0:
        warnings.warn(
            message=f"'The following years were not found from the account "
            f"data and they are not checked: {year_not_found}",
            category=Warning
            )
    # Check that values are matching
    __check_variable_pair(df, cols_to_check=cols_to_check)
    return df


def __standardize_service(
        df, log_file, disable_service=False, service_data=None,
        db_year=None, **args):
    """
    This function prepares service data to be checked, and calls
    function that checks it.
    Input: df
    Output: df with standardized organization data
    """
    # INPUT CHECK
    if not (utils.__is_non_empty_df(service_data) or service_data is None):
        raise Exception(
            "'service_data' must be non-empty pandas.DataFrame or None."
            )
    if not isinstance(disable_service, bool):
        raise Exception(
            "'disable_service' must be True or False."
            )
    if not (db_year is None or isinstance(db_year, str) or
            isinstance(db_year, int) or isinstance(db_year, pd.Series)):
        raise Exception(
            "'db_year' must be None, string or integer specifying a year."
            )
    # Check if column(s) is found as non-duplicated
    cols_df = ["service_code", "service_name"]
    cols_to_check = utils.__not_duplicated_columns_found(df, cols_df)
    if disable_service or len(cols_to_check) == 0:
        return df
    # INPUT CHECK END
    subset_based_on_year = True
    if service_data is None:
        path = path = pkg_resources.resource_filename(
            "osta", "resources/" + "data_service.csv")
        service_data = pd.read_csv(path, index_col=0, dtype=str)
        # Subset by taking only specific years
        if db_year is not None:
            service_data = utils.__subset_data_based_on_year(
                df, df_db=service_data, db_year=db_year, **args)
            subset_based_on_year = False
    # Column of db that are matched with columns that are being checked
    # Subset to match with cols_to_check
    cols_to_match = ["code", "name"]
    cols_to_match = [cols_to_match[i] for i, x in enumerate(cols_df)
                     if x in cols_to_check]
    # Test if year can be fetched based on the data
    year = None
    if "doc_date" in df.columns and \
        "year" in service_data.columns and \
            subset_based_on_year:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                date = df["doc_date"].astype(str)
                year = pd.to_datetime(date).dt.year
        except Exception:
            pass
    # If the year was found, check data based on years
    year_not_found = []
    if year is not None:
        for y in year.drop_duplicates():
            temp_df = df.loc[year == y, :]
            temp_service = service_data.loc[service_data["year"] == y, :]
            # If year was found from the database
            if temp_service.shape[0] > 0:
                # Standardize service data
                temp_df = __standardize_based_on_db(
                    df=temp_df, df_db=temp_service,
                    cols_to_check=cols_to_check,
                    cols_to_match=cols_to_match,
                    log_file=log_file, data_type="service",
                    disable_partial=True, **args)
                # Add data back
                df.loc[year == y, :] = temp_df
            else:
                year_not_found.append(y)
    else:
        # Standardize organization data without year information
        df = __standardize_based_on_db(
            df=df, df_db=service_data, cols_to_check=cols_to_check,
            cols_to_match=cols_to_match, disable_partial=True,
            log_file=log_file, data_type="service", **args)
    # Give warning if year was not found
    if len(year_not_found) > 0:
        warnings.warn(
            message=f"'The following years were not found from the service "
            f"data and they are not checked: {year_not_found}",
            category=Warning
            )
    # Check that values are matching
    __check_variable_pair(df, cols_to_check=cols_to_check)
    return df


def __standardize_suppl(
        df, log_file, disable_suppl=False, suppl_data=None, **args):
    """
    This function prepares supplier data to be checked, and calls
    function that checks it.
    Input: df
    Output: df with standardized supplier data
    """
    # INPUT CHECK
    if not (utils.__is_non_empty_df(suppl_data) or suppl_data is None):
        raise Exception(
            "'suppl_data' must be non-empty pandas.DataFrame or None."
            )
    if not isinstance(disable_suppl, bool):
        raise Exception(
            "'disable_suppl' must be True or False."
            )
    # Check if column(s) is found as non-duplicated
    cols_df = ["suppl_bid", "suppl_vat_number", "suppl_code", "suppl_name",
               "suppl_land"]
    cols_to_check = utils.__not_duplicated_columns_found(df, cols_df)
    if disable_suppl or len(cols_to_check) == 0:
        return df
    # INPUT CHECK END
    if suppl_data is not None:
        # Column of db that are matched with columns that are being checked
        # Subset to match with cols_to_check
        cols_to_match = ["bid", "vat_number", "code", "name", "land"]
        cols_to_match = [cols_to_match[i] for i, x in enumerate(cols_df)
                         if x in cols_to_check]
        # Standardize organization data
        df = __standardize_based_on_db(df=df, df_db=suppl_data,
                                       cols_to_check=cols_to_check,
                                       cols_to_match=cols_to_match,
                                       log_file=log_file, data_type="suppl",
                                       **args)
    # Check that data is not duplicated, BID is correct, and there are not
    # empty values. Get warning if there are.
    # Check VAT numbers
    __check_vat_number(
        df, cols_to_check=["suppl_bid", "suppl_vat_number", "suppl_land"],
        log_file=log_file, **args)
    __check_org_data(df, cols_to_check, log_file, "suppl", **args)
    return df


def __standardize_based_on_db(df, df_db,
                              cols_to_check, cols_to_match,
                              log_file, data_type,
                              pattern_th=0.7, scorer=fuzz.partial_ratio,
                              disable_partial=False,
                              **args):
    """
    Standardize the data based on database.
    Input: df, df_db including database,
    pattern_th to be used to match partial matching names
    Output: Standardized data
    """
    # INPUT CHECK
    # pattern_th must be numeric value 0-1
    if not utils.__is_percentage(pattern_th):
        raise Exception(
            "'pattern_th' must be a number between 0-1."
            )
    # Value [0,1] to a number between 0-100, because fuzzywuzzy requires that
    pattern_th = pattern_th*100
    # INPUT CHECK END
    # Create copy to avoid warnings related to assigning just a slice of data
    df = df.copy()
    # Which column are found from df and df_db
    cols_df = [x for x in cols_to_check if x in df.columns]
    cols_df_db = [x for x in cols_to_match if x in df_db.columns]
    # Drop those columns that do not have match in other df
    if len(cols_df) > len(cols_df_db):
        cols_to_check = [cols_df[cols_to_match.index(x)] for x in cols_df_db]
        cols_to_match = cols_df_db
    else:
        cols_to_match = [cols_df_db[cols_to_check.index(x)] for x in cols_df]
        cols_to_check = cols_df
    # If matching columns between df and data base were found
    if len(cols_to_check) > 0 and len(cols_to_match) > 0:
        # Subset the data
        df_org = df.loc[:, cols_to_check]
        # Drop duplicates from the database
        df_db = df_db.drop_duplicates(subset=cols_to_match)
        # Drop duplicates so we can focus on unique rows
        org_uniq = df_org.drop_duplicates()
        # Get matching values from database; replace incorrect values in
        # table including only unique values
        org_uniq_mod = __get_matches_from_db(
            df=org_uniq, df_db=df_db, cols_to_check=cols_to_check,
            cols_to_match=cols_to_match, pattern_th=pattern_th,
            disable_partial=disable_partial, scorer=scorer,
            log_file=log_file, data_type=data_type)
        # Replace values in original DataFrame columns
        df_org = __replace_old_values_with_new(df=df_org,
                                               old_values=org_uniq,
                                               new_values=org_uniq_mod,
                                               cols_to_check=cols_to_check,
                                               cols_to_match=cols_to_match)
        # Assign data back to original data, if some values were changed
        if any((df.loc[:, cols_to_check].fillna("") !=
                df_org.fillna("")).sum(axis=1) > 0):
            df.loc[:, cols_to_check] = df_org
    # If no matching columns were found from the data base
    elif len(cols_to_match) == 0:
        temp = cols_to_check[0].split("_")[0]
        warnings.warn(
            message=f"'{temp}' should include at least one of the "
            "following columns: 'name' (name), 'code' "
            "(number), and 'bid' (business ID for organization and "
            f"supplier data).",
            category=Warning
            )
    return df


def __check_org_data(
        df, cols_to_check, log_file, data_type, check_na=False, **args):
    """
    Check if organization data is not duplicated or has empty values, or
    incorrect business IDs.
    Input: df, columns that contain organization information
    Output: which rows are incorrect? None if check were not made
    """
    # INPUT CHECK
    if not isinstance(check_na, bool):
        raise Exception(
            "'check_na' must be True or False."
            )
    # INPUT CHECK END
    # Which column are found from df
    cols_to_check = [x for x in cols_to_check if x in df.columns]
    # If any columns were found
    res = None
    if len(cols_to_check) > 0:
        # Subset the data
        df = df.loc[:, cols_to_check]
        # Drop duplicates:
        # now there should be only unique number, name, ID combinations
        df = df.drop_duplicates()
        # Are there None values
        if check_na:
            res = df.isna().sum(axis=1) > 0
        else:
            res = [False] * df.shape[0]
        # BIDs found?
        if any(i in cols_to_check for i in ["org_bid", "suppl_bid"]):
            # Get bid column
            col_to_check = [x for x in ["org_bid", "suppl_bid"]
                            if x in cols_to_check][0]
            # Get BIDs
            col = df[col_to_check]
            # Check that bids are valid; True if not valid
            valid = utils.__are_valid_bids(col).values
            # Are bids duplicated?
            temp = df.loc[:, cols_to_check]
            temp = temp.drop_duplicates()
            freq = temp[col_to_check]
            freq = freq[freq.notna()].value_counts()
            uniq = freq[(freq > 1).values].index.tolist()
            duplicated = col.isin(uniq)
            # Update result
            res = res | ~valid | duplicated
        # Name found?
        if any(i in cols_to_check for i in ["org_name", "suppl_name"]):
            # Get column
            col_to_check = [x for x in ["org_name", "suppl_name"]
                            if x in cols_to_check][0]
            # Get names
            col = df[col_to_check]
            # Are names duplicated?
            temp = df.loc[:, cols_to_check]
            temp = temp.drop_duplicates()
            freq = temp[col_to_check]
            freq = freq[freq.notna()].value_counts()
            uniq = freq[(freq > 1).values].index.tolist()
            duplicated = col.isin(uniq)
            # Update result
            res = res | duplicated
        # Number found?
        if any(i in cols_to_check for i in ["org_code", "suppl_code"]):
            # Get column
            col_to_check = [x for x in ["org_code", "suppl_code"]
                            if x in cols_to_check][0]
            # Get numbers
            temp = df.loc[:, cols_to_check]
            temp = temp.drop_duplicates()
            freq = temp[col_to_check]
            freq = freq[freq.notna()].value_counts()
            uniq = freq[(freq > 1).values].index.tolist()
            duplicated = col.isin(uniq)
            # Update result
            res = res | duplicated
        if any(res):
            # Get only incorrect values
            df = df.loc[res, :]
            if log_file:
                msg = "The following organization data contains duplicated \
                    (e.g., equal business ID but different name) or empty \
                    values or business IDs are incorrect. Please check them \
                    for errors"
                file_name = "org.csv" if data_type == "org" else "suppl.csv"
                utils.__log_to_file(df.copy(), log_file, file_name, msg)
            else:
                warnings.warn(
                    message=f"The following organization data contains "
                    f"duplicated (e.g., equal business ID but different name) "
                    f"or empty values or business IDs are incorrect. "
                    f"Please check them for errors: \n{df}",
                    category=Warning
                    )
    return res


def __replace_old_values_with_new(
        df, old_values, new_values, cols_to_check, cols_to_match):
    """
    Replace values of df with new_values based on corresponding old_values
    Input: df, current values of it, and new values that replace old values
    Output: df with new values
    """
    # Which values were modified?
    # Get indices of those rows that are changed
    ind_mod = (old_values.fillna("") != new_values.fillna("")).sum(axis=1) > 0
    ind_mod = [i for i, x in enumerate(ind_mod) if x]
    # Loop over those rows and replace the values of original data columns
    for i in ind_mod:
        # Get old and new rows
        old_row = old_values.iloc[i, :].values.tolist()
        new_row = new_values.iloc[i, :].values.tolist()
        # Replace values with new ones
        df.loc[(df == old_row).sum(axis=1) == df.shape[1], :] = new_row
    return df


def __get_matches_from_db(
        df, df_db, cols_to_check, cols_to_match, pattern_th, scorer,
        disable_partial, log_file, data_type):
    """
    Is there some data missing or incorrect? Based on df_db, this function
    replaces values of df.
    Input: df, and data base
    Output: df with correct values
    """
    # Create a copy that will be modified
    df_mod = df.copy()
    # Initialize DF for warning messages
    missmatch_df = pd.DataFrame()
    not_detected_df = pd.DataFrame()
    part_match_df = pd.DataFrame()

    # Loop over rows
    for i in range(0, df.shape[0]):
        row = df.iloc[i, :]
        # Intialize a DF for variables' position in data base
        temp = pd.DataFrame()
        # Loop over variables
        for j, x in enumerate(cols_to_check):
            # Get name, number and id if they are found from the df,
            # otherwise get False
            var_df = row[df.columns == cols_to_check[j]]
            var_df = var_df.astype(str).str.lower().values
            # Can name, number and BID be found from the df_db?
            # Get True/False list
            var_db = df_db.loc[:, cols_to_match[j]].astype(
                str).str.lower().values
            var_db = var_db == var_df
            # Add to DF
            temp[x] = var_db
        # Loop over variables
        found = False
        missmatch = False
        for j, x in enumerate(cols_to_check):
            # If 1st, 2nd... or nth variable was found from database
            if any(temp[x]):
                row_db = df_db.loc[temp[x].tolist(), cols_to_match]
                # row_db = row_db.values.tolist()[0]
                found = True
                # If there were other variables,
                # check if they match with data base
                # values acquired by jth variable
                if temp.shape[1] > 1:
                    missmatch_df, missmatch = __check_if_missmatch_db(
                       temp=temp, row_db=row_db, j=j, df_db=df_db,
                       cols_to_check=cols_to_check,
                       cols_to_match=cols_to_match,
                       missmatch_df=missmatch_df)
            # If match was found, break for loop; do not check other variables
            if found:
                break
        # If false, try partial match if values include names
        if found is False and "name" in cols_to_match:
            # Get name from df and database
            name_df = row[df.columns == cols_to_check[
                cols_to_match.index("name")]].values[0]
            name_db = df_db.loc[:, "name"]
            # Try partial match, if not None
            if not pd.isna(name_df):
                res = process.extract(name_df, name_db, scorer=scorer)
                name_part = res[0]
                name_part2 = res[1]
                # If there are multiple values that include same partial string
                # e.g. karvia and merikarvia, they both have equal good match.
                # Try other partial match approach
                if name_part[1] == name_part2[1]:
                    res = process.extract(
                        name_df, name_db, scorer=fuzz.token_set_ratio)
                    name_part = res[0]
                    name_part2 = res[1]
            else:
                name_part = 0
                name_part2 = 0
            # If the matching score is over threshold
            if disable_partial is False and name_part[1] >= pattern_th and (
                    name_part[1] > name_part2[1]):
                # Get only the name
                name_part = name_part[0]
                # Find row based on name with partial match
                row_db = (df_db.loc[df_db.loc[:, "name"] == name_part,
                                    cols_to_match])
                # Add row to final data
                df_mod.iloc[i, :] = row_db.values.tolist()[0]
                # Store info for warning message
                temp = pd.DataFrame([name_df, name_part],
                                    index=[cols_to_check[
                                        cols_to_match.index("name")],
                                        "found match"])
                part_match_df = pd.concat([part_match_df, temp], axis=1)
                found = True
        # If match was found add row to final data
        if found and missmatch is False:
            # There might be multiple matches, get first one.
            row_db = row_db.iloc[[0], :] if row_db.shape[0] > 1 else row_db
            # Assign the row only
            df_mod.iloc[i, :] = row_db.iloc[0, :]
        else:
            # Store data for warning message: data was not found
            row = pd.DataFrame(row)
            not_detected_df = pd.concat([not_detected_df, row], axis=1)
    # If some data had missmatch
    if missmatch_df.shape[0] > 0:
        missmatch_df = missmatch_df.drop_duplicates()
        if log_file:
            msg = "The following data did not match. Please check it for \
                errors."
            file_name = data_type + ".csv"
            utils.__log_to_file(df.copy(), log_file, file_name, msg)
        else:
            warnings.warn(
                message=f"The following data "
                f"did not match. Please check it for errors: "
                f"\n{missmatch_df.transpose()}",
                category=Warning
                )
    # If some data was not detected
    if not_detected_df.shape[0] > 0:
        not_detected_df = not_detected_df.drop_duplicates()
        warnings.warn(
            message=f"The following data "
            f"was not detected. Please check it for errors: "
            f"\n{not_detected_df.transpose()}",
            category=Warning
            )
    # If partial match of name was used
    if part_match_df.shape[0] > 0:
        part_match_df = part_match_df.drop_duplicates()
        if log_file:
            msg = "The following organization names were detected based on \
                partial matching."
            file_name = data_type + ".csv"
            utils.__log_to_file(df.copy(), log_file, file_name, msg)
        else:
            warnings.warn(
                message=f"The following organization names were detected "
                f"based on partial matching:"
                f"\n{part_match_df.transpose().drop_duplicates()}",
                category=Warning
                )
    return df_mod


def __check_if_missmatch_db(temp, row_db, j, df_db,
                            cols_to_check, cols_to_match, missmatch_df):
    """
    This function checks if there are missmatch between row values of df
    and database.
    Input: df with indices that specify the row being checked currently,
    database row, j is the index of variable being checked,
    whole database, cols being checked, cols being matched, DF containing
    missmatches.
    Output: DF containing missmatches, and boolean value indicating if
    missmatch was found.
    """
    # Initialize result
    missmatch = False
    # Take other columns than j
    temp = temp.loc[:, [x for x in cols_to_check
                        if x not in cols_to_check[j]]]
    temp = temp.loc[:, temp.sum(axis=0) > 0]
    # If other variables had also matches
    if temp.shape[1] > 0:
        # Loop over variables
        for k, c in enumerate(temp.columns):
            # Get variable from database
            temp_db = df_db.loc[
                temp[c].values, [
                    x for x in cols_to_match
                    if x not in cols_to_match[j]]
                ].values.tolist()[0]
            # Get variable that was in values that will be
            # added to the final data if everything's OK
            value = [row_db.values.tolist()[0][num] for num, x in
                     enumerate(cols_to_match) if x not in
                     cols_to_match[j]]
            # Check if they not equal
            if value != temp_db:
                # Get values
                names1 = temp.columns.tolist()
                # Store data for warning message
                names2 = list("Found " + x for x in names1)
                names = [[names1[i], names2[i]] for i in range(0, len(names1))]
                names = names = sum(names, [])
                value.extend(temp_db)
                values = pd.DataFrame(value, index=names)
                missmatch_df = pd.concat([missmatch_df, values],
                                         axis=1, ignore_index=True)
                # Missmatch was found
                missmatch = True
    return [missmatch_df, missmatch]


def __check_variable_pair(df, cols_to_check, dtypes=None, **args):
    """
    This function checks variable pair that their data type is correct.
    Input: df, columns being checked, and expected data types
    Output: df
    """
    # Subset so that only available columns are checked
    ind = [i for i, x in enumerate(cols_to_check) if x in df.columns]
    cols_to_check = list(cols_to_check[i] for i in ind)
    # If dtypes is None, do not check them
    if dtypes is None:
        dtypes = df[cols_to_check].dtypes
    else:
        dtypes = list(dtypes[i] for i in ind)
    # Check if data types match
    ind = [i for i in ind if df[cols_to_check[i]].dtype != dtypes[i]]
    # If not, give warning
    if len(ind) > 0:
        # Subset to include only missmatches
        cols_to_check = list(cols_to_check[i] for i in ind)
        dtypes = list(dtypes[i] for i in ind)
        warnings.warn(
            message=f"The following data has incorrect data types."
            f"Data types of {cols_to_check} should be {dtypes}, respectively.",
            category=Warning
            )
    return df


def __check_vat_number(
        df, cols_to_check, log_file, disable_vat_number=False, **args):
    """
    This function checks that VAT numbers has correct patterns
    and match with business IDs.
    Input: df
    Output: df
    """
    # INPUT CHECK
    if not isinstance(disable_vat_number, bool):
        raise Exception(
            "'disable_vat_number' must be True or False."
            )
    # Check if column(s) is found as non-duplicated
    cols_to_check = utils.__not_duplicated_columns_found(df, cols_to_check)
    # All columns must be present
    if len(cols_to_check) != 3 or disable_vat_number:
        return df
    # INPUT CHECK END
    # Get vat number and bid column names
    # (do it this way, if orgaization gets also vat_number)
    vat_number_col = [x for x in cols_to_check if x in ["suppl_vat_number"]][0]
    bid_col = [x for x in cols_to_check if x in ["suppl_bid", "org_bid"]][0]
    country_col = [x for x in cols_to_check if x in ["suppl_land"]][0]

    # Drop NA
    df = df.loc[:, cols_to_check]
    df = df.dropna(subset=vat_number_col)

    # Test if valid VAT number
    res = -utils.__are_valid_vat_numbers(df[vat_number_col])

    # If BIDs are available
    if bid_col and country_col:
        # Get bids
        bids = df[bid_col]
        # Remove "-"
        bids = bids.astype(str).str.replace("-", "")

        # Get country codes from data base
        path = pkg_resources.resource_filename(
            "osta",
            "resources/" + "data_land.csv")
        codes = pd.read_csv(path, index_col=0, dtype=str)

        # Get unique countries
        uniq_countries = df[country_col].drop_duplicates()
        for country in uniq_countries:
            # Get the country from data base and get 2 character code
            temp = codes.loc[(codes == country).sum(axis=1) == 1, "code_2char"]
            temp = temp.values
            temp = temp[0] if len(temp) == 1 else ""
            # Add to data
            df.loc[df[country_col] == temp, "2_char_code"] = temp
        # Add country code to bid
        bids = df["2_char_code"] + bids
        # Check that it is same as VAT number
        not_vat = df[vat_number_col] != bids
        res = res | not_vat
    # If there were some VAT numbers that were incorrect, give a warning
    if any(res):
        df = df.loc[res, :]
        if log_file:
            msg = "The following VAT numbers were incorrect. They did not \
                match the correct pattern or match BIDs. Please check them \
                    for errors"
            utils.__log_to_file(df.copy(), log_file, "vat_number.csv", msg)
        else:
            warnings.warn(
                message=f"The following VAT numbers were incorrect. "
                f"They did not match the correct pattern or match BIDs. "
                f"Please check them for errors: {df}",
                category=Warning
                )
    return df


def __check_voucher(df, disable_voucher=False, **args):
    """
    This function checks if voucher column includes vouchers.
    Input: df
    Output: df
    """
    # INPUT CHECK
    if not isinstance(disable_voucher, bool):
        raise Exception(
            "'disable_voucher' must be True or False."
            )
    cols_to_check = ["doc_id"]
    cols_to_check = utils.__not_duplicated_columns_found(df, cols_to_check)
    # All columns must be present
    if disable_voucher or len(cols_to_check) == 0:
        return df
    col_to_check = cols_to_check[0]
    # INPUT CHECK END
    # CHeck with other columns
    res = utils.__test_if_voucher(
        df=df,
        col_i=df.columns.tolist().index(col_to_check),
        colnames=df.columns.tolist())
    # Get portion of unique values
    portion = len(df[col_to_check].drop_duplicates())/df.shape[0]
    # Voucher should match with other data or it should increase, or there
    # should be unique values in 25 % of rows.
    if not (res or df[col_to_check].is_monotonic_increasing or portion > 0.25):
        warnings.warn(
            message="It seems that 'voucher' column does not include " +
            "voucher values. Please check it for errors.",
            category=Warning
            )
    return df


def __check_empty_observations(df, log_file, thresh=0, **args):
    """
    This function checks if rows include empty values.
    Input: df
    Output: df
    """
    # INPUT CHECK
    if not (isinstance(thresh, int) and not isinstance(thresh, bool)):
        raise Exception(
            "'thresh' must be an integer."
            )
    # INPUT CHECK END
    # Remove columns that have less than thresh amount of non-empty values
    if thresh > 0:
        df = df.dropna(axis=0, thresh=thresh)
    # Calculate empty values per row
    empty_values = df.apply(lambda x: len(x)-x.count(), axis=1)
    if any(empty_values > 0):
        max_num = max(empty_values)
        if log_file:
            msg = f"It seems that the data includes rows with up to \
                {str(max_num)} empty values. Please check them for  errors."
            utils.__log_to_file(
                df.loc[empty_values > 0, :], log_file, "empty_rows.csv", msg)
        else:
            warnings.warn(
                message=f"It seems that the data includes rows with up to "
                f"{max_num} empty values. Please check them for errors. "
                f"Rows with empty values printed below.\n"
                f"{df.loc[empty_values>0,:]}",
                category=Warning
                )
    return df


# organize

def __subset_data(df, subset):
    """
    This function subset the data; takes only specific columns
    Input: df
    Output: df
    """
    if subset:
        # Load fields from file
        path = pkg_resources.resource_filename(
            "osta", "resources/" + "fields_export.csv")
        fields = pd.read_csv(path)
        fields = fields["key"]
        # Get those fields that are in DF
        fields = [x for x in fields if x in df.columns]
        # Subset the data
        df = df.loc[:, fields]
    return df


def __rename_columns(df, rename):
    """
    This function rename columns
    Input: df
    Output: df
    """
    if rename:
        # Load fields from file
        path = pkg_resources.resource_filename(
            "osta", "resources/" + "fields_export.csv")
        fields = pd.read_csv(path)
        # Create a dictionary from field data
        fields = fields.set_index("key")["value"].to_dict()
        # Rename columns
        df = df.rename(columns=fields)
    return df


def __modify_account(
        df, subset_account, add_account_group, language="fi", **args):
    """
    This function take only accounts 4300-4999.
    Input: df
    Output: df
    """
    # INPUT CHECK
    if not (language == "fi" or language == "en"):
        raise Exception(
            "'language' must be 'fi' or 'en'."
            )
    # INPUT CHECK END
    # Take only specific accounts
    if subset_account and "account_code" in df.columns:
        # Take index of rows that have account between 4300-4999
        ind = df["account_code"].astype(str).isin(
            [str(x) for x in range(4300, 5000)])
        # Subset the data
        df = df.loc[ind, :]
    # Add account group
    if subset_account and add_account_group and "account_code" in df.columns:
        # Initialize column
        column = "Kirjanpidon tiliryhmät" if language == "fi" else \
            "Account groups"
        df = df.reindex(columns=df.columns.tolist() + [column])
        # Get account codes
        accounts = pd.to_numeric(df["account_code"], errors="coerce")
        # Create account group 1
        ind = (accounts >= 4300) & (accounts <= 4499)
        value = "Palvelujen ostot" if language == "fi" else "Services"
        df.loc[ind, column] = value
        # Create account group 2
        ind = (accounts >= 4500) & (accounts <= 4699)
        value = "Aineet, tarvikkeet ja tavarat" if language == "fi" else \
            "Materials, supplies and goods"
        df.loc[ind, column] = value
        # Create account group 3
        ind = (accounts >= 4700) & (accounts <= 4799)
        value = "Avustukset" if language == "fi" else "Allowances"
        df.loc[ind, column] = value
        # Create account group 4
        ind = (accounts >= 4800) & (accounts <= 4999)
        value = "Muut toimintakulut" if language == "fi" else \
            "Other operating expenses"
        df.loc[ind, column] = value
    return df


def __convert_foreign_bid(
        df, drop_foreign_bid, foreign_bid="0000000-1", land_col=None, **args):
    """
    This function replace foreign bids.
    Input: df
    Output: df
    """
    # INPUT CHECK
    if not isinstance(foreign_bid, str):
        raise Exception(
            "'foreign_bid' must be a string."
            )
    if not (land_col is None or (
            isinstance(land_col, str) and land_col in df.columns)):
        raise Exception(
            "'land_col' must be None or string specifying a column."
            )
    # INPUT CHECK END
    # Get correct column
    if land_col is None:
        column = "suppl_land"
    else:
        column = land_col
    # If specified and column is found
    if (drop_foreign_bid and column in df.columns and
            "suppl_bid" in df.columns):
        # Load land codes from file
        path = pkg_resources.resource_filename(
            "osta", "resources/" + "data_land.csv")
        land = pd.read_csv(path, index_col=0, dtype="str")
        # Taken only those lands that are not Finnish
        land = land.loc[land["code_2char"] != "FI", :]
        # Get index of those values that are other that Finnish
        ind = land.apply(
            lambda x: df[column].astype(str).isin(x)).sum(axis=1) > 0
        # Replace those business IDs that are from foreign companies
        df.loc[ind, "suppl_bid"] = foreign_bid
    return df


def __drop_private_entrepreneur(
        df, drop_private, private_bid="0000000-0", language="fi",
        form_col=None, **args):
    """
    This function drops off sensitive data of private entrepreneurs.
    Input: df
    Output: df
    """
    # INPUT CHECK
    if not isinstance(private_bid, str):
        raise Exception(
            "'private_bid' must be a string."
            )
    if not (language == "fi" or language == "en"):
        raise Exception(
            "'language' must be 'fi' or 'en'."
            )
    if not (form_col is None or (
            isinstance(form_col, str) and form_col in df.columns)):
        raise Exception(
            "'form_col' must be None or string specifying a column."
            )
    # INPUT CHECK END
    private_name = "Yksityinen elinkeinonharjoittaja" if language == "fi" \
        else "Private person carrying on trade"
    # Check if correct column is available
    if form_col is None:
        column = ["suppl_yhtiömuoto", "suppl_company form",
                  "suppl_företagsform"]
    else:
        column = [form_col]
    column = [x for x in column if x in df.columns]
    # If there are column that tells the company form
    if drop_private and len(column) == 1:
        # List certain company type in different languages
        comp_type = [
            "yksityinen elinkeinonharjoittaja",
            "private person carrying on trade",
            "enskild näringsidkare"
            ]
        # Search those companies from the data
        ind = df[column[0]].astype(str).str.lower().isin(comp_type)
        # Change name if available
        if "suppl_name" in df.columns:
            df.loc[ind, "suppl_name"] = private_name
        # Change bid if available
        if "suppl_bid" in df.columns:
            df.loc[ind, "suppl_bid"] = private_bid
    return df
