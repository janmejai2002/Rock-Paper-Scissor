# Stone-Paper-Scissor
A Computer Vision project which identifies your hand-gesture in real time and plays against you :D

It is quite easy to setup. Read ahead to learn how to play and install

I am still working on the project to improve the `game experience`.


## Installation

    pip install -r requirements.txt

or based on your settingS you mgiht have to doo

    pip3 install -r requirements .txt

I suggest making a new environment because a new Tensorflow version has been released. Your existing environment may face some problems.


## Play

Open terminal in project directory. Then do :

    python main.py

_To know about commandline arguments check the More Information Section at the end_

Your webcam will start:

 - Move the green box using `W`, `S`, `A` and `D`.
 - Resize using `I` and `K`.
 - Reset it using `R`.

Now make sure your hand is not inside the green box and you also do not have any moving object inside it.

Press `B` to capture the background.

Now you can put your hand inside the Green Box. That is the zone for your move.

The model is pretty robust so you should not face issues of inaccurate results while being to close or far from the camera. If you do, feel free to train the model again.


## Instructions for training your own model

I have trained model on the binary masks of my hand gestures to not allow factor of background etc to seep it. It has led to a greater accuracy.


### Collecting data

 - For _collecting_ your image data use my repo here [Webcam-Data-Utility](https://github.com/janmejai2002/Webcam-Data-Utility) to collect your own images.

 - For splitting collected images into `train-val-test` use [split_folders](https://pypi.org/project/split-folders/) .  It is an amazing tool and just needs a single line of code.
 - You can also train your own model by using the images I have collected present inside `notebooks/data` dir.

### Training Model

 - Use `notebooks/train.ipynb`. You can even make your own model inside it and won't have to worry about data-loading etc.
 - While training on your PC do check the `batch_size` parameter at various places. You may have `OOM (Out of Memory)` errors if training on CPU. Reduce it until you find the desired amount.

### Inference

- Use `notebooks/confusion.ipynb` to get the confusion matrix for your trained model.
- You will have to change the name of the model you want to load `model_path` variable based on the name of your saved model.

### Integration
- After training your model, place it inside the `models` dir.

- While running `main.py` use the following command line arguments:


        python main.py --model "xyz.h5"

 - Replace `xyz.h5` with the name of your model



## More Information :

You can view all the command line arguments using:

    python main.py --help

The `model` argument was explained above. For rest proceed :

### Detection Accuracy

 - To enhace the detection accuracy I have further designed an algorithm which loads prediction for the frames inside a `deque` with a `maxlen=2` as default. I will add an explanation for it in sometime.

 - You can play with this parameter as follows

        python main.py --buffer 3

 - This will have a slight effect on the detection speed of model but make it even more robust to outlier detections which take place while you are moving your hand out of the frame etc.


### Webcam

- If you face any error with your webcam then you can try another index location for webcam by doing:
  
        python main.py --webcam 1








If you like it then do star. Thank you.

I will be working on this for sometime and introduce some more features for example a buffer state. So make sure you check the repo in a few days.

If you face errors feel free to create an issue.

