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
    1) :df: - pd.DataFrame with 
    """
    
    #create error variables
    var_name = df.columns[0]
    var_name_missing = f"err_{var_name}_missing"
    var_name_values = f"err_{var_name}_values"
    
    df[var_name_missing] = df.isna()
    
    if min_val and max_val:
        df[var_name_values] = ~df[var_name].isin(range(min_val,max_val+1))
    elif min_val:
        df[var_name_values] = df[var_name] < min_val
    elif max_val:
        df[var_name_values] = df[var_name] > max_val

    return df


if __name__ == "__main__":
    
    df = pd.read_excel("Межнац финал.xlsx", usecols=["NUMBER", "GORSELO"], index_col="NUMBER")
    checked_df = check_category_var(df, [1,2])
    print(checked_df.columns)