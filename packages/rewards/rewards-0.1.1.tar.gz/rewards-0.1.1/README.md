# **rewards** 
### A low code sdk for crearing custom environments and deep RL agents. 


<br>

### **Installation** 

**`[linux]`** 

Installing `rewards` is easy in linux. First clone the repository by running 

```bash
git clone https://github.com/rewards/rewards.git
```
One cloned go to the repository and make sure `make` is installed. If not installed just run:

```bash
sudo apt install cmake 
```

Once done, now create a new virtual environment and install dependencies. You can achieve
this by running the following:

```bash
make virtualenv
make install 
```
This should install all the dependencies and our sdk `rewards:v1.0.0`. 

<br>

**`[windows]`** 

For installation in windows, it's also simple. All you have to do is just clone the repository same as before. Then create a new virtual environment. 

```bash
virtualenv .venv
```

Load the virtual environment 
```
.\venv\Scripts\Activate
```
Now go to the repository and install all the dependencies and the `rewards`s package.

```bash
pip install -r requirements.txt
python setup.py install
```

<br>

### **Getting started**

**`rewards`** is mainly made for two important reasons. 

- First we want to make learning reinforcement learning easy, by introducing this low code framework. So that folks do not need to spend more time in making environments or other stuff. All they can focus is on creating different agents, models and expeiment with them.

- We want to make it as interactive and begginer friendly as possible. So we are also introducing **`rewards-platform`**  which where we gamified the experience of learning RL.

- If playing games can be fun and competitive then why not RL? Hence with **`rewards-platform`** and **`rewards`** you can host and join ongoing competition and learn RL with your friends. 

**NOTE**: Our coming enterprise version is mainly focussed to build the same but for RL/Robotics based 
companies where we want to ensure that their focus lies more on the research rather creating environments and other configurations. 

**Take a look on how to get started with a sample experiment** 

Currently this version of **`rewards`** only supports a single game and environment. That is `car-race`. We will be adding support for more environments (including gym, unity, and custom environments) very soon. 

So let's go ahead and see how to get started with a sample experiment.

```python
from rewards import workflow

configs = workflow.WorkFlowConfigurations(
    EXPERIMENT_NAME="Exp 3", 
    MODE="training", 
    LAYER_CONFIG=[[5, 64], [64, 3]]
)


flow = workflow.RLWorkFlow(configs)
flow.run_episodes()
```

First you call our sdk's `workflow` module. The workflow module helps us to 

- Create Environments and configure environments
- Create models and configure them 
- Run the whole experiment and log all the results 

All at one place. We first get started with writing our own configuration using 

```python 
configs = workflow.WorkFlowConfigurations(
    EXPERIMENT_NAME="Exp 3", 
    MODE="training", 
    LAYER_CONFIG=[[5, 64], [64, 3]]
)
```

**Here is the table of configuration and what they means** 

| Configuration Name | TYPE            | What it does                                                                                                                                                                                                                                   | Default value                                                                                              | Options                                                                                                                                                                                                                                                                               |
| ------------------ | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| EXPERIMENT_NAME    | `str`             | It tells what is the name of the experiment. The name of the experiment will be logged inside user's weights and biases projects dashbord.                                                                                                     | sample RL experiment                                                                                       | any string                                                                                                                                                                                                                                                                            |
| ENVIRONMENT_NAME   | `str`             | It states the name of the environment. `rewards:v1.0.0` only supports one environment for now and that is `car-race`.                                                                                                                          | car-race                                                                                                   | NULL                                                                                                                                                                                                                                                                                  |
| ENVIRONMENT_WORLD  | `int`             | According to our convention we keep some environments for training and some for testing (which are unseen). At one point of time, you can only train your agent on one single train environment.                                               | 1                                                                                                          | 0/1/2                                                                                                                                                                                                                                                                                 |
| MODE               | `str`             | This tells us which mode the agent is been running i.e. either in train or test mode.                                                                                                                                                          | training                                                                                                   | training/testing                                                                                                                                                                                                                                                                      |
| CONTROL SPEED      | `float`           | For our car environment user can set the control speed of the car environment.                                                                                                                                                                 | 0.05                                                                                                       | (0 - 1]                                                                                                                                                                                                                                                                               |
| TRAIN_SPEED        | `int`             | For our car environment user can set the control speed of the car environment.                                                                                                                                                                 | 100                                                                                                        | 1 - 100                                                                                                                                                                                                                                                                               |
| SCREEN_SIZE        | `Tuple`           | The size of the pygame window.                                                                                                                                                                                                                 | (800, 700)                                                                                                 | User' choice                                                                                                                                                                                                                                                                          |
| LR                 | `float`           | Learning rate                                                                                                                                                                                                                                  | 0.01                                                                                                       | User' choice                                                                                                                                                                                                                                                                          |
| LOSS               | `str`             | Loss function name                                                                                                                                                                                                                             | mse                                                                                                        | mse , rmse, mae                                                                                                                                                                                                                                                    |
| OPTIMIZER          | `str`             | Optimizer name                                                                                                                                                                                                                                 | adam                                                                                                       |adam, rmsprop, adagrad                                                                                                                                                                                                                                            |
| GAMMA              | `float`           | Hyper parameter `gamme` value                                                                                                                                                                                                                  | 0.99                                                                                                       | 0 - 1                                                                                                                                                                                                                                                                                 |
| EPSILON            | `float`           | Hyper parameter `epsilon` value                                                                                                                                                                                                                | 0.99                                                                                                       | 0 - 1                                                                                                                                                                                                                                                                                 |
| LAYER_CONFIG       | `List[List[int]]` | This expects a list of list. Where the inner list will have only two values [input neurons, output neurons]. This configuration will help us to build the neural network for our agent. The first value for the current environment must be 3. | [[5, 64], [64, 3]] | Here user can add more values but the values `5` in the first and `3` in the last must be fixed for this current environment that we are supporting. Example: <br> `[[5, ...], [..., ...], ...., [..., 3]]`, <br> Where `...` can be any value. We recommend to keep it between (1 - 256) |
| CHECKPOINT_FOLDER_PATH    | `str`             | The model checkpoint path from where it should be loaded. This can be either `None` then it will auto create a checkpoint path and store all the checkpoints there else it will save the models on the folder mentioned if exists.                                                                                                                                                                                      | `./saved_models`                                                                                                 | User's choice                                                                                                                                                                                                                                                                         |
| CHECKPOINT_MODEL_NAME    | `str`             | The name of the model name. This can be either named by the user or by default it will create the model name as `model_{<latest_date_and_time>}_.pth`.                                                                                                                                                                                       | `model_2023-04-07 16:10:36.366395_.pth` (This is just an example)                                                                                                 | User's choice                                                                                                                                                                                                                                                                         |
| REWARD_FUNCTION    | `Callable`        | Users are expected to write some reward function (`Callable`) and then have to use this reward function for agent's training.|  ```def default_reward_function(props): if props["isAlive"]: return 1 return 0 ```| User's choice <br> **some important parameters** <br><br> `isAlive` represents whether the car is alive or not. So on that basis we can penalize our agent. <br><br> `obs` The car's radar's oberservations values. (more on documentation) <br> <br>`rotationVel` Car's rotational velocity value (more on documentation)        |


So above is a quick overview of how to use different reward configurations. Now once configuration part is done, load those configuration to `RLWorkFlow()` and run for a single episodes. 

After this you are ready to run the above code:

```python 
from rewards import workflow

configs = workflow.WorkFlowConfigurations(
    EXPERIMENT_NAME="Exp 3", 
    MODE="training", 
    LAYER_CONFIG=[[5, 64], [64, 3]]
)


flow = workflow.RLWorkFlow(configs)
flow.run_episodes()
```

Here you will be able to see the game, and a very nice dashboard with all the runs and configurations and nice graphs. Stay tuned with `rewards.ai` for further updates, documentation and examples. 