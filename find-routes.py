#!/usr/bin/python3

# find routes that hit a given (hardcoded) stop

import csv


def main():
    with open('stops.txt') as stops_fh:
        stop_ids = set(find_stop_ids(stops_fh, 'Grand Central'))
    assert len(stop_ids) > 0, 'no stops found'

    with open('stop_times.txt') as stoptimes_fh:
        trip_ids = set(find_trip_ids(stoptimes_fh, stop_ids))

    with open('trips.txt') as trips_fh:
        for route_id in find_routes(trips_fh, trip_ids):
            print(route_id)


def find_stop_ids(stops_fh, name_prefix):
    """parse stops.txt, yield sequence of stop IDs based on want_name"""
    (reader, indexes) = open_csv(stops_fh, 'stop_id', 'stop_name')
    for line in reader:
        if line[indexes.stop_name].startswith(name_prefix):
            yield line[indexes.stop_id]


def find_trip_ids(stoptimes_fh, stop_ids):
    """parse stop_times.txt, yield sequence of trip IDs based on stop_ids"""
    (reader, indexes) = open_csv(stoptimes_fh, 'stop_id', 'trip_id')
    for line in reader:
        if line[indexes.stop_id] in stop_ids:
            yield line[indexes.trip_id]


def find_routes(trips_fh, trip_ids):
    """parse trips.txt, yield sequence of route IDs based on trip_ids"""
    (reader, indexes) = open_csv(trips_fh, 'trip_id', 'route_id')

    # keep track of unique route IDs in order to preserve order, and so the
    # caller can print route IDs as they arrive
    seen = set()
    for line in reader:
        if line[indexes.trip_id] in trip_ids:
            route_id = line[indexes.route_id]
            if route_id not in seen:
                yield route_id
                seen.add(route_id)


class Indexes:
    # dummy object that lets you set any attribute
    pass


def open_csv(fh, *want_columns):
    """wrap csv.reader around fh and look for wanted columns

    Return (reader, indexes) where indexes is an object with one attribute
    for every column in want_columns.

    Raise ValueError if the file is missing any of your wanted columns.
    """
    reader = csv.reader(fh)
    headers = next(reader)
    indexes = Indexes()
    for col in want_columns:
        setattr(indexes, col, headers.index(col))

    return (reader, indexes)


main()
