from django.http import JsonResponse


########################################
# FRONTEND CHART FORMATTING            #
########################################
def return_json(queryset):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    labels = []
    data = []

    for field in queryset:
        labels.append(field.label)
        data.append(field.data)

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def return_json_options(queryset):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    pks = []
    names = []

    for field in queryset:
        pks.append(field.pk)
        names.append(field.name)

    return JsonResponse(data={
        'id': pks,
        'name': names,
    })


def return_queryset_lists(queryset):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    labels = []
    data = []
    for field in queryset:
        labels.append(field['label'])
        data.append(field['data'])
    return labels, data


def fill_month_zeros(labels, data, colname):
    import pandas as pd
    if len(data) == 0:
        df2 = pd.DataFrame(columns=['label', colname])
        df2['label'] = pd.to_datetime(df2['label'], format='%m/%Y')
        df2['label'] = df2['label'].dt.to_period('M')
        df2 = df2.set_index('label')
    else:
        # convert labels and data array into one dataframe
        # https://stackoverflow.com/questions/46379095/convert-two-numpy-array-to-dataframe
        df = pd.DataFrame({'label': labels, colname: data}, columns=['label', colname])
        # convert label to date type
        df['label'] = pd.to_datetime(df['label'], format='%m/%Y')
        # convert date column to monthly period type
        # https://stackoverflow.com/questions/45304531/extracting-the-first-day-of-month-of-a-datetime-type-column-in-pandas
        df['label'] = df['label'].dt.to_period('M')
        # set index column to label and sort by label
        df2 = df.set_index('label').sort_index()
        # create period_range that starts with earliest date and ends with latest date in input labels
        # and reindexes by the range
        # https://stackoverflow.com/questions/17343726/pandas-add-data-for-missing-months
        df2 = df2.reindex(pd.period_range(df2.index[0], df2.index[-1], freq='M'))
        # fill NaN with 0, ultimately filling missing months with 0 value
        df2 = df2.fillna(0.0)
    return df2


def return_zeros_lists(labels, data, colname="data"):
    df = fill_month_zeros(labels, data, colname)
    df['label'] = df.index
    labels = df["label"].astype(str).tolist()
    data = df[colname].tolist()
    return labels, data


def return_merged_zeros_lists(labels_array, data_array):
    import pandas as pd
    dfs = []
    if len(labels_array) != len(data_array):
        raise Exception("Length of labels array does not match data array")
    for i in range(len(data_array)):
        colname = "data_"+str(i)
        df = fill_month_zeros(labels_array[i], data_array[i], colname)
        dfs.append(df)
    # merge dfs into one df
    df_merge = pd.concat(dfs, axis=0)
    # fill any NaN with zero
    df_merge = df_merge.fillna(0.0)
    # sort merged dfs
    df_merge = df_merge.sort_index()
    # reindex and fill in any missing months
    df_merge = df_merge.reindex(pd.period_range(df_merge.index[0], df_merge.index[-1], freq='M'))
    # fill any NaN with zero
    df_merge = df_merge.fillna(0.0)
    # convert index to list
    # https://stackoverflow.com/questions/20461165/how-to-convert-index-of-a-pandas-dataframe-into-a-column
    df_merge['label'] = df_merge.index
    labels = df_merge["label"].astype(str).tolist()
    # convert all data columns to list and append them to array
    data_array = []
    data_cols = [col for col in df_merge if col.startswith('data')]
    for col in data_cols:
        data = df_merge[col].tolist()
        data_array.append(data)
    return labels, data_array
