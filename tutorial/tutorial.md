![](https://github.com/NVIDIA-Omniverse/kit-extension-sample-csv-reader/raw/main/tutorial/images/logo.png)

# Create One CVS Reader with Omniverse Kit Extensions

**CSV** File, or **C**omma **S**eparated **V**alues, is the simplest form for storing data/information separated by commas, cf [CSV File](https://en.wikipedia.org/wiki/Comma-separated_values).
Those files are commonly used for exchanging data of various type and are broadly used. Examples : position of radio antennas and their types spread accross one town/region, 
position of hotels in Paris city and their grade, etc...In our case the CSV file contains X,Y,Z information about the position of
some elements to be placed in a 3D environment, as well a cluster column (representing some extra info), to be used as a color class grouping process.


## Learning Objectives
In this guide, we will learn how to:
* open a CSV file and read it
* place one shape at X,Y,Z position given by the CSV File
* shape displayed relying on the USD reference schema process - with position and color given by data retrieved from the CSV file

<p align="center">
    <img src="https://github.com/NVIDIA-Omniverse/kit-extension-sample-csv-reader/raw/main/tutorial/images/OV_CSVReader_WhatToExpect.png">
<p>




## Table of Content
0. [Prerequisites](#Part0)
1. [Download the Starter Project](#part1)
2. [Create one USD stage](#part2)
3. [Opening one CSV file](#part3)
4. [Displaying a shape at X,Y,Z + Colors](#part4)
5. [Grouping by class of Color/Cluster](#part5)
6. [Challenges](#part6)
7. [Discussion](#part7)

<a name="part0"></a>
## Prerequisites
* OV Code 2022.1 installed on one computer [GPU equiped and validated](https://docs.omniverse.nvidia.com/app_view/common/technical-requirements.html)
* some basics knowledge of python 
* Some knowledge of USD in particular the notion of reference API
    * [PIXAR USD Tutorial referencing](https://graphics.pixar.com/usd/release/tut_referencing_layers.html)
    * [NVIDIA Developer page](https://developer.nvidia.com/usd/tutorials)
    * [NVIDIA DLI Course](https://courses.nvidia.com/courses/course-v1:DLI+S-FX-02+V1/)
* [CSV file](https://en.wikipedia.org/wiki/Comma-separated_values) 

<a name="part1"></a>
## 1. Download the Starter Project
To get the assets for this hands-on lab, please clone the `tutorial-start` branch of `kit-extension-sample-csv-reader` [KitExtCSVReader](https://github.com/NVIDIA-Omniverse/kit-extension-sample-csv-reader). 

`git clone -b tutorial-start [https://github.com/NVIDIA-Omniverse/kit-extension-sample-csv-reader.git](https://github.com/NVIDIA-Omniverse/kit-extension-sample-csv-reader.git)' 

To load the extension, one possible way :
* in the extension tab, click on the _gear wheel_
* in the _extension search path_, add the path to the folder where you cloned the git repository
* afterwards, if you search for **CSV** in the extension tab, that one should then appear...

<p align="center">
    <img src="https://github.com/NVIDIA-Omniverse/kit-extension-sample-csv-reader/raw/main/tutorial/images/LoadExt.png">
<p>
    
To learn more about the other files in the repository, please check the [Build an Omniverse Extension in less than 10 Minutes](https://www.nvidia.com/en-us/on-demand/session/omniverse2020-om1483/), explaining how to create on extension and the files coming with it.


This tutorial will focus on the `models.py` file found in the `exts/omni.csv.reader/omni/csv/reader/`  directory, and in particular, on `Generate()`. Its workflow is defined as such:

```python
        def Generate(self):
                
                # Stage 2        
                # Clear the stage

                # create a new stage with Y up and in meters

                #  set the up axis

                #  set the unit of the world

                # define the root prim

                # Define the root prim as the default

                # add a light
        
                # Stage 3 (3.2)
                # check that CSV exists

                    # Read CSV file

                        #Iterate over each row in the CSV file
                        #   Skip the header row
                        #   Don't read more than the max number of elements
                        #   Create the shape with the appropriate color at each coordinate
                            
                            # Stage 4 (4.2)
                            #Read data from the next row
    
                            # root prim

                            # create the prim cluster path

                            # add group to path if the user has selected that option

                            #create the prim if it does not exist

                            #Create first reference prim

                            #Create instance to reference prim

                            #Get mesh from shape instance

                            #Set location
                            
                            # Stage 5 (5.2)
                            #Set Color
    
```           
> 📝 **Note:**  CSV Sample Files (2) to be read and default shapes to be used as references, are provided within the _data_ folder of this extension

<a name="part2"></a>
## 2. Create one USD stage
### 2.1 : Prior populating, setting that up - overall description
The first step we want to go with in our _Generate_ function is to create one stage, cleaning first what was created from previous run and setting some basic fundamentals, namely creating one _Root_ prim, adding a light (everyone likes having lights). 

Morevoer, working towards populating a 3D environment, we define (:
* the **UP** axis : 
```python
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
```
[Quoting:](https://graphics.pixar.com/usd/release/tut_xforms.html?highlight=xformop) _Computer graphics pipelines almost always pick an axis to represent the “up” direction. Common choices are +Y and +Z._
* the **UNIT** :
```python
    UsdGeom.SetStageMetersPerUnit(stage, self.stage_unit_per_meter)
```
Note that the *stage_unit_per_meter* is one member that is set once and for all in this current extension, but has been thought such that in the next version (your job :smile:) it could be, for example, modified in the UI.

The routine below present the different steps.

```python
        # Clear the stage
        stage = omni.usd.get_context().get_stage()
        primRoot = stage.GetPrimAtPath(self.rootUrl)
        if (primRoot.IsValid()):
            stage.RemovePrim(self.rootUrl)

        # create a new stage with Y up and in meters
        if omni.usd.get_context().new_stage() is False:
            carb.log_warn(f"failing creating a new stage")
            return None
                
        stage = omni.usd.get_context().get_stage()
        #  set the up axis
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
        #  set the unit of the world
        UsdGeom.SetStageMetersPerUnit(stage, self.stage_unit_per_meter)
        # define the root prim
        stage.DefinePrim(self.rootUrl)
        # Define the root prim as the default
        rootPrim = stage.GetPrimAtPath(self.rootUrl)
        stage.SetDefaultPrim(rootPrim)

        # add a light
        stage = omni.usd.get_context().get_stage()
        LightUrl = self.rootUrl + '/DistantLight'
        newLight = UsdLux.DistantLight.Define(stage, LightUrl)
        newLight.CreateAngleAttr(0.53)
        newLight.CreateColorAttr(Gf.Vec3f(1.0, 1.0, 0.745))
        newLight.CreateIntensityAttr(5000.0)
```  
### 2.2 : Practice
**TODO:** replace that code in the right section (only the big routine decribed above - the first 2 code lines, namely _SetStageUpAxis_ and _SetStageMetersPerUnit_ are only there for information, and already defined in the routine section), of the function _Generate_.

<a name="part3"></a>
## 3. Opening CSV file
### 3.1 : Format of one CSV File
CSV Files are common file format used by Data-scientists to store data, for various and heterogenous purposes.


<p align="center">
    <img src="https://github.com/NVIDIA-Omniverse/kit-extension-sample-csv-reader/raw/main/tutorial/images/CSV_Sample_both.png">
<p>

the structure of such a file is:
- the first line, or _header_, contains the names of the different fields.
- the following lines contain the values for each column, representing one 'element' per line.

To open and read one CSV file, we do rely on the Python’s inbuilt module called [**_csv_**](https://docs.python.org/3/library/csv.html) and in particular the _csv.reader_ object; this is combined with functions _open_ (to open the file), _cvs.reader_ to read the file with as argument _delimiter_ that specifies the character used to separate each field. 

### 3.2 : Practice
**TODO:** The routine in  `Generate()` is the one below. Now, knowing that our CSV file is made of:
- first line : the _header_, only fields name - not to be taken into account, starting then the loop from 1!
- 5 columns associated to the fields
- plenty of filled lines


```python
        if os.path.exists(self.CSVFilePath):
            # Read CSV file
            with open(self.CSVFilePath, newline='') as csvfile:
                csvReader = csv.reader(csvfile, delimiter=',')
                i = 1
                #Iterate over each row in the CSV file
                #   Skip the header row
                #   Don't read more than the max number of elements
                #   Create the shape with the appropriate color at each coordinate
                for row in itertools.islice(csvReader, TO_REPLACE, self.maxElements):
                    name = row[TO_REPLACE]
                    x = float(row[TO_REPLACE])
                    y = float(row[TO_REPLACE])
                    z = float(row[TO_REPLACE])
                    cluster = row[TO_REPLACE]
``` 

Please replace the **TO_REPLACE** with the proper values (the position in the CSV row) to match our expectation, taking into account our CSV format. When found, paste that one section after the creation of the stage.

Afterwards, please try running `Generate()` on pressing the button named similarly in the **UI**.

In case you would like to get confirmation it is working, and taking benefits of some _debug_ features of OV, you could add:

```python
                    carb.log_warn(f"X: {x} Y: {y} Z: {z}")
                    i += 1
``` 

and look at what is displayed on the console. Now remove those lines after validating reading was successfull - no need to keep that kind of debugging afterwards.

<details>
<summary>Solution</summary>
TO_REPLACE with...:

    for row in itertools.islice(csvReader, 1, self.maxElements):
                    name = row[0]
                    x = float(row[1])
                    y = float(row[2])
                    z = float(row[3])
                    cluster = row[4]

</details>   
 
<a name="part4"></a>
## 4. Displaying a shape at X, Y, Z + Colors
### 4.1 : Placing at X, Y and Z...
When working with USD scene composition, using _reference_ is one basic and usefull API. 

From the [USD Glossary](https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-References): 
>_"The primary use for References is to compose smaller units of scene description into larger *aggregates*, 
building up a namespace that includes the \"encapsulated\" result of composing the scene description targeted by a reference._"

The idea in our project is that instead of creating one prim per objects (which can be numerous, depending on the size of the CSV file), 
we do use the tool of using reference such that every displayed object is _based_ on the same shape. 
Benefits are several:
1. if the referred shape is changed, all elements would as well (sometimes we may prefer to have cubes, some other times sphere)
2. reducing the load of the scene - if saved, the output file (as _usd_ or _usda_) will be smaller

### 4.2 : Practice
Afterwards, in order to differentiate the objects, our algorithm place at different locations and change the color of the elements depending on their class (the column _cluster_ in our CSV file sample)

The steps are:
1. Create a place for the reference to live
2. Create the reference
3. create a new prim that refers to
4. optional: override/set color, position, scale, etc...


```python
                    # root prim
                    primClusterUrl = self.rootUrl

                    # add group to path if the user has selected that option
                    # FOR GROUPING PER COLOR
                    
                    primCluster = stage.GetPrimAtPath(primClusterUrl)

                    #create the prim if it does not exist
                    if not primCluster.IsValid():
                        UsdGeom.Xform.Define(stage, primClusterUrl)
                        
                    shapeUrl = primClusterUrl + '/box_%d' % i
                    i += 1

                    #Create first reference prim
                    refShape = stage.OverridePrim(shapeUrl)

                    #Create instance to reference prim
                    refShape.GetReferences().AddReference(str(self.ShapeFilePath), '/MyRef/RefMesh')
                                    
                    #Get mesh from shape instance
                    nextShape = UsdGeom.Mesh.Get(stage, shapeUrl)

                    #Set location
                    nextShape.AddTranslateOp().Set(
                        Gf.Vec3f(
                            TO_REPLACE, 
                            TO_REPLACE,
                            TO_REPLACE))

                    #Set Color
                    # FOR NEXT STEP COLOR
``` 

**TODO:** Copy the routine displayed above, and place it at the right location in `Generate()`. But do change the **TO_REPLACE** instances with the right values (they represent the position retrieved from the CSV file).

One add-on/idea: make use of the member _self.scaleDataConverter_ to display the objects at a more suitable position...
and why so? Any idea?
    
<details>
<summary>Solution (Basic)</summary>
In the code replace <code> #Set location</code>, with<br>

    #Set location
    nextShape.AddTranslateOp().Set(
              Gf.Vec3f(
                x, 
                y,
                z))   

</details>

**!!!Slightly Filled in the Room!!!** and quite drabbed color... :smile:

<p align="center">
    <img src="https://github.com/NVIDIA-Omniverse/kit-extension-sample-csv-reader/raw/main/tutorial/images/SlightlyFilledInTheRoom.png">
<p>
    
<details>
<summary>Solution ...with taking into account _unit/scale_</summary>
In the code replace <code> #Set location</code>, with<br>

    #Set location
    nextShape.AddTranslateOp().Set(
              Gf.Vec3f(
                self.scaleDataConverter*x, 
                self.scaleDataConverter*y,
                self.scaleDataConverter*z))   

</details>


### 4.3 :...and now changing the color
As you notice, we do use the function _AddTranslateOp().Set_ that we associate to the 
shape _nextShape_ currently being created.

But if we would like as well to change the color of this one?


### 4.4 : Practice

**TODO 1:** try adding _nextShape.GetDisplayColorAttr().Set([(1, 0, 0)])_ ...where? and what's the result?

Something like this?
<p align="center">
    <img src="https://github.com/NVIDIA-Omniverse/kit-extension-sample-csv-reader/raw/main/tutorial/images/AllRed.png">
<p>

**TODO 2:** change _[(1, 0, 0)]_ into _categoryColors[int(cluster) % self.maxNumberOfCluster]_
    
target of this line : changing the color accordingly to the _cluster_ value the object belongs to. 
    
<details>
<summary>Solution</summary>
In the code replace <code> # FOR NEXT STEP COLOR</code>, with<br>

    nextShape.GetDisplayColorAttr().Set(
             categoryColors[int(cluster) % self.maxNumberOfCluster])     

</details>

The origin of using _maxNumberOfCluster_ is that elements are grouped per class and we do want to limit the number of different colors so to have a better understanding of what is displayed (avoiding displaying one rainbow :rainbow: )
...but that is not necessary and would depend on the use case/target (and therefore a member parameter that can/could be changed.)

> 📝 [for more information about that _GetDisplayColorAttr_ function](https://graphics.pixar.com/usd/release/api/class_usd_geom_gprim.html)

<a name="part5"></a>
## 5. Grouping by class
### 5.1 : Why Grouping?
Why not? :wink:

In our current approach, based on our CSV sample, we thought about the fact that sometimes you may want to regroup the generated objects per class so as to more easily handle them afterwards.

let's imagine that the _cluster_ or _class_ topic refers to object of one certain type (_cluster_ 6 refers to _street lights_ and _cluster_ 29 to mail boxes...our CSV is about the positions of street's elements in one town, as an example). Then after displaying the shapes, someone would like to see only the mail boxes. Instead of selecting one by one in the stage scene, we can then select a _group_ and hide/show it easily thanks to the _eye icon_

<p align="center">
    <img src="https://github.com/NVIDIA-Omniverse/kit-extension-sample-csv-reader/raw/main/tutorial/images/TheMagicEye.png">
<p>

### 5.2 : Practice - How to do it.
Our class contains one member for that, namely _self.groupByCluster_. If you look at the **UI** of this extension, you can notice one checkbox to activate/deactivate such process of grouping. 

For what is behind the checkbox, you can have a look at the functions : 
* in _views.py_
```python
    ChoiceCheckBoxWithClass = ui.CheckBox(width=20) 
``` 
* and in _models.py_
```python
     def GroupByClusterChanged(self, _bool_checkboxVal_ClassGroup_):
``` 
Now to make it happen, just remember that USD is one extensible scene description, and as such, we can define some _structure_. 

Hence, in our case, we want, if activated, to group objects per class (the _cluster_ field of the CSV file).

**TODO:** with the 4 following hints, try to recreate the 2/3 lines of code that will make it happen.
the hints:
* _self.groupByCluster_ : is one _bool_ variable.
*  _primClusterUrl_ : is the _position_ where to add the generated _nextShape_
* when not grouped, _primClusterUrl = self.rootUrl_ is the _position_
* _self.clusterLayerRoot_ : is set as **_/Class__** (member of the class of our extension)
* from the CSV file, we do retrieve the current _cluster_ value

<details>
<summary>Solution</summary>
In the code replace <code># FOR GROUPING PER COLOR</code>, with<br>

    if self.groupByCluster:                    
           primClusterUrl += self.clusterLayerRoot + cluster

</details>

**EXPECTED RESULTS:**
<p align="center">
    <img src="https://github.com/NVIDIA-Omniverse/kit-extension-sample-csv-reader/raw/main/tutorial/images/WithGrouping.png">
<p>

<p align="center">
    <img src="https://github.com/NVIDIA-Omniverse/kit-extension-sample-csv-reader/raw/main/tutorial/images/OV_CSVReader_WhatToExpect.png">
<p>

<a name="part6"></a>
## 6. CHALLENGES
### 6.1 : bringing a third ref shape
If you look in the _data_ folder, we added a third one, namely _BasicQuadAsRef.usda_. The shape is not necessarily one good representative (flat surface), but depending on the target of why reading the CSV file, it can make sense.

Hence the challenge, if you accept, is:
- in _models.py_ : add one new shape in the list of potential shapes.
- in _views.py_ : change the _ComboBox_ and add the possibility to select that quad shape.

try it out by yourself.

### 6.2 : Changing the size of the shape
While so far we changed the position and the color of an object, we would like to alter as well the size/scale of it.

One Hint: if to change the position (_Add a Translate_) we use _nextShape.AddTranslateOp().Set_ , what do you think would be the solution to _Add a Rotation_?

> 📝 **Beware** of Transformations: USD uses the [UsdGeomXFormable](https://graphics.pixar.com/usd/release/api/class_usd_geom_xformable.html) schema. If you start looking deeper in it, you will notice that order of operations may differ from oneused _schemas_ to the other (example : SRT for Scale-Rotate-Translate...but can be different depending on...)


**MIXING a bit of Everything :**
<p align="center">
    <img src="https://github.com/NVIDIA-Omniverse/kit-extension-sample-csv-reader/raw/main/tutorial/images/OV_CSVReader_MixOfAllpng.png">
<p>

<a name="part7"></a>
## 7. Discussion
### CSV extensive format:
As presented, our CSV sample files contain 5 columns, including the _X_,_Y_,_Z_ and _cluster_ values...now CSV files may have
a bigger number of fields.

The challenge/question : how would you improve the current extension to handle any kind of CSV structures (we may imagine that
there are mandatory fields! - prerequisite of the extension V2.0)

### Scale and Units
As mentionned, CSV files are widely used to store any kind of data, of heteregenous nature.

Imagine you would like to display all the mail boxes and street lights of one town, the unit could be in meter. 

But then working on a CSV file displaying all the train stations located in Europe, you may tend to think that information would be given in km.

And then the challenge/question : how to display it in one 3D scene that would make sense? keep the unit of the stage as meters and deal with it, even though you may display elements thousands of units away?

#### Adding MetaData/Some text
how nice would it be to be able to display billboards, linked to objects, that would be shown when clicking on one of those latter !!!

## 7. Congratulations!!
Great job getting through this tutorial. Interested in improving your skills further? Interested in the presentating your version?

Challenge...Accepted...? :star:
