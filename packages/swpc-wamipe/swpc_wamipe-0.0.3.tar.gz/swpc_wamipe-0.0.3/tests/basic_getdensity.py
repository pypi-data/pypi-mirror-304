import time
from datetime import datetime
from src.wam_api import WAMInterpolator

def main():
    interpolator = WAMInterpolator()  # <-- as a class/object
    dt = datetime(2024, 5, 11, 18, 12, 22)
    lat, lon, alt = -33.4, -153.24, 550.68  # degrees north, degrees east, km

    # Clear the cache. Uncomment this to test cache retention
    interpolator.cache.clear_cache()

    # Measure Time, Calculate Density
    start_time = time.time()
    density = interpolator.get_density(dt, lat, lon, alt)
    end_time = time.time()
    print(f"Density: {density}, Runtime: {(end_time - start_time)}s")

if __name__ == '__main__':
    main()