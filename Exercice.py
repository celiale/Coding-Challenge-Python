import itk
import vtk
# import matplotlib.pyplot as plt
import argparse

## Arguments 

parser = argparse.ArgumentParser()
parser.add_argument('FileName', help='enter the name of the input file')
parser.add_argument('-out', '--output', help='enter the name of the output file')
parser.add_argument('-f', '--filter', help='choose the filter to apply (median, threshold)')
parser.add_argument('-r', '--radius', type=int, help='choose the radius of the median filter')

args = parser.parse_args()


## Input and output

PixelType = itk.UC
Dimension = 2
ImageType = itk.Image[PixelType, Dimension]

image = itk.imread(args.FileName, itk.UC)
# image = itk.ImageFileReader.New(FileName=args.FileName)

if args.output:
    output = args.output
else :
    output = 'filtered.png'


## Filters

if args.filter == 'median' :
    # Filter = itk.MedianImageFilter.New(image, Radius = 2)

    Filter = itk.MedianImageFilter[ImageType, ImageType].New()

    if args.radius :
        radius = args.radius
    else : 
        radius = 2

    Filter.SetRadius(radius)

elif args.filter == 'threshold' :
    Filter = itk.BinaryThresholdImageFilter[ImageType, ImageType].New()
    Filter.SetInput(image)
    Filter.SetLowerThreshold(0)
    Filter.SetUpperThreshold(150)
    Filter.SetOutsideValue(250)
    Filter.SetInsideValue(0)
else :
    Filter = itk.MedianImageFilter.New(image, Radius = 0)

Filter.SetInput(image)
itk.imwrite(Filter, output)
Filter.Update()
OutputImage = Filter.GetOutput()


## Display Matplotlib
# plt.figure(1)
# plt.subplot(121)
# plt.imshow(image, cmap='gray')
# plt.title('Original image')
# plt.axis('off')
# plt.subplot(122)
# plt.imshow(OutputImage, cmap='gray')
# plt.title('Filtered image')
# plt.axis('off')
# plt.show()

## Display vtk renderer

rw = vtk.vtkRenderWindow()
# print(rw.GetSize())
rw.SetSize(2500,1500)
rwInteractor = vtk.vtkRenderWindowInteractor()
rwInteractor.SetRenderWindow(rw)
rw.Render()
rw.SetWindowName('Exercice Python : Filtering an image')

xmins = [0, .5]
xmaxs = [0.5, 1]
ymins = [0, 0]
ymaxs = [1, 1]

for i in range(2):
    
    # Read the file
    reader = vtk.vtkPNGReader()
    if i == 0 :
        reader.SetFileName(args.FileName)
    else :
        reader.SetFileName(output)
    reader.Update()

    # Convert the image to a polydata
    imageDataGeometryFilter = vtk.vtkImageDataGeometryFilter()
    imageDataGeometryFilter.SetInputConnection(reader.GetOutputPort())
    imageDataGeometryFilter.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(imageDataGeometryFilter.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetPointSize(3)

    # Setup rendering

    renderer = vtk.vtkRenderer()
    rw.AddRenderer(renderer)
    renderer.SetViewport(xmins[i], ymins[i], xmaxs[i], ymaxs[i])
    renderer.AddActor(actor)
    renderer.SetBackground(1,1,1)
    renderer.ResetCamera()


rwInteractor.SetRenderWindow(rw)
rwInteractor.Initialize()
rwInteractor.Start()