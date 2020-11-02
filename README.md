# Coding-Challenge-Python

## Prerequisites
This code needs Python with ITK, VTK and argparse.

## The code
Reads an image given in argument, applies the ITK filter choosen, displays the original and the filtered image in a VTK renderer.

### Argparse
**Positional argument** : FileName.  
**Optional arguments** : output, filter (median or threshold), radius (int, if median filter).  
