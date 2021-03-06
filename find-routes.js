#!/usr/local/bin/node

// find routes that hit a given (hardcoded) stop
//
// Uses synchronous filesystem and csv-parse APIs, because it's the
// easiest way to do it. But this version is 5x slower than the Python
// version. Unclear why: maybe the use of synchronous I/O is to blame?
// No evidence for that, but I have a hard time believing that reading
// files in Python is 5x faster than in Node.
//
// (The CSV parser here is doing a bit more work, and making them
// equivalent yielded roughly 20% speedup -- nowhere close to 5x! So
// that's not the whole story.)

const fs = require('fs');
const csvparse = require('csv-parse/lib/sync');

function main() {
  let stop_ids = find_stop_ids("stops.txt", "Grand Central");
  let trip_ids = find_trip_ids("stop_times.txt", stop_ids);
  let route_ids = find_routes("trips.txt", trip_ids);
  for (let route_id of route_ids) {
    console.log(route_id);
  }
}

// find stops whose name starts with prefix; return set of stop IDs
// (string)
function find_stop_ids(filename, prefix) {
  let records = read_csv(filename);
  let results = new Set();
  for (let record of records) {
    if (record.stop_name.startsWith(prefix)) {
      results.add(record.stop_id);
    }
  }
  return results;
}

// find trips that hit a stop in stop_ids (a set); return set of trip
// IDs (string)
function find_trip_ids(filename, stop_ids) {
  let records = read_csv(filename);
  let results = new Set();
  for (let record of records) {
    if (stop_ids.has(record.stop_id)) {
      results.add(record.trip_id);
    }
  }
  return results;
}

// find routes that include a trip in trip_ids; return set of route
// IDs (string)
function find_routes(filename, trip_ids) {
  let records = read_csv(filename);
  let results = new Set();
  for (let record of records) {
    if (trip_ids.has(record.trip_id)) {
      results.add(record.route_id);
    }
  }
  return results;
}

// open filename, read it completely into memory, and return an array
// of records (one object per line, excluding the header line)
function read_csv(filename) {
  let data = fs.readFileSync(filename, {encoding: "utf8"});
  return csvparse(data, {columns: true});
}

main();
