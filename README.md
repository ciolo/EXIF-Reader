# Exif Reader
## Overview
**Exchangeable image file format**, Exif, is a standard that specifies the formats for images, sound, and ancillary tags used by digital cameras (including smartphones), scanners and other systems handling image and sound files recorded by digital cameras. The specification uses the following existing file formats with the addition of specific metadata tags: JPEG for compressed image files, TIFF for uncompressed image files, and RIFF WAV for audio files.It is not used in JPEG 2000 or GIF.
The metadata tags defined in the Exif standard cover a broad spectrum:
 - Date and time information. Digital cameras will record the current date and time and save this in the metadata
 - Camera settings. This includes static information such as the camera model and make, and information that varies with each image such as orientation (rotation), aperture, shutter speed, focal length, metering mode, and ISO speed information
 - A thumbnail for previewing the picture on the camera's LCD screen, in file managers, or in photo manipulation software.
 - Each unpopulated location that becomes populated if it has exactly **three** populated neighbors
 - Copyright information

## Implementation
The Reader was implemented using Python and pattern MVC. Furthermore, PyQT was used to develop the GUI.

### The Model
The model has been implemented in the `MyModel` Class. This class contain the program state.
It provides methods to get, set, modify and evolve the program state.

### The GUI
The GUI is composed of a main window (`MainWindow` class) containing some stock widgets and some custom widget developed for this assignment.

## Functionalities
The program can be launched from the `main.py` script:
```
$ python3 main.py
```
### Main window
The Main window presents itself like this:
![init.png](/Images/init.png)

### Add Photo/Drag and Drop
The user can add a photo using the push buttons at the top or he can drag it into the window.
If the user drags more than one photo, the list below will be filled and the last photo will be uploaded.

When the user drags or adds one or more photos, the Main window will show up as follows
![after.png](/Images/after.png)

### Rotate
The user can also rotate the image 90 degrees to the left and 90 degrees to the right using the two buttons at the top.

### Empty List
With the button **Empty List** at the bottom the user can empty the list of images returning to the initial situation.

### Remove Item
Using the button **Remove Item** the user can remove a single photo from the list.

### Get Info
With the button **Get Info** the user can view, through a tab widget, the general information of the photo displayed in the main window, and can also access to exif data of the photo itself.
![exif.png](/Images/exif.png)

## Requirements
| Software           | Version        | Required |
| --------------     |:--------------:| --------:|
| **Python**         |     >= 3.5     |    Yes   |
| **PyQt5**          |     >= 5.1     |    Yes   |
| **hurry.filesize** |     v0.9       |    Yes   |
| QDarkStylesheet    |    >= 2.3.1    | Optional |

hurry.filesize a simple Python library that can take a number of bytes and returns a human-readable string with the size in it, in kilobytes (K), megabytes (M), etc.
