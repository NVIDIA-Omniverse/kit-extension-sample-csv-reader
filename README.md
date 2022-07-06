# CSV Reader Extension Sample

## [CSV Reader (omni.csv.reader)](exts/omni.csv.reader)
![CSV Reader UI and Result](exts/omni.csv.reader/data/OV_CSVReader_WhatToExpect.png)


### About
This extension shows how to build a CSV reader extension. This sample extension presents how to read a csv file, to populate a 3D scene with objects at X,Y,Z coordinates given in the CSV file, as well as color(s). Generated Objects rely on the USD referencing schema process.


### [README](exts/omni.csv.reader)
See the [README for this extension](exts/omni.csv.reader) to learn more about it including how to use it.

### [Tutorial](tutorial/tutorial.md)
Follow a [step-by-step tutorial](tutorial/tutorial.md) that walks you through the creation of the Generate function (to open, read and populate the 3D scene)

## Adding This Extension

To add this extension to your Omniverse app:
1. Go into: Extension Manager -> Gear Icon -> Extension Search Path
2. Add this as a search path: `git://github.com/NVIDIA-Omniverse/kit-extension-sample-csv-reader?branch=main&dir=exts`


## Linking with an Omniverse app

For a better developer experience, it is recommended to create a folder link named `app` to the *Omniverse Kit* app installed from *Omniverse Launcher*. A convenience script to use is included.

Run:

```bash
> link_app.bat
```

There is also an analogous `link_app.sh` for Linux. If successful you should see `app` folder link in the root of this repo.

If multiple Omniverse apps is installed script will select recommended one. Or you can explicitly pass an app:

```bash
> link_app.bat --app code
```

You can also just pass a path to create link to:

```bash
> link_app.bat --path "C:/Users/bob/AppData/Local/ov/pkg/create-2022.1.3"
```

## Contributing
The source code for this repository is provided as-is and we are not accepting outside contributions.

