# Rate

Rate algorithm is a logical step-by-step method to solve the problem of estimating the value of use of a desktop and laptop computer equipment in next figure.

## Introduction & application 

Device owners nowadays decide if and when a digital device be comes ewaste, or is still usable for reuse but they do not have objective data to make this decision. This algorithm computes the value of use of the device. This algorithm together with the [RdevicePrice](https://github.com/eReuse/Rdeviceprice) allows to estimate a change price for devices. Entities and platforms applying Electronic Reuse Circular License use this algorithm to audit the application of the waste hierarchy. Prevention of waste generation can be avoided if we only recyle when the value of use is too low or has no demand, if it happens the owner or the community in custody obtains the recycling permission, or otherwise another cycle of reuse begins. This open source algoritm, as part of the eReuse.org platform (or used standalone), bring auditability on waste hierachy application, optimization and transparency in pricing. 

## Algorithm

### Input

The entry contains the main characteristics of a device that are: i) the components it has, such as processor, storage and ram memory, ii) the aesthetics or appearance, which is a categorical variable, now defined subjectively with values such as: “A: The device is new”, “B: really good condition (small visual damage in difficult places to spot)”, “C: good condition (small visual damage in parts that are easy to spot, not on screens)”, etc., (iii) and functionality, another categorical and subjective variable, such as: “A. Everything works perfectly (buttons, and in case screens there are no scratches)”, “B. There is a button difficult to press or a small scratch in an edge of a screen”, etc. At the same time, each component has a set of features such as processor speed, number of processor cores, processor score according to benchmarks, disk size and read/write speeds, or ram size and speed. 

The usage value of a product varies over time, for example, in year 2018 computers that do not have at least one dual core processor and 1 GB of RAM are not suitable for using an operating system and the most common applications. Therefore, the algorithm needs to access
up-to-date information with reference values for each component to estimate the current value for a device. This information is in the [Values of characteristics table.](https://github.com/eReuse/Rdevicescore/blob/master/data/models.csv)

This table is calculated periodically on the basis of data from devices in circulation managed by platforms and organisations reporting to the eReuse data pool. For each component, its normal distribution is calculated and the minimum acceptable values are set. The minimum acceptable value is represented by xMin, lower values add up to 0 in the component valuation, and the maximum value per xMax, higher values add up to the maximum allowed by the component.

The chosen percentile is recorded for each value, the main percentile is min, p5, p50, p75, p90, p95, max. For example, in the table the drive.size.xMax value has a value of 265,000 MB set for the percentile p90, this means that if we process a disk with this size, it will normalise to a value of 1, the same as if the disk has 500 GB. If the drive.size.xMin value is 4MB and the device is 4MB in size, that results in a value of 0.

### Process
**Step Filtering & Data Cleaning**

*Filtering*: Platforms manage diverse electronic devices such as televisions, printers, etc, the algorithm should filter the input only by accepting desktop and laptop type devices.
*Data cleaning*: The input with the description of the device components needs to be prepared for input to the algorithm. For example, if a device does not have disk the input is a null value that must be converted to 0.

**Step Component Parts Fusion**
There are components that are divided into what we call parts, such as RAM memory, which may have several memory cards or there may be several hard disks. The algorithm must merge them and treat them as a single component. In the case of size variables, we add the parts. For example, if we have two 100 GB disks, the result of the drive. size variable will be 200 GB. For example, if we have two RAM cards, one with 2GB and 100MB/speed, and the other with 4GB and 200MB/speed, the merger will result in a 6GB with 166MB/speed.

**Step Component Characteristic Normalisation**
At this stage, all parts of the components have been merged into one part with their corresponding characteristics. If for example we had 2 hard disks now we only have one disk with its variable size and speed. In this step we normalise between 0 and 1 the characteristics of the components. We use the "Values of Characteristics" table with
the values xMin and xMax and apply the standardisation formula, 
`y = (x −xMin)/(xMax −xMin)`

**Step Component Characteristic Score**
We have all the normalised characteristics of the components ranging from 0 to 1. In this step we give a score according to a distribution function as shown in next figure.

This distribution aims to give low scores to products that do not satisfy a minimum of usability features, as mentioned above. To use a common operating system and applications we need at least 1 GB of RAM and it would be desirable to have at least 2 GB. For the RAM,
the normalised 2GB value is 0.242, which corresponds to the p value of the function in which it begins to grow geometrically. From 4GB onward it would begin to grow logarithmically to give a lower score because in fact the usage value decreases. The key to adapting the algorithm is that the value p = 0.242 matches the minimum desirable
value of this characteristic.

**Step Component Characteristic Fusion**
In this step we merge the various characteristics of the components. Here we carry out the harmonic mean weighted by the weight of each characteristic (Harmonic Mean (weight)). The formula of the weighted harmonic mean is:

**Step Component fusion**
In this step we merge the various components into a single component. Again, we do the weighted harmonic mean. Established community weights are 50% for processor, 20% for disk and 30% for memory. The result is a unique score.

**Step Device Fusion**
We have achieved a score that groups all the components. Now we will merge the other scores we have, the aesthetic and functionality scores. Merger is just a sum. If aesthetics has an A rating (Is like new (without visual damage)) this represents 0.3 points of score, and if
functionality has an A rating (Everything works perfectly - buttons, and in case of screens there are no scratches) it would be 0.4 points.

Score final [−2,4.7] =Score aest [−1,0.3]+ Score funct [−1,0.4]

### Output
The result is a value ranging from -2 to 4.7. This value is interpreted as the usage value of a device. A value within [-2,2) is considered not valid. This device either does not have all the necessary components or these have insufficient performance to run an operating system and the most common applications. A device within [2.3) is considered low range, sufficient to be used but with limitations. A device within [3,4) is considered a midrange device that can be used for most applications and a device within [4,4.7] is a high-end device.

## Installation

## Licence

Copyright (c) Electronic Reuse Federation project under Pangea.org, released under the AGPL licence.
