# CSV Reader Extension

The CSV Reader extension offers the possibility to users to populate with some default shapes (Cubes or Spheres, for now) the scene, at locations X,Y,Z found in the CSV file.

prerequisites :
1) CSV Files place : either use the ones by default in the _data_ folder - or make sure to specify its place in the frame of the UI
2) Note that the CSV file should contain X, Y, Z and cluster columns. please look at examples provided in the _data_ folder

To use the extension:

process:

	[opt] : in the parameters frame, select the location of your CSV, the type of shape, if grouped by class...
	1) click on 'Generate' -> that should create elements here and there based on the info from the CSV file
		if required : you can export/save the USD stage with the 'file->Save As...' option.
		NB: that scene is reset everytime you press on Generate.

