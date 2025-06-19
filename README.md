Idea:
- Create a Python based GUI app where you can provide and image and have it remove its background
  and then make it look like it was cut out from a piece of paper
- It would be nice to have the GUI show you a preview of the image and also let you change show
  the edges look on it
- Would also be nice to choose what the main subject is (but this might be a future feature)

Potential New Approach:
- Create a GUI that shows the image after the background has been removed
- Let the user select how they want to crop the image (aka like the pen tool in Photoshop)
- The user should also be able to select the background color for their image
  (or transparent)

Libraries to be Used:
- rembg
  - Remove the background of an image
- opencv-python-headless
  - Image loading/saving, Gaussian blur, etc...
  - Using the headless version to avoid potential conflicts in the future
- opensimplex
  - Noise generation to create realistic torn/jagged edges for the paper cutout-effect
