#!/usr/bin/python3

# find routes that hit a given stop ("Grand Central - 42 St")

import csv


def main():
    with open('stops.txt') as stops_fh:
        stop_ids = set(find_stop_ids(stops_fh, 'Grand Central - 42 St'))
    assert len(stop_ids) > 0, 'no stops found'
    print('stop_ids:', stop_ids)

    with open('stop_times.txt') as stoptimes_fh:
        trip_ids = set(find_trip_ids(stoptimes_fh, stop_ids))
    print('trip_ids:', len(trip_ids))

    with open('trips.txt') as trips_fh:
        for route_id in find_routes(trips_fh, trip_ids):
            print(route_id)


def find_stop_ids(stops_fh, want_name):
    reader = csv.reader(stops_fh)
    headers = next(reader)
    id_idx = headers.index('stop_id')
    name_idx = headers.index('stop_name')
    for line in reader:
        if line[name_idx] == want_name:
            yield line[id_idx]


def find_trip_ids(stoptimes_fh, stop_ids):
    reader = csv.reader(stoptimes_fh)
    headers = next(reader)
    id_idx = headers.index('stop_id')
    trip_id_idx = headers.index('trip_id')
    for line in reader:
        if line[id_idx] in stop_ids:
            yield line[trip_id_idx]


def find_routes(trips_fh, trip_ids):
    reader = csv.reader(trips_fh)
    headers = next(reader)
    trip_id_idx = headers.index('trip_id')
    route_id_idx = headers.index('route_id')
    seen = set()
    for line in reader:
        if line[trip_id_idx] in trip_ids:
            route_id = line[route_id_idx]
            if route_id not in seen:
                yield route_id
                seen.add(route_id)


main()
