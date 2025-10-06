## Prusa Slicer x Kronos cross-GCode-generator

This repository contains a configuration for PrusaSlicer, including a postprocessor, to generate GCode that can be executed on the Kronos machines.

---

### Pre-requirements
Python Version >= 3 ([windows installer](https://www.python.org/downloads/windows/)) must be installed.  
If the profile repository should be cloned, git must be installed as well ([windows installer](https://git-scm.com/download/win)).

### How to start Slicer
Slicer can be started with a dedicated config directory. Just clone this repository and start Slicer from a terminal like this:
```
"C:\Program Files\PrusaSlicer-2.9.3-beta3+win64-202112040927\prusa-slicer.exe" --datadir=D:\path\to\git\repository\prusa-slicer-profile
```

On Linux systems it should look like this:
```
PrusaSlicer-2.9.3+linux-x64-202101111322.AppImage --datadir=prusa-slicer-profile
```

### Important settings (must be configured for every machine!)

- SHIFT_MOVING_FRAME
- Z-offset 

### Postprocessor
Brief: replace the path in ```Print settings -> Output options -> Post-processing scripts``` with the correct path for your installation like this: 
```
"C:\Users\<username>\AppData\Local\Programs\Python\Python310\python.exe" D:\path\to\git\repository\prusa-slicer-profile\postprocessor.py;
```

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