# Assignment 1 - Big Data Platforms

The documentation of the code implementation can be found [here](codeReport.md).

## Index 

1. [Design of a Big Data Platform](#design-of-a-big-data-platform)<br/>
	11. [Desing and Interaction between Components](#desing-and-interaction-between-components)<br/>
	12. [Nodes to run the Platform](#nodes-to-run-the-platform)<br/>
	13. [Containers](#containers)<br/>
	14. [Scalability in Platform](#scalability-in-platform)<br/>
	15. [Industrial Cloud Development](#industrial-cloud-development)<br/>
2. [Development and deployment](#development-an-deployment)<br/>
	21. [Core Schema Structure](#core-schema-structure)<br/>
	22. [Data partition](#data-partition)<br/>
	23. [Data Ingest Component](#data-ingest-component)<br/>
	23. [Data Ingest Component](#data-ingest-component)<br/>
	24. [Performance in concurrent ingestion](#performance-in-concurrent-ingestion)<br/>
	25. [Improving performance](#improving-performance)<br/>
3. [Extension with discovery](#extension-with-discovery)<br/>


## Design of a Big Data Platform

### Desing and Interaction between Components

Big Data Platforms have grown up very quickly these last years, as well as Data Science. In this assignment we will be designing and developing a small big data platform given a data set.

The data set is a group of elements with the same properties. In our case, we will be working with the New York City Taxi Data set. Due to managing practicalities, the data will be retrieved from the dataset, instead of saving a very huge *.csv* file. In real life it would be a real scenario of ingesting each taxi ride and stored and managed them in the data base. NYC Taxi Ride Data Set **Documentation** can be checked [here](https://data.cityofnewyork.us/Transportation/2018-Yellow-Taxi-Trip-Data/t29m-gskq). 

In order to design and build a big data platform some aspects need to be considder. The design is based on basic 3 components:

* **Data Ingestion** (*mysimbdp-dataingest*): the data ingestion part is where raw data is retrieved. In our case the data is set by *tuples*. In other words, it is an ordered set of elements, in this case, attributes. Each row is a tuple and each colum is a property of each element. Ideally, each driver would submit each trip he or she does, inserting all the required information (note that most of the fields below would probably be filled in automatically):

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

		Each driver would have a small computer in which they can insert the data and then sent them to the platform. This means that there are multiple tenants on the platform and it should managed together at the same time. It might be all at the same time, even though it is least probable. Mapping and transformation data is one of the possible preprocessing tasks doing before storing. There exist 112,234,626 tuples in less than one year (24/9/2018 to 5/5/2019) but is expected to grow, so a real scalability must be consider as one of the most important aspects. This means that 112,234,626 / 223 = 593 insertions each day on average. 

		On the other hand, this component must be able to call all API functions, in order to insert, delete, query or modify data. These operations must be implemented in this module and of course need to satisfy all contracts of interfaces of the API. In general terms this is called Service Level Agreements (*SLA*): redundancy, security or performance. In our case each insertion to the data base depend on each computer on board, so redundance or performance in this point of view is not as importan as the Core part. Security is very important in some situations, but not a real threat in this scenario, since it is not really sensible information. Despite all before, it depends on TLC and TPEP/LPEP terms.

		Note also that despite in a real scenario all taxi drivers would be sumbitting their trips, here we are doing a simulation, so the insertions are randomized done .

* **APIs** (*mysimbdp_daas*): this section of the design is based on the comunication between real and physical resources where the data is stored and the interaction of the tenants in the real world. Each Big Data Platform provides its own APIs with its own functions. But in order to start doing the SLAs we first need to select one tecnology as the core of the platform. The *dataingest* component will provide the contracts, given in interfaces, in which a tenant can interact with the data base. Each one will have different privileges and/or obligations. 

* **Core** (*mysimbdp_coredms*): the core component is the most important aspect to take care of when designing the platform. It works as *PaaS* (*Platform as a Service*) and the technology used depends on the data and its environmental particular characteristics. In our case we are working with tuples which stores rides on NYC taxi rides. There are a few aspects to take into account in order to select the best technology:

	* Selecting Virtual Machines or Containers:
	    * Virtual Machines: this option provides a good performance. Each virtualized aspect (*computing resources, storage and network*) allows the platform to scale and adapt to the tenants needs as it grows as well as a solid privacy space, no files shared. 
	    * Containers: these works similar to a virtual machine but they are a bit more simple. Usually no private spaces so designer has to care about *sensible information*.
	    
	        In our case containers are the most suitable solution but we will discuss this topic later.

	* Design how our platform grows and evolves (scaling): this is an important aspect in the future. Maybe there is no need to grow platform now but could be in the future. This case is instanced in a *.csv* finished file ingestion workflow with no growing in the number of instances. If the real scenario is considered, each taxi driver could keep inserting more instanced per ride and the data set would increase. This way, the platform could increase the number of physical resources (*physical hardware*). Not only because of the storage capacity, but also because of performance on managing ingestions, storing and modifying processes.

	Using *Paas* such as Kubernetes in a Docker *PaaS* can easily manage resources and be able to extent computational power and storage capacity if the amount of taxi drivers increases.

	* What are the specific SLAs: Contracts are the base of the big data development. We supposed that are two kind of tenants: taxi drivers who submit or insert data in the data base, and managers, who treat the information. This means that first tenants have can only insert data and maybe do a query, while the last ones have the privileges to modify the data at any circumstance.

	* Availability of the platform: availability is one requirement of any platform, if it has bad availability, then no intrinsic requisite is satisfied and a bad job will be made. It is known as the probability a system will work during a certain period of time. Availability is not so so important for taxi drivers, since the software implemented to push the rides information can easily and automatically push it when the connection is established. However, this does not mean that it does not account. A minimum availability is required in order to work properly. 

	* Fault Tolerance: in this case, insertions can be performed in no real time and can be storaged locally, waiting to be sent. Then, in the taxi driver point of view fault tolerance is higher. On the other hand, if we have a look at the manager point of view, it needs a high level of availability, so at least 2 copies are needed, in case one fails. This is also because the data can not be lost. Data is very important for the customer and designers must do as much as they can to ensure the privacy, security and loss.

	* Performance: taxi drivers do not storage frecuently, and furthermore ingestions can be done with offset on the time, so does not really need to be extremly good. It can save some money investment. Managers also need a good performance, but no other data analysis must be performed (such data science) so, again, no extremly good performance needed.

	* Elasticity: the data base must be able to grow up as the amount of files increases. As the name of *big data platforms* stands for, the data base must manage big volume of information. The company might use more taxis than before, drivers might do more ingestions, and evenmore, the company could need more resources if they are recently affiliated with others or need them for other type of purposes.

![Big Data Platform Design Scheme](/reports/images/BDP_A1_I1.svg)

Explained all above, is the moment to choose a tecnology. In this case, MongoDB is a really good choice due to the following reasons:

* Each tuple could be stored in a file.
* Each ride the taxi driver submits it is already in *.json* file and MongoDB works fine with any formatted data.
* Something else.

### Nodes to run the Platform

Nodes are very important in terms of performance, availability and consistency. CAP Theorem states that only 2 of the 3 can be satisfied (Consistency, Availability and Tolerance to network partition). The platform could run just with 2 nodes. With this in mind:

* **Consistency** can be ensured by doing updates in a low frecuently time, for example at night. Insertions do not affect updates, since it is not modifying any tuple. Usually managers work from a single earth spot and on the mornings. Then, updates can be performed daily. 

* **Availability**: this aspect is not really important, since ingestions and storages can be performed not immediately. As mentioned above, the system must offer a minimum of availability, since the ingestions must be done at some time, they can not be waiting for ever. Furthermore, managers must be able to access de database and use the information, as it is meant to be.

	Multiple ways of accessing the platform is as important as having copies of the system. Networks can have failures and the data may be lost or neither reach the database. So, given this possible threat, the best option is to have other extra node with other ways of access. However, since this is the implementation of this development, this decision should be made by the client (the taxi driver company). The importance of the data depends on the tenant.

* **Tolerance to Network Partition**: in this case, if one node fails, there is always other still working to provide access to the managers, but, the reliability is very low. Even there is a copy of the whole data, if both nodes fail, then data can be lost. Due to this fact, 3 or 4 nodes would cut down the failure probability, and loosing the data would be very difficult. With 2 nodes, if one fails, tenants still have other backup one to keep working with the data. 

	In our case, one node will be the primary one, in which most of the insertions and managment will be performed. There is no need to have spreaded nodes, since it only works for New York City. The other node will be the backup one, in which updates will be done.

	Using virtualized containers with Docker/LXC and Kubernetesor other *PaaS* can make the backups and maintainence much easier. However, this implementation will take it into account, as the MongoDB can manage multiple databases, the only step is to deal with some different databases in different nodes. (It is assumed that the backup database is located in a different resource).

![Availability, consistency](/reports/images/BDP_A1_I3.svg)	

### Containers

Containers are one of the options to build the platform. In this case, a container will be a better option:

* Data Ingestion Component: using containers in data ingestion is very suitable, due to there are only to kind of tenants, there is no sense in building several virtual machines to implement the functions. Multiple taxi drivers can store information at the same time (there are no many insertions at the same time) and managers can delete, modify and do analysis very easily just with containers. They are also very lightweight, do not use too much resources and can be running tons of months with no crashes. Despite that, if the TLC has more than one subcompany, multi container is absolutely supported. All drivers will be ingesting the information, and depending on the volume of ingestion, several containers may be needed.

* API Container: as the previous component, the best option is to use containers. APIs should manage all ingestions. Again, containers offers a light and robust operability. The more ingests, the more containers or the more power processing container needed.

* Core component:  containers for core component is the most appropiate because our model is based on simple tuples where they are only stored and, in some cases managed for other purposes (*data sciece*). Data isolation is not really necessary: each tuple is not sensible to each other.

	
	Using virtual machines for the core component may be heavy and a waste of resources. 
	Containers are ligher than VM, allowing to compute faster. They just share kernel and libraries, but no resources splitting. Insertions are supposed to be performed spreadly, so no high performance is needed. We also have to take into account that several *ingestion* and *API* containers will perform simultaneously and the processing load will be spreaded aswell.
	The development is meant to be deployed in local server. Despite that fact, when everything works fine in local, we will set it on Docker or other platform in any Cloud Service.
	This is because tons of insertions can be done so multiple core containers and multiple api/ingestion containers will be needed to, as said above, spead the process/storage load.

See a concept of the containerization of the whole platform:

![Containerization of the BDP](/reports/images/BDP_A1_I4.svg)	

### Scalability in Platform

Many of the Big Data developers are concern about how the data grows right now. However, we should also think about how it will grow in the future, and since we do not know the details, we can make an approximated guess. As the data set grows in the number of rides, it is needed to be stored in a physical resource. But also the number of taxis can grow eassily in a short period of time due to a company affiliation, or even the data can be used to compute Machine Learning or General Data Science. Scalability may be a problem if not solved. There are a few things that constraint platform workflow:

* CPU Usage: insertions does not really grows, it just keeps the same (aproximated) value along the time. But if we have a look at possible data science or data management it can increase and be a bottleneck. Since we have opted for containers, if there is no more containers in hour single node, we will have to use other servers
* Lack of memory: it is the same as the CPU usage but in this case, memory can be added easily. Even though, big cloud companies usually try to recomend an other resources plan, and a cloning or adding a new machine need to be done.
* Disk Usage: Disk capacity addition can be performed but speed is a real problem: the only solution would be to migrate to another resource plan.

There exist other kinds of improvments apart from physical resources. Instances length or unnecesary properties can increase the number of tuples in the same disk, increase speed, performance and memory management.

Moreover, scaling in resources is quite easy and quickly using containers. Deploy virtualized containers can be performed in case there are more information that the selected resources can affoard.
MongoDB can manage tons of Megabyes of information in a single collection, so the problem kicks in when the container can not manage the amount of information. Usually, the smaller the container is, the easier scalable the platform is. Despite that, we can not work with a tiny containers, since the processing can get worse. We should look for a balance option. As already said before, the first step is to make the platform work in the local host, then in a real cloud.

Also there exists the software data flow, in which the data can be partitioned several times before it reaches the storage node. Given this fact, if the number of nodes can not manage the amount of data, there is always to have more in the future, maybe placed in certain locations in order to improve the latency, but also to speed up the whole process.

Kubernetes is a good tool if we want to manage all resources we have, saling them up, scaling them out, make some automations, and so on. 

In order to deal with hundreds or even thousands of sources generating and ingesting data, we can add more data brokers or to route them to balance the data load flow. Other alternative is to provide dedicated brokers on demand, depending on the service.

The last thing we can do is use microcomponents. This is very useful when the client has several processes or their data can be splitted, managed, routed and stored in a certain or specific way. Taxi drive ride data has just a few properties so it is not so useful.

The decisions taken in this example are:

* __3 Nodes__ in NYC due to latency: the main one to store the data, the backup one located far from the main one, and the last one, to retrieve the generated data while the main one is being repaired in order to avoid data loss.
* 460Bytes each document, since all tuples have the same format and similar content. 593 trips a day · 460Bytes = 247940Bytes a day. It is expected to grow linearly, since the amount of taxies and drivers may increase very very slow a day.

	460Bytes each trip · 112,234,626 trips ≅ 48GB.
	Even with tons of insertions, the average is quite low and MongoDB and any Cloud tool is way to powerful to withstand this insertion rate.

* Using __containers__ as the opted virtualized technology.
* Data is __not partitioned__ in principle, since there is no huge volume.
* We will keep some nodes in order to support an upcoming increase of volume of data. Also to still store more trips and even to do data analysis.
* There is __no data splitting__ during the begining of the deployment of the data base.
* __Two brokers__ are going to be deployed, more in the future if there is ingestion problem:
	* One broker for the main node.
	* Other broker for the temporal node.

* __No microservices__.

### Industrial Cloud Development

- industrial cloud infrastructure.
- UPLOADER (scheduler)

## Development and deployment

### Core Schema Structure

MongoDB is a really powerfull tool to develop a big data platforms. The raw data obtained from the sources are already in *.bson* files, so no other file transformation is needed.
In a real scenario, the data would be already parsed to *.bson* files in order to speed up the ingestion.

As already said above, each object contains a simple list of trip properties. Now, with this structure, the most accurate way to implement the core of the data base is with a simple container. Have in mind that there is just a 48GB of data in more than 7 months, so we can linearly use more containers as the data grows in size. Containers are meant to be used for different purposes, however, since we want a usefull, scalable and easy to use data platform, we will be splitting the data in different containers. One year of retrieved data is supposed to be less than 100GBs of disk memory, so we will have a single container for year. Despite this decision, if the number of trips increases for any reason, we are able to use more containers.

Google Cloud will be the most suitable techology, since it is a good platform for MongoDB using Kubernetes. There will be 3 nodes: the main one, the backup one and the temp one. All the data will be stored in the main node in one Mongo Collection. Collections can handle therabytes of information and almost never fail. However, it is implemented in a real and physical resource, thus we usually split the resources and the data to make it scalable and manageable.

Each object or also called *document* in Mongo has the following format:

```
{
	"vendorid":"2",
	"tpep_pickup_datetime":"2037-11-17T21:24:28.000",
	"tpep_dropoff_datetime":"2037-11-17T21:46:03.000",
	"passenger_count":"1",
	"trip_distance":"2.99",
	"ratecodeid":"1",
	"store_and_fwd_flag":"N",
	"pulocationid":"170",
	"dolocationid":"143",
	"payment_type":"1",
	"fare_amount":"15",
	"extra":"0.5",
	"mta_tax":"0.5",
	"tip_amount":"1.7",
	"tolls_amount":"0",
	"improvement_surcharge":"0.3",
	"total_amount":"18"
}
```
As it is shown above, each object has a bunch of properties, but they do not have an id to identify them. In principle, we will be use the MongoDB *_id* tag to identify them. Despite that, there will not be a planned data analysis so the managers can still use the basic query API or a custom one to access the data base.

### Data partition

The data partition model is very important in order to build a strong and flexible database. NYC Data Base is going to be build with 3 initial nodes. This is due to the client owner of NYC taxi trips data does not need access the data from different places, since the amount of it is quite low compared with other examples. Nonetheless there will be tons of data sources ingesting data, so the model will have several data brokers organizing and managing all the information to balance the load of the *core* and the backup server is meant to be far away to guarantee that, in case of a physical problem, one server is still available. The other two nodes whould help keeping the **ACID** properties:

* **Atomicy**: the platform should ensure that the data generated is saved in the core. The brokers should ensure this property, hence, if the main node is not working, brokers would send it to the temp node or keep the information in their memory, until the main server is available.
* **Consistency**: the platform should also ensure that the data ingested is the same as the source. This is very importante, since we can not work with corrupted data.
* **Isolation**: the system could be equiped with technology so that the ingestions can be done paralelized, regardless in reality they are serialized.
* **Durability**: data would be accessible for the managers even though occurs a fail. It is thanks to the backup node and the temp node. The first one does not receive requests from any source and it has less probability to fail or to stop withstanding.

The platform implementation maintains a balance between availability and consistency. Availability is provided by the two nodes. If a node is good enough, two nodes will supply with the required availability but also keep a good consistency.
For NYC trips, the most suitable time in a day to do backups is when less people are having rides. But we should also know that there exist rides in the middle of the night and brokers can hold until the main server is backed up. So, while the platform satisfies most of the ACID properties, we will still be looking for a more balance implementation using **BASE** properties.

Given the CAP solution, now we have to explain how the data is partitioned. Data accessing is not the priority in this implementation, since the biggest part of the operations are ingesting. All the data will be in the same main node. This lets the client cut down the cost of the deployment and it is more suited for its needs. Deploying 10 or 20 nodes will not improve the availability and consistency, because there is more spreaded data to be checked and backed up. The only reason to do this is to reduce the probability of loosing availability in case of failure.

### Data Ingest Component

In order to launch the Intestion Component, have a look at the [code *README* file](/codeReadme.md)

### Performance in concurrent ingestion

The code implements two methods of ingestion: one retrieving the data from the server (which takes a lot of time), and other one getting the data from a local file. Since the request method takes so many time we will measure the performance reading a local file.

The local file is a sample from the server data file, containing 100 elements. The test will be done calling the ingest component giving the number of concurrent ingestions we want. In order to know how to specify it, check the [code *README* file](/codeReadme.md).

```
handler.py -l "../data/local_data.csv" -p 8 -t -d atlass
```

The command above is calling the ingestion component 8 concurrent times. There is a limit of 128 just in case, however it cold be more than 128 taxis ingesting data at the same time, but we are testing in a closed environment.
Furthermore, a script file has been made in order to measure the time it takes to perform from 2 to 128 concurrent ingestions. You can find it [here](../code/performance.sh).

It is looping 125 times performing different concurrent ingestions to the Atlass Cluster. As it can be seen in the [performance_log](../logs/performance_log.txt) it takes little time to store data: just less than 10 seconds for 127 different sources with 100 trips each one ingesting at the same time.
Given this information we are completely sure that it could perfectly work in a real scenario.


### Improving performance

In principle there is no problem ingesting such this amount of data at the same time, even though it is being used a free and limited Atlass Cluster in terms of performance.

However, we know that the data might grow and we need to deploy a flexible data platform. The changes would be the following:

* Using more than one node: this would improve the way the data is store, since parallel nodes can be ingesting less data. But even the availability and the general throughput is better, there is a consistency problem. The more nodes we have (spreaded data), the less consistent our system is.
* Increasing the number of brokers: brokers are in the middle way between sources and the nodes. A few brokers may collapse if they have tons of sources ingesting. The more brokers the less load the infrastructure has.

## Extension with discovery

