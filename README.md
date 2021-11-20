"# Team26-AY21" 

### Built With
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Visual Studio Code](https://code.visualstudio.com/)

### Optional Built
- [Anaconda](https://www.anaconda.com/products/individual)


<h1>Installation</h1>

1. Clone the repo

```sh
git clone with HTTPS        https://github.com/SIT-ICT3x03/Team26-AY21.git
git clone with SSH          git@github.com:SIT-ICT3x03/Team26-AY21.git
git clone with Github CLI   gh repo clone SIT-ICT3x03/Team26-AY21
```
2. Install the necessary files
(Choose any of the 3 to follow on the terminal of Vs Code up to own preferences)


CMD
```sh
# This creates a virtual environment so that when you install the libraries
# it's only isolated to this environment
1. python -m venv venv (optional)
    # This is to activate the virtual environment you just downloaded
    - venv\Scripts\activate

# This installs all the require libraries needed for this project
2. pip install -r requirements.txt

# Sets the main.py file as the main app for flask
3. set FLASK_APP=main.py

# Sets the project environment to development so that the project will refresh upon
# changes to the code without needing to restart the server
4. set FLASK_ENV=development

# Runs the flask project
5. flask run

# if running more then 1 flask project set different port[OPTIONAL]
6. flask run --host 127.0.0.1 --port 5001
```
PowerShell
```sh

# This creates a virtual environment so that when you install the libraries
# it's only isolated to this environment
1. python -m venv venv (optional)
    # This is to activate the virtual environment you just downloaded
    - venv\Scripts\activate.ps1

# This installs all the require libraries needed for this project
2. pip install -r requirements.txt

# Sets the main.py file as the main app for flask
3. $env:FLASK_APP="main.py"

# Sets the project environment to development so that the project will refresh upon
# changes to the code without needing to restart the server
4. $env:FLASK_ENV="development"

# Runs the flask project
5. python -m flask run
```
Anaconda
```sh
# Creating a "team26meok" venv with anaconda through terminal on vs code 
1. conda create --name team26meok python=3.8

#Activate team26meok venv 
2. conda activate team26meok

# This installs all the require libraries needed for this project
3. pip install -r requirements.txt

# Sets the main.py file as the main app for flask
3. set FLASK_APP=main.py

# Sets the project environment to development so that the project will refresh upon
# changes to the code without needing to restart the server
4. set FLASK_ENV=development

# Runs the flask project
5. flask run

```
3. Error in running flask?
```sh
# Refer to the venv folder you will see the file dir as shown below 
|_ venv
    |_Include
    |_Scripts
    |_Libs
    |_pyvenv.cfg
1. Delete the following things -> Scripts and pyvenv.cfg
2. Recreate the venv environment as mention in the previous steps
3. Rerun step 1 to 4 , step 5 which is the flask run should work now
```
4. Run with Docker
```sh
1. For hosting locally, the lines with comments within nginx/conf/default.conf need to be changed
2. For issues with the database, remove mysql/database_data and start the dockers again to reset the database
3. .env files should exist in the flask and mysql folders
4. Run with either build.sh or using docker-compose.yml
    - ./build.sh
    - docker-compose up -d
```


<h1>Automated Testing Checklist</h1>

```sh

1. Choice of Automated Testing: Unit Testing , Integration Testing and Selenium Testing

2. Checklist:
Unit Testing
-[x] Login
    - Test login passed credential
    - Test login failed password credential
    - Test login failed username credential
    - Test login failed both credential
-[x] Update of profile
    - Test successfully update user profile
    - Test successfully insert new announcement
-[x] Validation Input
    - Number Validation
    - Text Validation
    - Email Validation
    - Symbols Validation
    - Password Hash Validation
Selenium Testing
-[x] Login
-[x] Logout
```
