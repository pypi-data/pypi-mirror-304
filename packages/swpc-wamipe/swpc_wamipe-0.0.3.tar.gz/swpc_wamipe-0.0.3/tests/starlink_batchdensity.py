# CSV file retrieved from https://zenodo.org/records/7026474
import shutil

import pandas as pd
from datetime import datetime, timedelta
import time
from src.wam_api import WAMInterpolator

# Read the CSV file
df = pd.read_csv('launch_group4-7_3181.csv')

num_samples = 30

# Take only the first num_samples entries
timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S.%f') + timedelta(days=730) for ts in df['t_utc'][:num_samples]]
latitudes = df['latitude'].tolist()[:num_samples]
longitudes = df['longitude'].tolist()[:num_samples]
altitudes = df['altitude'].tolist()[:num_samples]

# Initialize WAMInterpolator
interpolator = WAMInterpolator()

# Benchmark 1: Batch Get

def benchmark_batch():
    interpolator.cache.clear_cache()
    start_time = time.time()
    densities = interpolator.get_density_batch(timestamps, latitudes, longitudes, altitudes)
    end_time = time.time()
    return densities, end_time - start_time

# Benchmark 2: Regular Get (Serial)
def benchmark_serial():
    interpolator.cache.clear_cache()
    start_time = time.time()
    densities = []
    for i in range(len(timestamps)):
        density = interpolator.get_density(timestamps[i], latitudes[i], longitudes[i], altitudes[i])
        densities.append(density)
    end_time = time.time()
    return densities, end_time - start_time

batch_densities, batch_time  = benchmark_batch()
serial_densities, serial_time = benchmark_serial()

print()
print("-" * 50)
print("BENCHMARKS")
print(f"Batch get time: {batch_time} seconds")
print(f"Regular (serial) get time: {serial_time} seconds")
print("-" * 50)