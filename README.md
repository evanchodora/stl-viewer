# viewer
### Python-based STL viewer

Opens any ASCII-type STL file for viewing with various perspective settings (isometric, dimetric, and trimetric) and different hidden line views (full wireframe, removed hidden lines, and greyed hidden lines). Additional toolbar commands can display the object in any of the 6 standard orthographic views.

Keyboard Bindings:

| Transformation| Keys          |
| ------------- |:-------------:|
| Rotate        | Arrow Keys    |
| Zoom          | J,            |
| Pan           | W, A, S, D    |


Freeze using PyInstaller:
```pyinstaller.exe --onefile --windowed --icon=cube.ico GUI.py```
