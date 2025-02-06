# Py-Textures
 
A small python program that produces noise textures using numpy and matplotlib. Having worked with Godot, Unity, and Blender, I wanted a simple way to create and edit static noise images that could be used for procedural terrain, textures, and more. This repository contains two python files that allow the user to interface with the noise generation functions:
- <strong>textures.py</strong> is a tkinter app designed to interface with these noise textures through layers and composition to produce new textures.
- <strong>noisegen.py</strong> provides a text interface to produce simple noise files.

The project currently supports white noise, perlin noise, worley (or cellular) noise, fractal brownian motion (layered perlin), and directional stripes.

To use <strong>noisegen.py</strong>, provide shell commands in the following format:
```
C:\...> py -m noisegen.py [noise_type, <str>] [scale, <int>]
```

The noise_type parameter currently accepts 'white', 'perlin', 'worley', and 'white'. Using the following commands will produce the following images:<br>
```
C:\...> py noisegen.py worley 4 
```
<img src='worley_s4.png'>

```
C:\...> py noisegen.py perlin 2
```
<img src='perlin_s2.png'>

<br>
<strong>textures.py</strong> currently supports layers and alpha channels but has not been connected to Noise.py yet.