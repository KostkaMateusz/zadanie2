# python3 find-available-slot.py --calendars /in --duration-in-minutes 30 --minumum-people 2

# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("--calendars")
# parser.add_argument("--duration")
# parser.add_argument("--minumum")
# args = parser.parse_args()

# path = args.calendars
# duration=args.duration
# minimum=args.minumum
import os
from datetime import datetime
import itertools


path = "calendars"
duration = 15
minimum = 2
now = datetime.strptime("2022-07-02 16:00:00", "%Y-%m-%d %H:%M:%S")


def read_calendars_from_path(path: str) -> list[list[datetime]]:
    """Take path to folder with calendars and create datetime rerpesentation"""
    calendars_list = os.listdir(path)
    periods_list = []
    for filename in calendars_list:
        period = []
        with open(f"{path}/{filename}", "r") as f:
            list_of_lines = f.readlines()
            for line in list_of_lines:
                line = line.strip("\n")
                # split entry to start and end by " - " sign
                item_list = line.split(" - ")
                # if entry is of lenght 1 there is no free time
                if len(item_list) != 1:
                    # first in itemlist is start time
                    termin = datetime.strptime(item_list[0], "%Y-%m-%d %H:%M:%S")
                    period.append(termin)
                    # second in itemlist is end time
                    termin = datetime.strptime(item_list[1], "%Y-%m-%d %H:%M:%S")
                    period.append(termin)
        periods_list.append(period)
    return periods_list


def generate_free_time_periods(periods) -> tuple[list[datetime]]:
    """Based of datetime list with busy date create free periods for each person"""
    date_list = []
    start_list = []
    end_list = []
    for period in periods:
        # group list by date in dictionary
        dictionary = {per.date(): [date for date in period if per.date() == date.date()] for per in period}
        for key, value in dictionary.items():
            # for each list in dictioanry add start and end date
            value.append(datetime.strptime(f"{key} 23:59:59", "%Y-%m-%d %H:%M:%S"))
            value.insert(0, datetime.strptime(f"{key} 00:00:00", "%Y-%m-%d %H:%M:%S"))
            # every second item is a start of free period
            start_list.append(value[::2])
            # every first item is a finish of free period
            end_list.append(value[1::2])
        date_list.append(dictionary)
    # flatline list of lists
    start_list = list(itertools.chain(*start_list))
    end_list = list(itertools.chain(*end_list))
    return start_list, end_list


def filter_periods_by_duration(start, end, duration):

    filtered_start = []
    filtered_end = []

    for start_item, end_item in zip(start, end):
        diference = end_item - start_item
        if diference.total_seconds() / 60 >= duration:
            filtered_start.append(start_item)
            filtered_end.append(end_item)
    return filtered_start, filtered_end


def trim_periods_before_now(start, end, now):

    filtered_start = []
    filtered_end = []

    for start_item, end_item in zip(start, end):
        if now < end_item:
            filtered_start.append(start_item)
            filtered_end.append(end_item)

    return filtered_start, filtered_end


def find_max_attendants(start_periods, end_periods):

    # Sort arrival and exit arrays
    start_periods.sort()
    end_periods.sort()
    n = len(start_periods)
    # attendants_avaliable indicates number of attendants at a time
    attendants_avaliable = 1
    max_attendants = 1
    time = start_periods[0]
    i = 1
    j = 0

    # process all events in sorted order
    while i < n and j < n:
        # If next event in sorted order is
        # avalaible, increment count of attendants
        if start_periods[i] <= end_periods[j]:
            attendants_avaliable = attendants_avaliable + 1

            # Update max_attendants if needed
            if attendants_avaliable > max_attendants:
                max_attendants = attendants_avaliable
                time = start_periods[i]
            # increment index of arrival array
            i = i + 1
        else:
            attendants_avaliable = attendants_avaliable - 1
            j = j + 1

    print(time)
    print(max_attendants)


if __name__ == "__main__":
    periods = read_calendars_from_path(path)

    start, end = generate_free_time_periods(periods)

    filtered_start, filtered_end = filter_periods_by_duration(start, end, duration)

    filtered_start, filtered_end = trim_periods_before_now(filtered_start, filtered_end, now)

    find_max_attendants(filtered_start, filtered_end)
