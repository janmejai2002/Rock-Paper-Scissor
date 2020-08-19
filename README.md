# Rock-Paper-Scissor

Enjoy a more realistic game of rock paper scissors against your computer than just pressing some buttons. This project was a lot of fun. I hope you enjoy it as well :D

---

## Installation

    pip install -r requirements.txt

or based on your settings you mgiht have to doo

    pip3 install -r requirements.txt

I suggest making a new environment because a new Tensorflow version has been released. Your existing environment may face some problems.

---

## Play

To see a small video tutorial check [this](https://github.com/janmejai2002/Rock-Paper-Scissor/blob/master/RPS.gif) gif I made :D

You might have to use `python3` for the commands ahead.

Open terminal in project directory. Then do :

    python main.py

_To know about commandline arguments check the More Information Section at the end_

Your webcam will start:

 - Move the blue box using `W`, `S`, `A` and `D`.
 - Resize using `I` and `K`.
 - Reset it using `R`.

Now make sure your hand is not inside the box and you also do not have any moving object inside it.

Press `B` to capture the background.

Now you can put your hand inside the box. That is the zone for your move.

The model is pretty robust so you should not face frequent issues of inaccurate results while being to close or far from the camera. If you do, feel free to train the model again.

---

## Instructions for training your own model

I have trained model on the binary masks of my hand gestures to not allow the factor of background to seep in. It has led to a greater accuracy.  

To understand more about it refer [OpenCv background Subtraction]((https://docs.opencv.org/3.4/d1/dc5/tutorial_background_subtraction.html#:~:text=OpenCV%3A%20How%20to%20Use%20Background%20Subtraction%20Methods&text=Background%20subtraction%20(BS)%20is%20a,scene)%20by%20using%20static%20cameras.)

Have a look at the images inside `notebooks/data`.

### Collecting data

 - For _collecting_ your image data you can use my repo here [Webcam-Data-Utility](https://github.com/janmejai2002/Webcam-Data-Utility). It makes collecting images using webcam hassle free.

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

---

## More Information :

You can view all the command line arguments using:

    python main.py --help

Commandline arguments have been defined inside `utils/helper_functions.py`.

The `model` argument was explained above. For rest proceed :

### Detection Accuracy

 - To enhace the detection accuracy I have further designed an algorithm which loads prediction for the frames inside a `deque` with a `maxlen=4` as default. I've explained it at the end.

 - You can play with this parameter as follows

        python main.py --buffer 7

 - Increasing will have a slight effect on the trigger speed of model but make it even more robust to outlier detections which take place while you are moving your hand out of the frame etc.


### Webcam

- If you face any error with your webcam then you can try another index location for webcam by doing:
  
        python main.py --webcam 1

---

## The Use of deque


Now, the model is not 100% accurate every frame, slight hand movements combined with webcam noise can trigger new predictions. You would not want an undesired action to have consequences. To solve this problem I had to use deques.

Deque have `O(1)` complexity in popping or appending elements. So they are pretty fast to work with.


To learn how they work check [here](https://docs.python.org/3/library/collections.html#collections.deque).



Now see the following code blocks from `main.py` :

First I initialized two deques before the `while`:

    # for prediction sensitivity
    pred_deque = deque(maxlen=args["buffer"])
    prev_pred = deque(maxlen=args["buffer"])


Then this part inside the `while`:


    if isBgCaptured == 1:
            prediction, score = predict_rgb_image_mobilenet(thresh, model)
            pred_deque.append(prediction)

            if pred_deque != prev_pred and (pred_deque.count(pred_deque[0]) == len(pred_deque)) and len(pred_deque) == args["buffer"]:
                prev_pred = pred_deque.copy()
                # print(f"Prediction : {prediction}")

                # Align the '|' in moves with upper
                # The closest I could do it.
                if prediction != 'None':
                    set_prediction = f"  {prediction}  "
                else:
                    set_prediction = prediction

                # get computer move after player move has been predicted.
                computer_move = game_brain.getWinner(prediction)
                score_dict = game_brain.getCurrentScore()
                # print(f"Current Score : {score_dict}")


Ignore the `set_prediction` part that is just my best attempt to align the prediction and computer move text with the score text.

Predictions should be made only when the background has been captured, hence the `isBgCaptured`

Now, when you come inside the first if statement, it sends the image(mask) for prediction and gets a prediction in the form of `R`,`P`,`S` or `None`.

That prediction is appended to `pred_deque`.

From now I will refer the following variable as :

- `prev_pred` --> Previous predictions deque.
- `pred_deque` --> Current predctions deque.


After this has happened for `buffer` frames, the following combination is formed:
-  Current prediction deque is filled completely.
-  Previous prediction deque does not have any elements.
-  Suppose you did not give any gesture to the Box (as all this happens pretty fast), so all elements inside Current prediction deque are same i.e all are `None`.

    - So, the second `if` gets a `True` value:
    - Now Previous prediction deque is set to be Current Prediction deque. I have used `.copy()` and not `prev_pred = pred_deque` because it copies references and that is not what we desire.
    - The game action is then triggered to get a move from computer.

After the above, in every loop the conditions checks if the all the elements inside your current prediction deque are same and also if the current prediction deque is entirely different from the previous prediction deque.

So that is the explanation, I first tried it using `list` but observed a massive decrease in speed. Then found out that `list` have `O(n)` complexity for appending and popping. After some researching I got to know about deques.



Thank you for making it so far :D

If you enjoyed the game, a star is really appreciated :D
