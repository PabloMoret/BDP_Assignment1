# Assignment 1  785257

## Design of a Big Data Platform

### Desing and Interaction between Components

Big Data Platforms have grown up very quickly these last years, as well as Data Science. In this assignment we will be designing and developing a small big data platform given a data set.

The data set is a group of elements with the same properties. In our case, we will be working with the New York City Taxi Data set. Due to implementing practicalities, the data set will be stored in a *.csv* file, but in real life it would be a real scenario of ingesting each taxi ride and stored and managed them in the data base. NYC Taxi Ride Data Set **Documentation** can be checked [here]https://data.cityofnewyork.us/Transportation/2018-Yellow-Taxi-Trip-Data/t29m-gskq. 

In order to design and build a big data platform some aspects need to be considder. The design is based on basic 3 components:

* Data Ingestion (*mysimbdp-dataingest*): the data ingestion part is where raw data is retrieved. In our case the data is set by tuples, *tuples* in other words. Each row is a tuple and each colum is a property of each element. Ideally, each driver would submit each trip he or she does, inserting all the required information:

	* ID of the vendor.
	* Date and time of the trip when engaged.
	* Date and time of the trip when disengaged.
	* Number of passengers.
	* Location when engaged.
	* Location when disengaged.
	* The rate of the trip, depending on the destination.
	* Trip stored in vehicle or not.
	* Payment type.
	* Fare amount.
	* Extra fees.
	* MTA tax.
	* Improvement surcharge.
	* Tip amount.
	* Tolls amount.
	* Total amount.

  Each driver would have a small computer in which they can insert the data and then sent them to the platform. This means that there are multiple tenants on the platform and it should managed together at the same time. It might be all at the same time, even though it is least probable. Mapping and transformation data is one of the possible preprocessing tasks doing before storing. There exist 112,234,626 tuples in less than one year (24/9/2018 to 5/5/2019) but is expected to grow, so a real scalability must be consider as one of the most important aspects. This means that $\frac{112,234,626}{223}$ = 593

  On the other hand, this component must be able to call all API functions, in order to insert, delete, query or modify data. These operations must be implemented in this module and of course need to satisfy all contracts of interfaces of the API. In general terms this is called Service Level Agreements: redundancy, security or performance. In our case each insertion to the data base depend on each computer on board, so redundance or performance in this point of view is not as importan as the Core part. Security is very important in some situations, but not a real threat in this scenario, since it is not really sensible information. Despite all before, it depends on TLC and TPEP/LPEP terms.

  

* APIs (*mysimbdp_daas*): this section of the design is based on the comunication between real and physical resources where the data is stored and the interaction of the tenants in the real world. 

* Core (*mysimbdp_coredms*):

![Big Data Platform Design Scheme](/assignment_data/images/BDP_A1_I1.svg)

