import zlib
import bz2
import lzma
import os
import logging
import pygal
import time
import matplotlib.pyplot as plt

#Compression types from here: https://docs.python.org/3/library/archiving.html

logging.basicConfig(level=logging.INFO)


def measure_compress_time(file, compress_type='gzip'):
    start_time = time.time()
    compressed = None
    
    if compress_type == 'gzip':
        #you can give argument level to compress to choose between compress speeds
        compressed = zlib.compress(file.read())
    elif compress_type == 'bzip2':
        #ompresslevel, if given, must be an integer between 1 and 9. The default is 9.
        compressed = bz2.compress(file.read())
    elif compress_type == 'lzma':
        compressed = lzma.compress(file.read())
    elapsed_time = time.time() - start_time
    return elapsed_time, compressed

def compress(file_to_compress, compress_types):

    try:
        f = open(file_to_compress, 'rb')
        size_of_file = os.path.getsize(file_to_compress)
        logging.info("Before compression = {} bytes\n".format(size_of_file))
        elapsed_times = []
        for compress_type in compress_types:
            elapsed_time, compressed = measure_compress_time(f,compress_type)
            logging.info("COMPRESSING WITH {}:".format(compress_type.upper()))
            logging.info("After compression = {} bytes".format(len(compressed)))
            logging.info("Compression time = {} seconds\n".format(elapsed_time))
            elapsed_times.append(elapsed_time)
            f.seek(0) #return to start of file
        return elapsed_times
    except FileNotFoundError:
        return None



#file_to_compress = 'linia.jpg'

#elapsed_times = compress(file_to_compress, compress_types)
