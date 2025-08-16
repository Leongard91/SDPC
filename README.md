# SDPC

### Description:

"Steel door price calculator"(or SDPC) is an application for calculating door price costs for clients based on real door company information.

SDPC is a web-based application using JavaScript, Python, and SQLite. It is an interactive program for working with door catalogs. Using this app You can:
- Make fast calculations based on information from a database.
- Print out a ready offer for the client.
- Get and print out earlier made calculations.
- Insert new information into the door catalogs.
- Create a database of users (customers).

The application can be used by store personal or can be embedded in the main door company URL page. In the second case, customers will be able to choose all necessary parameters by themselves and get an actual price offer on chosen door. As result, the buyer no longer needs to visit the store.


### Installation:
1. Download and install [Python](https://www.python.org/downloads/).
2. Unzip the "SDPC.zip" file to the working folder.
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
In this application, You no need to import CS50's library and features.

### Easy Start:
At the moment application doesn't upload to the server. So You need to start it using the Flask command.

1. Open the "SDPC" folder in the terminal by following commands:
```
1) $ cd (path to saved SDPC folder)
2) $ cd SDPC
```
2. Start Flask. In the command line type:
```
$ python -m flask run
```
3. Further to the received link.

### Design:
For the main layout was used "finance" application design from CS50's "problem set 9".
It has a very useful form and universal blocks, which can be screened on most devices.

### Usage:
#### Log in page:
The first page, which You will see, will be "Log in" page.

![alt text](https://raw.githubusercontent.com/Leongard91/SDPC/0c04ca0a6cfee9c9c40684e18f3c1afb07cb3903/screenshots/Login.JPG)

You have no user account yet, so you need to click on `Regisrer` in the header of the page, and pass registration. Once all necessary information becomes filled, application updates the "users" table in the database and create a new special table for registered user, into which will be inserted its calculation history.

After registration, You will be redirected to the "Log in" page.
Enter your username/password and click the `Log in` button!

#### Main page:
If successfully logged in, You will be redirected to the "main" page.

![alt text](https://raw.githubusercontent.com/Leongard91/SDPC/0c04ca0a6cfee9c9c40684e18f3c1afb07cb3903/screenshots/main.JPG)
On the main page, You will see a welcome message and `CALCULATE` button, as buttons in the header of the page. Click `CALCULATE` to start!

#### Calculate page:
After clicking 'CALCULATE' bottom, You will see the next page:

![alt text](https://raw.githubusercontent.com/Leongard91/SDPC/0c04ca0a6cfee9c9c40684e18f3c1afb07cb3903/screenshots/Calculate.JPG)

On this page, You should choose all options for your new door. Options of selections got directly from the database, so don't try to change It here. JavaScript code makes this page more interactive, so You can see all parameters and doors view before as `Calculate` button will be pushed.
Click 'Calculate'!

When 'Calculate' pressed, the application automatically make the next operations: 
1. Creates an order number and estimated installation date.
2. Calculate door price based on chosen parameters and database price information. 
3. Updates the user's history table.
4. Fills prepared '.xlsx' form.
5. Creates offer's pdf file from this '.xlsx' form and saves it in the pdf-archive folder
6. Redirect You to the "Calculated" page, where You could see chosen parameters, calculated price, and "Print" button. 

![alt text](https://raw.githubusercontent.com/Leongard91/SDPC/main/screenshots/calculated2.JPG)

Once click "Print", the application gets created earlier file from pdf-archive, which You can print out or save to your device.

### History page:
If click on the "History" in the header, You will see next:

![alt text](https://raw.githubusercontent.com/Leongard91/SDPC/main/screenshots/History.JPG)

This page shows your offer history from the database history table.
Click on the highlighted offer number to get pdf file from the pdf-archive folder.

### Insert New page:
Although, You can insert new information into the doors catalogs. 
For this operation, You have to Log Out and Log in like 'Adminitraror':
```
Username: Admin
Password: 11111111
```
Then, if click on the 'Insert New' in the page header, returns back next page:

![alt text](https://raw.githubusercontent.com/Leongard91/SDPC/main/screenshots/Insert.JPG)

Here You can choose the catalog, what You want to update, and enter all necessary information. Using JavaScipt code, the page shows You can be updated inputs only. 

Into some catalogs, You can insert positions title, price, and even upload images.
Application takes an image in '.png' format, rename and save it in '/static/img' folder.
You don't have png? Try '.jpg' format! The application automatically converts the jpg to png and does some operations.

### Access:
The "SDPC" application is opened for anybody and available on my GitHub page: [Leongard91/SDPC](https://github.com/Leongard91/SDPC)

Database information based on [STRAJ](straj.ua) company page.

Enjoy!
