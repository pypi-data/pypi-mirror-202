# DA4RDM_Vis_ProcessBased

## Description
The DA4RDM_Vis_ProcessBased is a python based package that can be used to evaluate fitness scores for the RDLC phases namely Planning, Production, Analysis, Archival, Access and Reuse for a reference projectid. The fitness scores are evaluated by generating a meaningful log based on the records associated with the reference projectid, converting them into a format accepted by the pm4py process mining algorithm and then evaluating alighment based fitness values by replaying the log on models defined for each RDLC phase separately. The package finally provides a radar vizualization of the evaluated fitness scores.


## Installation
The package is built using Python as a programming language and utilizes basic python packages. The package also uses the pm4py process mining package for fitness evaluations. Noteworthy, it uses few visualization packages like plotly express and kaleido to get the radar vizualization. Please make sure the necessary packages are installed before execution. Few other packages include scipy, json etc. The test package can be installed using the pip command provided below.

**pip install DA4RDM_Vis_ProcessBased**


## Importing the Module 
The package has one important module **Vizualize**. This modules invokes the necessary functions from other modules that perform the tasks of data extraction, model creation, fitness evaluation and plotting. The module can be imported using the below command:

```python
from DA4RDM_Vis_ProcessBased import Vizualize
```

## Usage
As mentioned earlier, the package can be used to extract fitness values and plot them for a reference ProjectId. The fitness value corresponding to the each RDLC phase is evaluated separately by replaying the log extracted for the reference projectid on the predefined model of the respective RDLC phase. The overall process thus evaluates 6 fitness score corresponsing to the previously mentioned RDLC phases. Finally, a radar vizualization of the same can be generated and the file is saved onto the local disk and the path of the radar vizualization image file is returned. To use the package for generating the radar vizualization, the function **process_vis** within the module **Vizualize** should be used. This method is the entry point and invokes the necessary functions that perform the evaluations and render the radar vizualization. The function body along with parameter information is as shown below:

```python
def process_vis(dataset_user_interactions, project_id, earliest_timestamp, last_timestamp):
 """
  :param dataset_user_interactions: filepath to the csv file, a string is expected
  :param project_id: the project for which fitness are to be evaluated
  :param earliest_timestamp: the earliest timestamp to consider for filtering records 
  :param last_timestamp: the earliest timestamp to consider for filtering records
 """
```

## Example
Example Usage:<br />
Below is an execution of the function with the parameters provided.
```python
from DA4RDM_Vis_ProcessBased import Visualize
path = Visualize.process_vis('17-02-2023.csv', "f5c043a1-82bc-4c61-bce6-0acbc0062948", '2023-02-14 08:57:44.315', '2021-05-03 02:31:54.652')
print(path)
```

## Output
All the above executions invokes the function **process_vis** with the passed parameter values. The fitness values are calculated and returned by the function. The radar vizualization is generated and saved onto the local repository of the program using the package. The function finally returns the path for the saved image file as shown below:

```python
.\Radarchart.png
```

