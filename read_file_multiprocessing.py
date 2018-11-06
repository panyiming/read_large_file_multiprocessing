# read file using multiprocessing

import multiprocessing as mp
import os
import time

def process_wrapper(chunkStart, chunSize, file_path):
    with open(file_path, 'r') as f:
        f.seek(chunkStart)
        lines = f.read(chunSize).splitlines()
        for line in lines:
            process(line)

def process(line):
    parts = line.strip().split('\t')
    i = 0
    while i<100:
       i+=1
   # print '{} score is {}'.format(parts[0], parts[1])

def chunkfy(file_path, size=1024*1024):
    fileEnd = os.path.getsize(file_path)
    with open(file_path, 'r') as f:
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size, 1)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd > fileEnd:
                 break

def read_single_process(file_path):
    with open(file_path, 'rb') as f:
        for line in f:
            process(line)

def create_test_file(file_path, line_num=10000000):
    j = 0
    f = open(file_path, 'w')
    while j < line_num:
        line = str(j) + '\t' + str(100) + '\n'
        f.write(line)
        j += 1
    f.close()
    print 'finished creating test file'

if __name__ == '__main__':
    test_file = './test_file.txt'
    create_test_file(test_file)


    # init objects
    cores_num = 10
    pool = mp.Pool(cores_num)
    jobs = []
    # create jobs
    for chunkStart, chunkSize in chunkfy(test_file):
        jobs.append(pool.apply_async(process_wrapper, (chunkStart, chunkSize, test_file)))
    time1 = time.time()
    # wait for jobs to finish
    for job_i in jobs:
        job_i.get()

    # clean up
    pool.close()
    time2 = time.time()
    read_single_process(test_file)
    time3 = time.time()
    print 'multiprocess process time is {}'.format(time2-time1)
    print 'single process process time is {}'.format(time3-time2)
