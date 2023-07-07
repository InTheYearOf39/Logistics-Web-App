
# Lastmile.pudonet.net

___


<h2>Preview of <a href="https://lastmile.pudonet.net">lastmile.pudonet.net</a> Web App<h2>

![Alt lastmile.pudonet.net web App screenshot](Logistics-Web-App\django_project\static\img\face.png)
_Visit [lastmile.pudonet.net](https://lastmile.pudonet.net) to learn more!_

## What is lastmile.pudonet.net?

Lastmile.pudonet.net is a Third-Party Logistics Management web-based application built to facilitate the process of tracking and managing of packages from one location to a set destination.

<div>&nbsp;</div>


## Contributing to the lastmile.pudonet.net Web Application

In the following steps, you will setup your development environment, fork and clone the repository, run the site locally, and finally commit, sign off, and push any changes made for review.

### 1. Set up your development environment

- _The Lastmile App is built using `Django` - Django is a powerful and versatile `Python` web framework that enables efficient development of robust and feature-rich web applications! You can learn more about Django and setting up your development environment in the [Django Docs](https://docs.djangoproject.com/en/4.2/)._    


- First [Download Python](https://www.python.org/downloads/), Select a download type that is compatible with the machine you're working on (`Windows`, `Linux/UNIX`, `macOS`). Select any python version that falls within the python `3.10` bracket as we shall be using that throughout this project.

### 2. Get the code

- Fork and then clone the [Logistics-Web-App repository](https://github.com/InTheYearOf39/Logistics-Web-App)
  ```bash
  $ git clone https://github.com/YOUR-USERNAME/Logistics-Web-App
  ```
- cd into project using
  ```bash
  $ cd Logistics-Web-App/django-project
  ```
- create a virtual environment to store all your project dependencies
  ```bash
  $ pip install virtualenv    
  $ virtualenv -p python3.10 'environment name goes here without the quotations'   
  ```
  __Note__: We specified `python10` because it is what we have have installed and setup for this  project.   

   
  
- Install all project dependencies
  ```bash
  $ pip install -r requirements.txt
  ```
    
  __Note__: This command will install all the dependencies as listed in the requirements.txt file and any new dependencies installed should be updated in this file

### 3. Serve the site

- Serve the code locally
  ```bash
  $ py manage.py runserver
  ```
  _Note: This command should spin up a development server running locally at `http://127.0.0.1:8000/` or `http://localhost:8000/`

### 4. Create a Pull Request

- Create a branch where you'll be making a change or building a feature. After making changes, stage the changes to the file and commit them.   
To stage the changes:
  ```bash
  $ git add <relative path to file>
  ```
  or add all changes by running    
  ```bash
  $ git add .
  ```
  Then to commit them:   
  ```bash
  
  $ git commit -m “my commit message”
  ```
- Once all changes have been committed, push the changes.
  ```bash
  $ git push origin <branch-name>
  ```
- Then on Github, navigate to the [Logistics-Web-App repository](https://github.com/InTheYearOf39/Logistics-Web-App) and create a pull request from your recently pushed changes!

                                                                                                   
