# Assignment 1  785257

## Design of a Big Data Platform

### Desing and Interaction between Components

Big Data Platforms have grown up very quickly these last years, as well as Data Science. In this assignment we will be designing and developing a small big data platform given a data set.

The data set is a group of elements with the same properties. In our case, we will be working with the New York City Taxi Data set. Due to managing practicalities, the data will be retrieved from the dataset, instead of saving a very huge *.csv* file. In real life it would be a real scenario of ingesting each taxi ride and stored and managed them in the data base. NYC Taxi Ride Data Set **Documentation** can be checked [here](https://data.cityofnewyork.us/Transportation/2018-Yellow-Taxi-Trip-Data/t29m-gskq). 

In order to design and build a big data platform some aspects need to be considder. The design is based on basic 3 components:

* Data Ingestion (*mysimbdp-dataingest*): the data ingestion part is where raw data is retrieved. In our case the data is set by *tuples*. In other words, it is an ordered set of elements, in this case, attributes. Each row is a tuple and each colum is a property of each element. Ideally, each driver would submit each trip he or she does, inserting all the required information (note that most of the fields below would probably be filled in automatically):

 * ID of the vendor.
 * Date and time of the trip when engaged.
 * Date and time of the trip when disengaged.
 * Number of passengers.
 * Location when engaged.
 * Location when disengaged.p
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

 Each driver would have a small computer in which they can insert the data and then sent them to the platform. This means that there are multiple tenants on the platform and it should managed together at the same time. It might be all at the same time, even though it is least probable. Mapping and transformation data is one of the possible preprocessing tasks doing before storing. There exist 112,234,626 tuples in less than one year (24/9/2018 to 5/5/2019) but is expected to grow, so a real scalability must be consider as one of the most important aspects. This means that \\( {112,234,626 \over 223} = 593 \\) insertions each day on average. 

 On the other hand, this component must be able to call all API functions, in order to insert, delete, query or modify data. These operations must be implemented in this module and of course need to satisfy all contracts of interfaces of the API. In general terms this is called Service Level Agreements (*SLA*): redundancy, security or performance. In our case each insertion to the data base depend on each computer on board, so redundance or performance in this point of view is not as importan as the Core part. Security is very important in some situations, but not a real threat in this scenario, since it is not really sensible information. Despite all before, it depends on TLC and TPEP/LPEP terms.

 Note also that despite in a real scenario all taxi drivers would be sumbitting their trips, here we are doing a simulation, so the insertions are randomized done .

* APIs (*mysimbdp_daas*): this section of the design is based on the comunication between real and physical resources where the data is stored and the interaction of the tenants in the real world. Each Big Data Platform provides its own APIs with its own functions. But in order to start doing the SLAs we first need to select one tecnology as the core of the platform. The *dataingest* component will provide the contracts, given in interfaces, in which a tenant can interact with the data base. Each one will have different privileges and/or obligations. 

* Core (*mysimbdp_coredms*): the core component is the most important aspect to take care of when designing the platform. It works as PaaS (*Platform as a Service*) and the technology used depends on the data and its environmental particular characteristics. In our case we are working with tuples which stores rides on NYC taxi rides. There are a few aspects to take into account in order to select the best technology:

* Selecting Virtual Machines or Containers:
 * Virtual Machines: this option provides a good performance. Each virtualized aspect (*computing resources, storage and network*) allows the platform to scale and adapt to the tenants needs as it grows as well as a solid privacy space, no files shared. 
 * Containers: these works similar to a virtual machine but they are a bit more simple. Usually no private spaces so designer has to care about *sensible information*.
 In our case containers are the most suitable solution, due to there is no sensible information. physical resources splitting are not really necessary: choosing a virtual machine could be better option, since they can share resources and are more reliable, but it would be really expensive compared to the real needs. In this case, store is needed, and nothing else in a big scale. If data science, machine learning or data mining would be one of the estabilished contracts, a virtual machine platform would be more suitable: it offers more reliability and performance.
 Containers are ligher than VM, allowing to compute faster. They just share kernel and libraries, but no resources splitting. Insertions are supposed to be performed spreadly, so no high performance is needed.

* Design how our platform grows and evolves (scaling): this is an important aspect in the future. Maybe there is no need to grow platform now but could be in the future. This case is instanced in a *.csv* finished file ingestion workflow with no growing in the number of instances. If the real scenario is considered, each taxi driver could keep inserting more instanced per ride and the data set would increase. In this case, the platform could increase the number of physical resources (*physical hardware*). Not only because of the storage capacity, but because of performance on managing ingestions, storing and modifying processes.

* What are the specific SLAs: Contracts are the base of the big data development. In this case, we supposed that are two kind of tenants: taxi drivers who submit or insert data in the data base, and managers, who treat the information. This means that first tenants have can only insert data and the last ones have the privileges to modify the data at any circumstance.

* Availability of the platform: availability is one requirement of any platform, if it has bad availability, then no intrinsic requisite is satisfied and a bad job will be made.

 * Fault Tolerance: in this case, insertions can be performed in no real time and can be storaged locally, waiting to be sent. Then, in the taxi driver point of view fault tolerance is higher. On the other hand, if we have a look at the manager point of view, it needs a high level of availability, so at least 2 copies are needed, in case one fails.
 * Performance: taxi drivers do not storage frecuently, and furthermore storages can be done with offset on the time, so does not really need to be extremly good. It can save some money investment. Managers also need a good performance, but no other data analysis must be performed (such data science) so, again, no extremly good performance needed.
 * Elasticity: the data base must be able to grow up as the amount of files increases. As the name of *big data platforms* stands for, the data base must manage big volume of information.

![Big Data Platform Design Scheme](/assignment_data/images/BDP_A1_I1.svg)

Explained all above, is the moment to choose a tecnology. In this case, MongoDB is a really good choice due to the following reasons:

	* Each tuple could be stored in a file.
	* Each ride the taxi driver submits it is already in *.json* file and MongoDB works fine with any formatted data.
	* 

### Nodes to run the Platform

Nodes are very important in terms of performance, availability and consistency. CAP Theorem states that only 2 of the 3 can be satisfied (Consistency, Availability and Tolerance to network partition). The platform could run just with 2 nodes. With this in mind:

* Consistency can be ensured by doing updates in a low frecuently time, for example at night. Insertions do not affect updates, since it is not modifying any tuple. Usually managers work from a single earth spot and on the mornings. Then, updates can be performed daily. 

* Availability: this aspect is not really important, since ingestions and storages can be performed not immediately. 

* Tolerance to Network Partition: in this case, if one node fails, there is always other still working to provide access to the managers, but, the reliability is very low. Even there is a copy of the whole data, if both nodes fail, then data can be lost. Due to this fact, 3 or 4 nodes would cut down the failure probability, and loosing the data would be very difficult. With 2 nodes, if one fails, tenants still have other backup one to keep working with the data.

In our case, one node will be the primary one, in which most of the insertions and managment will be performed. There is no need to have spreaded nodes, since it only works for New York City. The other node will be the backup one, in which updates will be done.

![Availability, consistency](/assignment_data/images/BDP_A1_I2.svg)	

### Containers

Containers are one of the options to build the platform. In this case, a container will be a better option:

* Data Ingestion Component: using containers in data ingestion is very suitable, due to there are only to kind of tenants, there is no sense in building several virtual machines to implement the functions. Multiple taxi drivers can store information at the same time (there are no many insertions at the same time) and managers can delete, modify and do analysis very easily just with containers. They are also very lightweight. They do not use too much resources and can be running tons of months with no crashes.

* API Container: as the previous component, there is just a few reasons to use virtual machines in APIs: privacy and data isolation, resources splitting. Containers are very lightweight and APIs can easily run together for both tenants. There is also another possibility: using pairs of containers machines in order to implement the APIs: n machines with some containers on them, each pair of machine would be for taxi tenant and manager tenant (in a pair, one machine for taxi driver running several containers for insertion and deleting functions, in case a driver has misstyped information, and other machine for manager tenant running several containers for general managing functions).

* Core component:  containers for core component is the most appropiate because our model is based on simple tuples where they are only stored and, in some cases managed for other purposes (*data sciece*). Data isolation is not really necessary: each tuple is not sensible to each other.

### Scalability in Platform

As the data set grows in the number of rides, it is needed to be stored in a physical resource. Scalability may be a problem if not solved. There are a few things that constraint platform workflow:

* CPU Usage: insertions does not really grows, it just keeps the same (aproximated) value along the time. But if we have a look at possible data science or data management it can increase and be a bottleneck. Since we have opted for containers, hardware flexibility is not a possibility, so adding more servers is the only option.
* Lack of memory: it is the same as the CPU usage but in this case, memory can be added easily. Even though, big cloud companies usually try to recomend an other resources plan, and a cloning or adding a new machine need to be done.
* Disk Usage: Disk capacity addition can be performed but speed is a real problem: the only solution would be to migrate to another resource plan.

There exist other kinds of improvments apart from physical resources. Instances length or unnecesary properties can increase the number of tuples in the same disk, increase speed, performance and memory management.

### Industrial Cloud Development




## Development and deployment

### Core Schema Structure

MongoDB is a really powerfull tool to develop a big data platforms, but it constraints the 

### Data partition



