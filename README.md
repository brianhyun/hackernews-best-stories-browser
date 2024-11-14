Hacker News Best Stories Browser
================================

This project is a simple script that fetches the best stories from Hacker News and opens them in a web browser. It keeps track of the stories you've already visited to avoid showing you the same ones again.

How to Use
------------

1. Clone this repository to your local machine.
2. Make sure you have Python installed on your system.
3. Install the required packages by running `pip install requests webbrowser` in your terminal.
4. Run the script by executing `python main.py` in your terminal.
5. The script will open the top 10 best stories from Hacker News in your default web browser.

Features
--------

* Fetches the best stories from Hacker News.
* Keeps track of the stories you've already visited.
* Opens the top 10 best stories in your web browser.
* Avoids showing you the same stories again.

Technical Details
-----------------

* The script uses the Hacker News API to fetch the best stories.
* It stores the IDs of visited stories in a JSON file named `visited_stories.json`.
* The script uses the `requests` library to make HTTP requests to the Hacker News API.
* It uses the `webbrowser` library to open the stories in your default web browser.

License
-------

This project is licensed under the MIT License.
