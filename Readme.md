
# Authentication Management System


This Django based authentication management system has the following functionalities:

   * #### Register users  
   * #### Activate the newly registered user account through an email   
   * #### Login users after their account has been activated successfully

The system is build using **Django 4**, **Python 3.11**, **Bootstrap 5** and **HTML 5**.

![image](https://github.com/YordanovaT/AuthenticationApp/assets/109622871/3ff17568-a5a5-40d7-8ccd-fc214453d248)

## Table of contents
*  [Installation](#Installation)  
* [Running the application](#Running-the-application)  
* [View the application](#View-the-application)

### [Installation](#Installation) 

**1. Create virtual environment**  
*From the **root** directory run:*

      python -m venv venv  

**2. Activate the environment**  
*On MacOS:* 

    source venv/bin/activate
*On Windows :*  

    venv\scripts\activate

**3. Install required dependencies**  
*From the **root** directory run:* 

    pip install -r requirements.txt

**4. Run migrations**  
*From the **root** directory run:*  

    python manage.py makemigrations

*Then run:*  

    python manage.py migrate

**5. Create Django admin user in order to have access to the Django Admin Panel:**  
*From the **root** directory run:*  

    python manage.py createsuperuser

*When prompted, enter username, email and password.*  

### [Running the application](#Running-the-application)  

*From the **root** directory run:*  

    python manage.py runserver

### [View the application](#View-the-application)  

*Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)*  
  

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
