# read_large_file_multiprocessing
this is a demo for reading large file using multiprocessing in python2. The following test result is
based on a easy file which has 10000000 lines and the test machine has 56 cores:

|processing number|cost time(s)|
|:--:|:--:|
|1|37.35|
|5|7.91|
|10|4.55|
|20|2.35|
