# Face Verifier

Checks whether there is a face in an image.   

## Prerequisities

  * Python 2.7
  * [OpenCV](http://opencv.org)   
  * Data for the haar face classifiers are in the `data` folder.

## Usage

    verifier.py <image_path> [--min_area=<min_area>]

    Options:
      -h, --help             Show this screen
      <image_path>           Filepath to image (.jpg, .jpeg, .png)
      --min_area=<min_area>  Minimum rectangular face area [default: 0]
      --version              Show version

## Return values

* ok = `Good. Face detected`
* no_face = `No face detected`
* not_frontal = `Not a frontal face`
* no_eyes = `Both eyes not detected`
* too_small = `Face too small`

## Example

    $ python verifier.py lena.png
    Good. Face detected


