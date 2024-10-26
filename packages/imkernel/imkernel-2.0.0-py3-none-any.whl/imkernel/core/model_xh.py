def add_value(df, index_name, column_name, value):
    """
    根据索引名称和列名，为多级索引的 DataFrame 添加值。

    参数:
    df: pandas DataFrame，具有多级索引
    index_name: 要匹配的索引名称（针对 level_4）
    column_name: 要修改的列名
    value: 要添加的值
    """
    # 找到符合 index_name 的行，并在指定列中添加值
    df.loc[pd.IndexSlice[:, :, :, index_name], column_name] = value
