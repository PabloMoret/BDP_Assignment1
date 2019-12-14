# This directory is about the code.
>Note: we must be able to compile and/or run the code. No BINARY files are within the code. External libraries should be automatically downloaded (e.g., via Maven, npm, pip, docker pull)

# Code README

## Installation: Setting up the environment

This implementation is based on Python. It uses the MongoDB platform. The first step is to install the requirements. Find the *requirements.txt* in the *code* folder and run the following command:

``
pip install requirements.txt
``

The installation depends on the version of Python installed on your system. In order to avoid problems, you can install for both: Python Version 2 and Python Version 3.

The next step is to use a MongoDB database. The easiest way is to install MongoDB Server. You can find it [here](https://www.mongodb.com/).
However, there is a Cloud Data Base in Google Cloud managed by MongoDB Atlass. It is a cluster managed by MongoDB allocated in the Google Cloud. If you want to use the Atlas Cluster you should make sure that your IP Address is in the whitelist. Otherwise you will not be able to do ingestions.

To run the program, go to the *code* folder and run a cmd on **Windows** or a terminal on *Linux*. Then run the following command:

``
python handler.py *arguments*
``

## Running the program

Depending on the Operating System the *python* command must or must not be included. Now let's explain all the flags the program need to execute:

``
handler.py [-h] (-r | -l LOCAL) [-p PARALLEL] [-t] -d DATABASE
``

* **-r | -l LOCAL** : the use of one of these flags is compulsory. -r flag lets you to do a request from *data.cityofnewyork.us*, where the raw original data is allocated. If -l is instead selected, it fetchs the data from a local *csv* file. You can find some samples in the *data* folder.

```
python handler.py -r
python handler.py -l "../data/local_data.csv"
```

Note that making a request takes much time. Avoid using -r and -p at the same time, or the ingestion will take a long long time.

* **-p PARALLEL** : this optional command simulates a concurrent ingestion. In the real scenario, it is supposed that multiple sources are ingesting at the same time. It needs an int argument from 2 to 127.

```
python handler.py -p 60
```

* **-t** : the *t* optional flag is used to measure the time while ingesting. If you run the program in concurrent mode, the timing takes into account all the desired concurrent ingestions.

```
python handler.py -t
```

* **-d DATABASE** : this compulsory flag is needed to select the target database. If *atlass* argument is typed, then the fetched data will be ingested in the Atlass Cluster, whereas *local* is typed, then the source data will be stored in the local Mongo server.

```
python handler.py -d atlass
python handler.py -d local
```

The program starts running *handler.py*. It is a manager that gets all arguments and run the ingestion with the desired options. Handler first initializes the BD Platform in *db_config.py*, then handler calls *mysimbdp_dataingest.py*, which calls *NYC_YTTD_ingestion.py* if needs a request or just reads a file with the source data. Finally *mysimbdp_daas.py* is called from the ingestion component to ingest the data using the custom API. 

## Performance test

There already exists a log file containing all the times took to ingest from 2 to 127 parallel sources. You can have a look [here](../logs/performance_log.txt).
This test has been made with from 2 concurrent ingestions to 127. It has been made with the *performance.sh* file located in the code folder. It just loop 125 times making ingestions to the Atlass database. The log file contains the time taken to ingest the data.