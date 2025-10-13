## Prusa Slicer x Kronos cross-GCode-generator

This repository contains a configuration for PrusaSlicer, including a postprocessor, to generate GCode that can be executed on the Kronos machines.

---

### Pre-requirements
Python Version >= 3 ([windows installer](https://www.python.org/downloads/windows/)) must be installed.  
If the profile repository should be cloned, git must be installed as well ([windows installer](https://git-scm.com/download/win)).

### How to start Slicer
Slicer can be started with a dedicated config directory. Just clone this repository and start Slicer from a terminal like this:
```
"C:\Program Files\Prusa3D\PrusaSlicer\prusa-slicer-console.exe" --datadir C:\repository\prusa-slicer-profile
```
Second option how the slicer can be started is via a windows shortcut. Create a new shortcut by right click -> new -> shortcut. Copy the command from above to the line and change
file locations accordingly.

![windows_shortcut](https://github.com/user-attachments/assets/9d8f6480-5836-455b-995e-64b7e42e5ef0)

Copy the command from above to the line and change file locations accordingly.

![windows_shortcut_ile_location](https://github.com/user-attachments/assets/71b9eb55-0e5c-426e-92a3-8bbccf14ca3b)

### Important settings (must be configured for every machine!)

- SHIFT_MOVING_FRAME

![SHIFT_MOVING_FRAME](https://github.com/user-attachments/assets/8e96b34a-2a53-44d4-afe5-4e31b58d2cdf)

- Z-offset

![z-offset](https://github.com/user-attachments/assets/0a763972-26ac-4b0a-87cb-f32f66c6d84b)

### Postprocessor
Brief: replace the path in ```Print settings -> Output options -> Post-processing scripts``` with the correct path for your installation like this: 
```
"C:\Users\<username>\AppData\Local\Programs\Python\Python310\python.exe" D:\path\to\git\repository\prusa-slicer-profile\postprocessor.py;
```

![postprocessor_path](https://github.com/user-attachments/assets/ae622882-4050-46d4-8a47-b00be93d17ba)

**Hint**: it is sometimes difficult to find the full python.exe path.
Run
```
python -c "import os, sys; print(os.path.dirname(sys.executable))"
```
in a CMD to find the installation path.

Some Kronos specific GCode statements are already included in the ```Printer Settings -> Custom G-code``` fields. 
An additional python postprocessor converts the resulting ```.gcode``` file, replacing some expressions with the B&R specific syntax. 
The postprocessor ```postprocessor.py``` must be listed in the Slicer configuration under ```Print settings -> Output options -> Post-processing scripts``` with the full absolute path.
We currently don't have a good way to synchronize the Slicer-profile without overwriting installation specific paths. 

The postprocessor does the following things:
* replace comments ```; -> ()```
* replace ```E -> QE=```
* suppress ```M106/M107 (fan control)``` commands
* convert temperature commands (```M104, M109, M140, M190```) into ```SET_TEMPERATURE[]```
* replace toolchange commands ```T0 -> TOOLID[1], T1 TOOLID[3]```

ToolID and BedID are currently configured as variables in ```postprocessor.py```
