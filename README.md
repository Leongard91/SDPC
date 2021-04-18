# SDPC
### Description:

"Steel door price calculator"(or SDPC) is an application for calculating door price costs for clients based on real door company information.

SDPC is a web-based application using JavaScript, Python, and SQLite. It is an interactive program for working with door catalogs. Using this app You can:
- Make fast calculations based on information from a database.
- Print out a ready offer for the client.
- Get and print out earlier made calculations.
- Insert new information into the door catalogs.
- Create database users (customers).

The application can be used by store personal or can be embedded in the main door company URL page. In the second case, customers will be able to choose all necessary parameters by themselves and get an actual price offer on chosen door. As result, the buyer no longer needs to visit the store.


### Installation:
1. Download and install [Python](https://www.python.org/downloads/).
2. Unzip "SDPC.zip" file to the working folder.
3. Install all necessary Python libraries from "requirements.txt" using links to instruction for the ich module.

```bash
1. Flask (https://flask.palletsprojects.com/en/1.1.x/installation/);
2. Flask-Session (https://pypi.org/project/Flask-Session/);
3. requests (https://pypi.org/project/requests/);
4. werkzeug (https://pypi.org/project/Werkzeug/);
5. pywin32 (https://pypi.org/project/pywin32/);
6. openpyxl (https://pypi.org/project/openpyxl/);
7. functools (https://pypi.org/project/functools/);
8. Pillow (https://pypi.org/project/Pillow/);
```

### Usage:

1. Open "SDPC" folder in the terminal by following commands:
```
1) cd (path to saved SDPC folder)
2) cd SDPC
```
2. Start Flask and further to the received link. In the command line:
```
python -m flask run
```
3. Register in the application and log in.
4. If You want to open the application with full functionality, should log in like an administrator.
```
Username: Admin
Password: 11111111
```
Database information based on [STRAJ](straj.ua) company page.
 
Enjoy!
