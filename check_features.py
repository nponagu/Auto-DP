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
    1) :df: - pd.DataFrame with 
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