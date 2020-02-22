def add_date_parts(df):
    df = df.copy()
    attrs = ['Dayofweek', 'Day', 'Month', ]
    for attr in attrs:
        df[f'pickup_datetime{attr.lower()}'] = getattr(df.pickup_datetime.dt, attr.lower())
    return df
