# IIB_GMV-Testat
An internal tool of the TU Darmstadt iib department to batch load and score student assessments.

# Description
Based on the QT framework, this tool was designed as a GUI application. 
In this way, non-technical staff can read in student submissions, 
enter scores in the input mask and automatically generate individual PDFs at the end, 
which can be handed out to the respective student.

# How to Install and Run the Project
## Install dependencies
You need an installed version of python (3.8 or newer).
Also, please install the following python modules via pip:
* pyqt5
* pandas
* numpy
* fpdf
* openpyxl
* lxml
* html5lib
* bs4

It may happen that the interpreter indicates the absence of other packages. Please install them as well.

## Create a standalone application
If you prefer using a single app, you have to use pyinstaller and a proper configured spec-file.

1.  Install pyInstaller: `pip install pyinstaller`
2.  Create a spec-file: `pyi-makespec --onefile gmvtestatview.py`
3.  Insert the following line of code to the top of the spec-file:
4.      added_files = [("imgs", "imgs"),("ui", "ui")]
5.  Change `datas=[]` to `datas=added_files,` in the spec-file
6.  Run `pyinstaller --onefile  gmvtestatview.spec`

Now, you can run and distribute the executable in the `dist` folder.
