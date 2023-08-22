# garage-system
proof of concept garage security system written in python

# model
traning data for the model was split in following ration:
- traning data: **60%**
- validation data: **20%**
- testing data: **20%**

it was trained on **15** epochs with the batch size of **30**

![traning-result](model/licence/results.png)

# setup

### anaconda

```shell
  conda create -n garage python=3.8
  conda activate garage
  setup.bat
```

# credits
**[dataset](https://www.kaggle.com/datasets/andrewmvd/car-plate-detection)**
<br>
**[model](https://github.com/ultralytics/yolov5)**
