# Group Picasso

### Installation for Ubuntu
* ```git clone git@github.com:thalvari/cc-project.git```
* ```cd cc-project```
* ```python3 -m venv venv```
* ```source venv/bin/activate```
* ```pip install -U pip setuptools```
* ```pip install -r requirements.txt```

### Usage
* ```python run.py [PATH_TO_CONTENT_IMG] [PATH_TO_STYLE_IMG]```

### Examples
Original content, style, markovified styles and generated artifacts:

![](images/content/golden_gate_sq.jpg)
![](images/styles/towers_1916_sq.jpg)
![](gifs/m1.gif)
![](gifs/a1.gif)

![](images/content/colva_beach_sq.jpg)
![](images/styles/clouds-over-bor-1940_sq.jpg)
![](gifs/m2.gif)
![](gifs/a2.gif)

![](images/content/statue_of_liberty_sq.jpg)
![](images/styles/zigzag_colorful.jpg)
![](gifs/m3.gif)
![](gifs/a3.gif)

![](images/content/eiffel_tower.jpg)
![](images/styles/red_texture_sq.jpg)
![](gifs/m4.gif)
![](gifs/a4.gif)

### References
* [markov-img-gen](https://github.com/JonnoFTW/markov-img-gen)
* [Magenta](https://github.com/tensorflow/magenta)
