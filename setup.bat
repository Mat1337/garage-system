@ECHO OFF

:: switch into the yolov5 project directory
CD yolov5

:: install the requirements for the yolov5 project
pip install -r requirements.txt

:: revert to the original root directory
CD ..

:: install the requirements for the current project
pip install -r requirements.txt

:: wait for user input
PAUSE