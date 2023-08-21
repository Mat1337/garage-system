@ECHO OFF

:: switch into the yolov5 project directory
CD yolov5

:: train the model
python train.py --img 450 --batch 30 --epochs 15 --data ../model/LicenceModel.yaml --weights yolov5m.pt

:: revert to the original root directory
CD ..

:: wait for user input
PAUSE