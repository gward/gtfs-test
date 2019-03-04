#!/usr/local/bin/node

// find routes that hit a given (hardcoded) stop

const fs = require('fs');
const csvparse = require('csv-parse/lib/sync');

function main() {
  let stop_ids = find_stop_ids("stops.txt", "Grand Central");
  console.log(`stop_ids = ${stop_ids} (${stop_ids.size}) = ${stop_ids.values()}`);
  let trip_ids = find_trip_ids("stop_times.txt", stop_ids);
  console.log(`trip_ids = ${trip_ids.size}`);
  let route_ids = find_routes("trips.txt", trip_ids);
  for (let route_id of route_ids) {
    console.log(route_id);
  }
}

function find_stop_ids(filename, prefix) {
  let data = fs.readFileSync(filename, {encoding: "utf8"});
  let records = csvparse(data, {columns: true});
  let results = new Set();
  for (let record of records) {
    if (record.stop_name.startsWith(prefix)) {
      results.add(record.stop_id);
    }
  }
  return results;
}

function find_trip_ids(filename, stop_ids) {
  let data = fs.readFileSync(filename, {encoding: "utf8"});
  let records = csvparse(data, {columns: true});
  let results = new Set();
  for (let record of records) {
    if (stop_ids.has(record.stop_id)) {
      //console.log(`stop_id ${record.stop_id} in stop_ids: saving trip_id ${record.trip_id}`);
      results.add(record.trip_id);
    }
  }
  return results;
}

function find_routes(filename, trip_ids) {
  let data = fs.readFileSync(filename, {encoding: "utf8"});
  let records = csvparse(data, {columns: true});
  let results = new Set();
  for (let record of records) {
    if (trip_ids.has(record.trip_id)) {
      results.add(record.route_id);
    }
  }
  return results;
}

main();
