# API UserParams

The project is a realization of interaction with database.

## Description

Project consists of several views which could be used for create, read and update database entities. 
### The views are:

* set_param

Creates entity in database if it doesn't exist, else changes existing entity. Works only for existing users.

Allowed methods: POST

Url for usage:
```
/api/parameters/username/param_name/param_type/
```
Also requires atribute "Value", which should be 
sent in body of request. Example:
```
{"Value": 'value to set'}
```

* get_param

Returns user parameter if it exists in database. Without param_type return user parameters of all types. Works only for 
existing users.

Allowed methods: GET

Urls for usage:
```
/api/parameters/<username>/<param_name>/
```
or
```
/api/parameters/<username>/<param_name>/<param_type>/
```

* get_all_user_params

Returns all user parameters.

Allowed methods: GET

Url for usage:
```
/api/parameters/<user>/
```

* set_several_params

Sets several parameters for user.

Allowed methods: POST

Url for usage:
```
/api/<username>
```
Data for this view must be sent in request body.
Example:
```
{"Query": 
 [
    {
   "Operation":"SetParam", 
   "Name":<param_name>, 
   "Type":<param_type>, 
   "Value":<param_value>
  },
 ]
}
```
Can be several set operations.

* add_user

Allowed methods: POST

Creates new user in database.

Url for usage:
```
/api/add_user/
```

* main_page

Start page.

Url for usage:
```
/
```

## Usage
1. After cloning repository from github create your virtual environment.

For Windows:
```bash
python -m venv env
```
For Linux:
```bash
python3 -m venv env
```
2. Activate virtualenv:

For Windows:
```bash
venv\Scripts\activate.bat
```
For Linux:
```bash
source venv/bin/activate
```

3. Install requirements
```bash
pip install -r requirements.txt
```

4. Enjoy of usage(app starts working after running the file 'main.py')