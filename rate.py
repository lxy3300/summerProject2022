import geopandas as gpd
import datetime


def read_file(path):
    data = gpd.read_file(path)
    return data


def save_file(data, path):
    data.to_file(path)


def rate_month(dataframe, months):
    dataframe['MRATE'] = round(dataframe['ACNUMBER']/months, 2)
    return dataframe


def calculate_days():
    d1 = datetime.datetime(2018, 1, 1)
    d2 = datetime.datetime(2022, 5, 1)
    intervals = d2 - d1
    return intervals.days


def rate_day(dataframe, days):
    dataframe['DRATE'] = round(dataframe['ACNUMBER']/days, 2)
    return dataframe


def rate_hour(dataframe, hours):
    dataframe['HRATE'] = round(dataframe['ACNUMBER']/hours, 4)
    return dataframe


if __name__ == "__main__":
    path_to_center = 'data/halifax_center/halifax_center.shp'
    center = read_file(path_to_center)
    # calculate month rate
    center = rate_month(center, 52)
    # calculate day rate
    days = calculate_days()
    center = rate_day(center, days)
    # calculate hour rate
    hours = days * 24
    center = rate_hour(center, hours)
    # save the file
    save_file(center, path_to_center)
