import pandas as pd

def check_category_var(df, valid_values):

    """
    Check conditions for a category feature.
    
    Input:
    1) :df: - pd.DataFrame with a category feature. Can be numeric or string. Should be with set index
    2) :valid_values: - expected values for a feature
    
    Used functions:
    1) :df.columns[0]: - get a name of feature
    2) :df.isna(): - make True or False for missing values
    3) :df.isin(): - check valid values
    
    Output:
    1) :df: - pd.DataFrame with error variables
    """
    
    #create error variables
    var_name = df.columns[0]
    var_name_missing = f"err_{var_name}_missing"
    var_name_values = f"err_{var_name}_values"
    
    #missing value
    df[var_name_missing] = df.isna()
    
    #wrong values, not expected
    df[var_name_values] = df[var_name].isin(valid_values)
    
    return df


def check_interval_var(df, min_val=None, max_val=None):
    
    """
    Check conditions for an interval feature.
    
    Input:
    1) :df: - pd.DataFrame with a category feature. Must be numeric. Should be with set index
    2) :valid_values: - expected values for a feature
    
    Used functions:
    1) :df.columns[0]: - get a name of feature
    2) :df.isna(): - make True or False for missing values
    3) :df.isin(range(min_val,max_val+1)): - check a range of values
    
    Output:
    1) :df: - pd.DataFrame with error variables
    """
    
    #create error variables
    var_name = df.columns[0]
    var_name_missing = f"err_{var_name}_missing"
    var_name_values = f"err_{var_name}_values"
    
    #missing value
    df[var_name_missing] = df.isna()
    
    #wrong values, not expected
    if min_val and max_val:
        df[var_name_values] = ~df[var_name].isin(range(min_val,max_val+1))
    elif min_val:
        df[var_name_values] = df[var_name] < min_val
    elif max_val:
        df[var_name_values] = df[var_name] > max_val

    return df


def check_spread_var(
    df, 
    filter_var = None,
    var_name = "spread",
    valid_values = list(),
    na_list = None
):
    
    """
    Check conditions for a spread feature.
    
    Input:
    1) :df: - pd.DataFrame with a spread feature. Can be numeric or string. Should be with set index
    2) :filter_var: - bool series for selecting a sample which should to answer
    3) :var_name: - a short unique name for a list of spread variables
    4) :valid_values: - expected values for a feature
    5) :na_list: - values for excluding another values ("don't know", "none of the above" etc.)
    
    Output:
    1) :df: - pd.DataFrame with error variables
    """

    
    #create list of spread variables
    if filter_var:
        var_list = list(df.columns.drop(filter_var))
    else:
        var_list = list(df.columns)

        
    #create error variables
    var_name_missing = f"err_{var_name}_missing"
    var_name_answered = f"err_{var_name}_answered"
    var_name_values = f"err_{var_name}_values"
    var_name_na = f"err_{var_name}_NA"
    var_name_duplicates = f"err_{var_name}_duplicates"

    
    #missing value
    df[var_name_missing] = df.loc[
        df.loc[:, filter_var] == True, var_list].isna().all(axis='columns')

    
    #a fake answer
    df[var_name_answered] = ~df.loc[
        df.loc[:, filter_var] != True, var_list].isna().all(axis='columns')

    
    #NA with another answer
    if na_list:
        battle_val_list = [val for val in valid_values if val not in na_list]
        df[var_name_na] = (
            df.loc[:, var_list].isin(na_list).any(axis='columns') & 
            df.loc[:, var_list].isin(battle_val_list).any(axis='columns')
        )
    
    
    #duplicates
    df[var_name_duplicates] = False
    for num in range(len(var_list) - 1):
        var = var_list[num]
        short_mult_list = var_list[num+1:]
        for val in valid_values:
            bool_array = (
                df.loc[:, [var]].isin([val]).any(axis='columns') & 
                df.loc[:, short_mult_list].isin([val]).any(axis='columns')
                )
            df[var_name_duplicates].loc[bool_array] = True

            
    return df


if __name__ == "__main__":
    
    # df = pd.read_excel("Межнац финал.xlsx", usecols=["NUMBER", "GORSELO"], index_col="NUMBER")
    # checked_df = check_category_var(df, [1,2])

    df = pd.read_excel("Межнац финал.xlsx", usecols=[
        "NUMBER", "V24", "V25.1", "V25.2", "V25.3", "V25.4", "V25.5", "V25.6", "V25.7", "V25.8"
        ], index_col="NUMBER")
    df["filt_V25"] = (df.loc[:, "V24"] == 1)
    df.drop(columns=["V24"], inplace=True)


    checked_df = check_spread_var(
        df,
        filter_var="filt_V25",
        var_name="V25",
        na_list=[99], 
        valid_values=[1,2,3,4,5,6,7,8,9,99]
        )
    print(checked_df.shape)