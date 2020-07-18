<div align="center">

![alt](./art/bot.png)

# Github Follow Bot

</div>

## What Does it Do?

Follows Github users and also their followers from a user provided list of Github handles.

## Installation

* Clone the repo.
* Create a Python virtual environment.
* Install the dependencies:

    ```
    pip install -r requirements.txt
    ```

* Download compatible [Chrome Driver](https://chromedriver.chromium.org/downloads) for your OS.

* Provide your Chrome Driver path, credentials and the target users' Github usernames:

    ```python
    CHROME_DRIVER_PATH = "./    chromedriver_linux64/chromedriver"

    # Put your github username and password here
    YOUR_NAME = "yourname"
    YOUR_PASS = "yourpass"

    # List of people's github usernames whose followers you want to follow
    # This could be even yourself
    TARGET_NAMES_LIST = ["rednafi", "gvanrossum"]
    ```

* Run the bot and let it do its work:

    ```
    python -m followbot.bot
    ```

## Disclaimer

I created this just to fiddle with some [selenium](https://selenium-python.readthedocs.io/). The code could be polished. Also, it's debatable whether you should use a bot to follow people or not. Use at your own risk 🤷‍♂️
