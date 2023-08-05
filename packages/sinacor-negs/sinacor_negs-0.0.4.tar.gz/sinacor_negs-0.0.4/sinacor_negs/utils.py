def drop_left_zeros_df(df):
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.lstrip("0").str.strip()
    return df