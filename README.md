# FootballPath / ViDraw
SD Hacks 2016

Given a football video stream, track the receiver and draw his path. 

##Our algorithm
1. Run k-means on RGB to separate green grass and colored players
2. Run k-means on spatial coordinate to distinguish players 
3. Draw rectangles around them
4. Use Camshift to track movements through time in video (need OpenCV library)
5. Connect the dots and formuate the path 

Setting up OpenCV: http://www.pyimagesearch.com/2015/06/29/install-opencv-3-0-and-python-3-4-on-osx/
