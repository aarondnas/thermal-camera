# Gesundheitstechnik Gruppenprojekt

In diesem Projekt wird ein Prototyp für einen Thermographen (Wärmebildkamera) entwickelt.

## Inhaltsverzeichnis
1. [Beschreibung](#beschreibung)
2. [Anforderungen an die Entwicklungsumgebung](#anforderungen-an-die-entwicklungsumgebung)
3. [Verwendete Libraries](#verwendete-libraries)
4. [Setup und Installation](#setup-und-installation)
    - [Software](#software)
        - [Installation Raspberry Pi OS](#installation-raspberrypi-os)
        - [Terminal Installationen](#terminal-installationen)
        - [Implementierung von Code aus Repository](#)
    - [Hardware](#hardware)
        - [CAD - Setup und Installation](#cad)
    - [Elektronik](#elektronik)
        - [Bauteile](#bauteile)
5. [Support](#support)


## Beschreibung
Teil des Projekts ist die Entwicklung der Software, der Elektrotechnik und der Konstruktion.

Wichtigste Funktionen:
- Erkennung des zu messenden Körperteils
- ein Körperteil einrahmen und fixieren
- Verschiedene Filtermodi zur Temperaturmessung zwischen 36 und 39° Celsius
- Bedienoberfläche
- Schnappschussfunktion durch digitalen Trigger und Abspeichern des Bildes


## Anforderungen an die Entwicklungsumgebung
[Python 3.x](https://www.python.org/downloads/)


## Verwendete Libraries
- tkinter 
- from tkinter import *
- cv2
- customtkinter
- from operator import mil
- import lumpy as np
- from PIL import Image, ImageDraw, Imagefilter, ImageTK
- datetime

## Verwendete IDE
Visual Studio Code Version: 1.72.1 (Universal)

## Setup und Installation
### Software
#### Installation Raspberry Pi OS auf Micro-SD
Installiere mit dem [Raspberry Pi Imager](https://www.raspberrypi.com/software/) das Betriebssystem für den Raspberry Pi 3b v. 1.2 um anschließend folgende Imports über das Terminal zu installieren.

#### Terminal Installationen:
1. Installieren der Libraries:

Für Ubuntu: 
```
sudo apt-get install python3-tk
sudo apt-get install libopencv-dev
```

#### Implementierung von Code aus Repository
Um den gesamten Code ordnungsgemäß nutzen zu können, downloade [hier](https://gitlab.rz.htw-berlin.de/s0577479/gesundheitstechnik_thermograph/-/archive/main/gesundheitstechnik_thermograph-main.zip) die .zip Datei um ihn anschließend auf dem Raspberry Pi auszuführen. 

### Hardware
#### CAD
Der erste Prototyp für das Gehaeuse wurde mit AutoDesk 360 entworfen. Im Ordner [Gehaeuse](/Gehaeuse) wurden drei unterschiedliche Formate angelegt: .stp, .igs und .f3z. Falls ein anderes Format bevorzugt wird, kann über diesen [Link](https://mygmx81809.autodesk360.com/g/shares/SH9285eQTcf875d3c53958665734c225feb5) das gewünschte Format heruntergeladen werden.

Referenz unseres ersten Prototypen gibt es im Wiki unter dem Reiter Konstruktion.

***

### Elektronik
#### Bauteile
Folgende Bauteile werden für den Nachbau benötigt:<br>
Bildschirm: [Joy-IT 3,5" LCD-Display 480x320 Pixel](https://joy-it.net/de/products/RB-TFT3.5)<br>
Computer: [Raspberry Pi 3B](https://www.berrybase.de/raspberry-pi-3-modell-b)<br>
DC/DC Wandler: [adafruit PowerBoost 1000C](https://www.adafruit.com/product/2465)<br>
Sensoren: [FLIR Lepton Pure Thermal 2](https://groupgets.com/manufacturers/getlab/products/purethermal-2-flir-lepton-smart-i-o-module)
& [MLX 90640](https://www.adafruit.com/product/4407)<br>
Akku: [Eckstein Energy 3,7V 2500mAh](https://eckstein-shop.de/LiPo-Akku-Lithium-Ion-Polymer-Batterie-37V-2500mAh-mit-JST-PHR-2-Stecker-LP785060)<br>
Button: [Unimec MEC Momentary Push Button Switch](https://docs.rs-online.com/af73/A700000008823370.pdf)

## Support
General Support: 
Achim.Klenk@student.htw-berlin.de

Software Support: 
Aaron.Schultz@student.htw-berlin.de / Falko.Kristen@student.htw-berlin.de

CAD Support: 
Arthur.Schneider@student.htw-berlin.de

***

## Autoren
Achim Klenk, 
Falko Kristen, 
Aaron Schultz, 
Arthur Schneider

## Lizenz
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.


↑ [zurück zur Übersicht](#gesundheitstechnik-gruppenprojekt)
