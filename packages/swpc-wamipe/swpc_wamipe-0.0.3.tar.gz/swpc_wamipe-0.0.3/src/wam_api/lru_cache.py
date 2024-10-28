from collections import OrderedDict
import requests
import os
import json
import threading

class LRU_Cache():
    # Define Required Constants
    FILE_SIZE = 3  # size of each file in mb
    CACHE_PATH = 'wamapi_filecache'  # Move this to /tmp/wam_api/filecache, maybe?
    CACHE_METADATA = f'{CACHE_PATH}/metadata.json'

    def __init__(self, max_size=100, s3bucket='noaa-nws-wam-ipe-pds'):
        self.max_size = max_size  # allow the user to decide the max cache size, 100mb by default
        self.s3bucket = s3bucket
        self.download_set = set()  # maps file that is being downloaded to list of threads waiting on the download
        self.condition_dict = {} # stores thread conditions to act as event listeners
        self.cache_lock = threading.Lock()  # the lock object to be used across threads for the cache
        self.download_lock = threading.Lock() # the lock object to be used across threads for download set and condition dict

        if os.path.exists(self.CACHE_METADATA):
            with open(self.CACHE_METADATA, 'r') as metadata_file:
                self.file_map = json.load(metadata_file, object_pairs_hook=OrderedDict)
                self.current_size = len(self.file_map.keys())

        else:
            os.makedirs(self.CACHE_PATH, exist_ok=True)  # makes a directory if it doesn't already exist
            self.file_map = OrderedDict()   # maps file paths to their NetCDF dataset. ordered dict tracks the access order of the files 
            self.current_size = 0
    
    def get_file(self, file_path):
        if file_path not in self.file_map.keys():

            # file does not exist in cache. need to check if the file is already being downloaded.
            if file_path in self.download_set:  # file is being downloaded
                condition = self.condition_dict[file_path]
                with condition:
                    # print(f'Thread #{threading.get_ident()} waiting file {file_path} download')
                    condition.wait()
                # once the thread is done waiting on the download to be complete by another thread, we'll go down and return the local fileapth
            else:
                # add to download set
                # print(f'Thread #{threading.get_ident()} currently downloading {file_path}')
                self.download_set.add(file_path)
                self.condition_dict[file_path] = threading.Condition()

                # allow multiple threads to make http requests in parallel, but synchronize changes to the cache
                if self.put_file(file_path) is True:
                    self.mark_recently_used(file_path)
                    condition = self.condition_dict[file_path]

                    # notify threads here that download is complete and remove from download set and condition_dict
                    with condition:
                        condition.notify_all()

                    with self.download_lock:
                        self.download_set.remove(file_path)
                        self.condition_dict.pop(file_path)

                else:
                    # synchronize this
                    self.update_metadata()
                    return None
        else:
            self.mark_recently_used(file_path)

        # synchronize this
        self.update_metadata()
        return self.file_map[file_path]
    
    def put_file(self, file_path):  # downloads the NetCDF file from the s3 bucket, inserting the data into the file_map
        if self.current_size + self.FILE_SIZE > self.max_size:
            # synch this
            with self.cache_lock:
                self.remove_lru_file()

        # multtiple threads will be making requests (downloads) in parallel
        url = f"https://{self.s3bucket}.s3.amazonaws.com/{file_path}"
        response = requests.get(url)

        if response.status_code == 200:
            # create a valid output file path based on the input file path given
            output_path = os.path.join(self.CACHE_PATH, f'{file_path.replace(".", "_").replace("/", "_")}.nc')
            
            with open(output_path, 'wb') as file:  # saves the file into the designated local directory
                file.write(response.content)
            
            # synch these two lines below
            with self.cache_lock:
                self.file_map[file_path] = output_path
                self.current_size += self.FILE_SIZE  # update cache size
            
            return True
        else:
            return False

    def mark_recently_used(self, file_path):
        with self.cache_lock:
            self.file_map.move_to_end(file_path)

    def remove_lru_file(self):
        # remove the least recently used file from the local directory
        _, output_lru = self.file_map.popitem(last=False) # removes the least recently used file from the cache
        if os.path.exists(output_lru):
            os.remove(output_lru) # removes least recently used file from local directory

        self.current_size -= self.FILE_SIZE

    def print_cache(self):
        print(f'maxsize = {self.max_size}, currentsize = {self.current_size}')
        print(f'cache contains [{len(self.file_map.keys())}] total entries')
        for key, value in self.file_map.items():
            print(f'\t- file with path {key}')

    def update_metadata(self):    # call this function upon exiting the program 
        with self.cache_lock:
            with open(self.CACHE_METADATA, 'w') as metadata_file:
                json.dump(self.file_map, metadata_file, indent=4)

    def clear_cache(self):
        # Remove all files from the cache directory
        for file_path in self.file_map.values():
            if os.path.exists(file_path):
                os.remove(file_path)

        # Clear the file map and reset current size
        self.file_map.clear()
        self.current_size = 0

        # Update the metadata file
        self.update_metadata()
        print('Cache cleared successfully')