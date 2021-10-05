RLE compressor
=========
This repo is a python-implementation of rle-compression algorithm. The program uses concurrent programming. Repo is based on case study from book: **Python 3 Object Oriented Programming second edition.**

Table of contents
=================

<!--ts-->
   * [Update](#Update)
   * [Theoretical background](#Theoretical background)
   * [Tech](#tech)     
   * [Installation](#installation)
   * [Usage](#usage)
   * [features](#features)
   * [ToDo](#ToDo)
   * [Status](#Status)
   * [Inspiration](#inspiration)  
   * [Resources](#resources)
<!--te-->
Update
============
Theoretical background
============
RLE is a lossless method of compression. It replaces  consecutive identical values into a code consisting of the character and the number marking the length of the run. Thus it's not garaunteed that the result size is less than the size  input
ONe extreme case is all teh values are differ.
An example:
```bash
aaabbca => a3b2c1a1
```
You can refer to [this link](https://www.section.io/engineering-education/run-length-encoding-algorithm-in-python/) for more info. This program implements RLE for black and white images(otherwise it converts the image into bitmap image). To do that, it splits the image into rows, which in turns is splited into chunks of 128 bit. 
Each row is compressed using thread. 

Tech
============
The code is implemented using python3.8 . It uses the following libraries:
<!--ts-->
* argparse
* numpy
* Pillow
* futures
* pathlib
<!--te-->
Installation
============
For installation, first:
Install the virtualenv package:
```bash
pip install virtualenv
````
Create the virtual environment:
```bash
virtualenv mypython
````
To activate the virtual environment, under Mac OS / Linux
```bash
source mypython/bin/activate
````
under windows, use the following command:
```bash
mypthon\Scripts\activate
```
Then run the following command:
```bash
pip install -r /path/to/requirements.txt
```
Usage
=====
features
=====
ToDo
=====
Status
=====
Inspiration
=====
Resources
=====
* [Python 3 Object-oriented Programming - Second Edition](https://www.packtpub.com/product/python-3-object-oriented-programming-second-edition/9781784398781)
