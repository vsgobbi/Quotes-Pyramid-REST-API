
## Description
Sample RESTFul API using Pyramid Framework and SQLAlchemy libs to deploy local or remotely like in Google App Engine.
Requester library created under lib/ folder to request remote AWS API of quotes.
This API creates and access quotes, originally from python Zen (try:
  
```shell
import this
```
 to check quotes):

## Table of Contents


- [Installation](#installation)
- [Usage](#usage)
- [Tests](#tests)
- [Features](#features)
- [License](#license)


<a href="https://gnu.org"><img src="https://www.gnu.org/graphics/gplv3-127x51.png" title="FVCproductions" alt="GPL"></a>

<!-- [![FVCproductions](https://avatars1.githubusercontent.com/u/4284691?v=3&s=200)](http://fvcproductions.com) -->
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](http://img.shields.io/travis/badges/badgerbadgerbadger.svg?style=flat-square)](https://travis-ci.org/badges/badgerbadgerbadger)
[![Coverage Status](http://img.shields.io/coveralls/badges/badgerbadgerbadger.svg?style=flat-square)](https://coveralls.io/r/badges/badgerbadgerbadger) 


---

## Installation

### CLONE PROJECT
- Firstly, clone this repo to your local machine

```shell
git clone git@github.com:vsgobbi/quotes_pyramid_api.git

```
or 

```shell
git clone https://github.com/vsgobbi/quotes_pyramid_api.git
```
---


### Setup

##### CREATE VIRTUAL ENV

- Create virtualenv using Python3.7
```shell     
virtualenv -p python3.7 venv
```
- Activate the virtualenv
```shell     
source venv/bin/activate
```
- Verify if version is correct
```shell     
python --version #expected return: Python3.7
pip --version
```

- Install main libs
```shell     
pip install -r requirements.txt
```
- Initialize SQLAlchemy database and migration
```shell
python initialize_db.py development.ini
```
- Install and export egg.info of project
```shell
pip install -e .
```
- Init database migration to create tables
```shell
initialize_db development.ini
```
- Start server (with development configs)
```shell
pserve development.ini --reload
```

## Tests
- Run python unittests
```shell     
python -m unittest discover quotes/
``` 

## Features
> Using the following main libs: 
- Pyramid, Request, Transaction, SQLAlchemy


---
## Usage

#### How to use requester library:
```python
from lib.requester import get_quotes, get_quote
```

##### Run tests :
```python
python -m unittest discover .
```

## Support

Reach out to me at one of the following places!
### Vitor Sgobbi, 2019 
- E-mail at <a href="mailto:" target="_blank">`sgobbivitor@gmail.com`</a>
- Instagram at <a href="https://www.instagram.com/vsgobbi/" target="_blank">`@vsgobbi`</a>
- Github at <a href="https://www.github.com/vsgobbi" target="_blank">`@vsgobbi`</a>

---

## License

 [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
- **[GPL license](https://www.gnu.org/licenses/gpl-3.0)**
- Copyright 2019 © <a href="https://github.com/vsgobbi" target="_blank">Vitor Sgobbi</a>.
