<h1 align="center"> SipStore </h1>

![made by](https://img.shields.io/badge/made_by-slychagin-blue)
![coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![python](https://img.shields.io/badge/python-v3.10.5-green)
![django](https://img.shields.io/badge/django-v4.1-green)
![postgres](https://img.shields.io/badge/postgres-15-green)
![Python](https://img.shields.io/badge/Python-17.2%25-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-37.0%25-yellow)
![Ajax](https://img.shields.io/badge/Ajax-yes-blue)
[![templates](https://img.shields.io/badge/templates-safira-orange)](https://preview.themeforest.net/item/safira-organic-food-html-template/full_screen_preview/25782200?_ga=2.120049934.701405216.1682335958-16236204.1679321900)

![Home page](https://github.com/slychagin/sip-store/blob/master/readme_assets/home_page.jpg)
<h2 align="center"> [Visit Online Store](https://food.saltway.in.ua/) </h2>

### [README file in Russian](https://github.com/slychagin/sip-store/blob/master/README_RUS.md)

## Description
After a year of learning Python, I got the opportunity to develop a real online store selling meat semi-finished
products. While working on this project, I have powerfully upgraded my skills in working with Python and Django.
The frontend (html, css and some javascript) was separately purchased and kindly provided by my client.
Unlike my previous work, in this project I tried to do everything in an adult way, starting with views based on
classes and ending with testing my own code (for more details, see the section "About the project").
At this stage, the site is filled fake data, which will soon be replaced by real content.

## About the project
#### What is the project written in?
- the online store is written in Python (v3.10.5), Django framework (v4.1);
- Postgres 15 database;
- a ready-made template (HTML, CSS and JavaScript) was used as the front;
- many functions written in jQuery using Ajax.
#### A little about views
- most views are written using CBV;
- views that interact with Ajax - based on functions.
#### Without reload
- some functionality that needed to be done without reloading the page (for example, add products
to cart, add to wish list, change the number of added products, confirm forms, etc.) was implemented with
using Ajax.
#### Let's trust Celery
- the project implemented scheduled tasks (updating delivery departments, clearing expired sessions, monitoring
expiration dates of promotional codes), for which I used Celery in conjunction with Redis;
- tasks can be adjusted and added from the admin panel.
#### Third Party Services
- to inform the site administrator about new orders, a Telegram bot was connected;
- after confirming the order, the bot sends a telegram message with the details of the order and the buyer's data;
- the site is connected via API to the delivery service Nova Poshta (when placing an order, the buyer can enter the
name locality, for which the database will give him a list of delivery offices in his city);
- in the contacts section, you can see Google maps with marked points of sale (connection via Google API).
#### Code testing
- I wrote about 300 tests using the unittest library;
- code coverage by tests is checked using coverage and is 100%;
- tested everything: views, forms, models, Selenium tests.
#### Project deploy
- it was originally planned to host the site on a separate server, for which I dockerized the project.
For project deployment on after some settings, you will need to execute several commands (this version of the
project is in git branch master). In this case, the application starts by uWSGI;
- but in order to save money, since the customer already had a connected e-VPS hosting without a separate server,
the project had to slightly adapt to these conditions (git branch e-vps). Since Postgres and Docker is not installed
on this hosting, I connected the built-in SQLite3 database and deployed the project in an old-school way without Docker;
- in the future, perhaps, they will decide to transfer the site to a dedicated server, which will not be difficult
with Docker.

## In plans for the future
- connection of the payment system;
- it will be possible to implement user registration (at the moment we decided that this is not necessary);
- creation of the necessary additional functionality at the request of the site owner;
- filling the necessary sections of the site (as information is received from the owner of the site).