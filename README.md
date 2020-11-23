# CSE 545 Project

This repository contains the code for Team 6's CSE 545 project.

## Dependencies

 - Python 3
 - sqlite3
 - ~~PostgreSQL~~ (not for development)
 - see `requirements.txt` for pip dependencies
 
## Development setup

Everything here should only be done once, unless noted otherwise.

Make a virtual environment:
```bash
$ cd /directory/where/you/cloned/this
$ python -m venv env
```

Activate it. **You have to do this every terminal session**:
```bash
$ source env/bin/activate
```

Install dependencies:
```bash
$ pip install -r requirements.txt 
```


Initialize `FLASK_APP`. **You have to do this every terminal session**:
```bash
$ export FLASK_APP=sbs.py
```

Now, set up the database
```bash
$ flask db init
$ flask db migrate -m "initial migration"
$ flask db upgrade
```

Insert initial testing data

```bash
$ python initdb.py
```

Now, you're good to go. To run the application:

```bash
$ flask run
```

## Implementation document

https://docs.google.com/document/d/1aqdolFjQ37W1SfJQcp4OA4GeoymEFvLtcRCK_uwyH9o/edit


# secure_banking_system
