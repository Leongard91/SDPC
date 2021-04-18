import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, send_from_directory, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from PIL import Image

from helpers import apology, login_required, render_xlsx, render_pdf

# paramenters for uploading images to static
UPLOAD_FOLDER = os.getcwd() + '/static/img/'
ALLOWED_EXTENSIONS = {'png', 'jpg'}

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded and open upload folder
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# function for ansure that file have allowed extention function
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

user_rights = ""

g_bought = 0
g_sell = 0
g_success = 0

@app.route("/")
@login_required
def index():
    # render start page
    return render_template("index.html")


@app.route("/calculate", methods=["GET", "POST"])
@login_required
def calculate():
    if request.method == "POST":
        con = sqlite3.connect('db.sqlite')
        db = con.cursor()
        install_date = str(date.today() + timedelta(days=31))
        
        # check all parameters complete
        if not request.form.get("door_type") or not request.form.get("size") or not request.form.get("open_side") or not request.form.get("handle_color") \
            or not request.form.get("frame_and_hinge_color") or not request.form.get("quarter_color") or not request.form.get("decor_color")\
                 or not request.form.get("outside_model") or not request.form.get("outside_cover")\
                    or not request.form.get("inside_model") or not request.form.get("inside_cover") or not request.form.get("latch"): 
            return apology("calculate.html", "must provide all parameters", 400)

        # create and insert order number
        o = db.execute("SELECT COUNT(id) FROM ord_numbs WHERE date = ?", (date.today(),)).fetchone()[0]
        if o == 0: o = 1
        else: o += 1
        ord_numb = "{:%d%m}".format(datetime.now()) + str(o)
        db.execute("INSERT INTO ord_numbs(number, date_time, date) VALUES(?, DATETIME('now'), ?)", (ord_numb, date.today()))

        # get posted parameters from calculate.html
        from_ord_numbs = db.execute('SELECT number FROM ord_numbs WHERE date_time=(SELECT MAX(date_time) FROM ord_numbs)').fetchone()[0]
        from_door_tipes = request.form.get("door_type")
        from_st_size = str(request.form.get("size"))
        from_open_sides = str(request.form.get("open_side"))
        from_handle_colors = str(request.form.get("handle_color"))
        from_paint_colors_frame_color = str(request.form.get("frame_and_hinge_color"))
        from_paint_colors_quoter_color = str(request.form.get("quarter_color"))
        from_covers_decor_color = str(request.form.get("decor_color"))
        from_models_out_side_model = str(request.form.get("outside_model"))
        from_covers_out_side_cover = str(request.form.get("outside_cover"))
        from_models_in_side_model = str(request.form.get("inside_model"))
        from_covers_in_side_cover = str(request.form.get("inside_cover"))
        from_latches = str(request.form.get("latch"))

        # create static varibles
        if "SECUREMME" in from_door_tipes:
            from_up_locks = "SECUREMME 2019 5K"
            from_strips_up_lock_strip = "---"
            from_main_locks = "SECUREMME"
        elif "MOTTURA" in from_door_tipes:
            from_up_locks = "MOTTURA DP58-170"
            from_strips_up_lock_strip = "SECUREMME"
            from_main_locks = "MOTTURA DP58-171"
        else:
            return apology("calculate.html", "Error", 400)
        from_strips_main_lock_strip = "SECUREMME"
        from_handles = "RDA FORME Q SQ. CHROME"
        from_lock_cylinders = "SECUREMME 3101QCS"
        from_peepholes = "SECUREME"
        
        # price calculating
        price_t = (db.execute("SELECT price FROM door_tipes WHERE tipe = ?", (from_door_tipes,)).fetchone()[0],
                db.execute("SELECT price FROM latches WHERE latch = ?", (from_latches,)).fetchone()[0],
                db.execute("SELECT price FROM covers WHERE color = ?", (from_covers_out_side_cover,)).fetchone()[0],
                db.execute("SELECT price FROM models WHERE model = ?", (from_models_out_side_model,)).fetchone()[0],
                db.execute("SELECT price FROM covers WHERE color = ?", (from_covers_in_side_cover,)).fetchone()[0],
                db.execute("SELECT price FROM models WHERE model = ?", (from_models_in_side_model,)).fetchone()[0])
        price = sum(price_t)
        if request.form.get("installing") == "Yes": installing = 40
        else: installing = 0
        if request.form.get("deinstalling") == "Yes": deinstalling = 4
        else: deinstalling = 0
        service_cost = deinstalling + installing
        total_price = service_cost + price

        # insert all data to user's table
        db.execute(f'''INSERT INTO {session['user_id']}(date, install_date, from_ord_numbs, from_door_tipes, from_st_size, from_open_sides, from_handle_colors, 
        from_paint_colors_frame_color, from_paint_colors_quoter_color, from_covers_decor_color, from_models_out_side_model, from_covers_out_side_cover,  
        from_models_in_side_model, from_covers_in_side_cover, from_up_locks, from_strips_up_lock_strip,from_main_locks, from_strips_main_lock_strip, 
        from_handles, from_lock_cylinders, from_peepholes, from_latches, price, deinstalling, installing, service_cost, total_price) VALUES(DATETIME('now'), ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);''',
        (install_date, from_ord_numbs, from_door_tipes, from_st_size, from_open_sides, from_handle_colors, from_paint_colors_frame_color,\
        from_paint_colors_quoter_color,from_covers_decor_color, from_models_out_side_model, from_covers_out_side_cover, from_models_in_side_model,\
        from_covers_in_side_cover, from_up_locks, from_strips_up_lock_strip, from_main_locks, from_strips_main_lock_strip, from_handles, from_lock_cylinders, \
        from_peepholes, from_latches, price, deinstalling, installing, service_cost, total_price))
        con.commit()
        con.close()

        # create new pdf file in calculation's archive
        con = sqlite3.connect('db.sqlite')
        con.row_factory = sqlite3.Row
        db = con.cursor()
        db.execute(f'SELECT * FROM {session["user_id"]} WHERE date=(SELECT MAX(date) FROM {session["user_id"]})')
        r = db.fetchone()
        e=0
        rows = {}
        for i in r:
            rows[r.keys()[e]] = i
            e+=1
        con.commit()
        con.close()
        render_xlsx(rows, price_t)
        render_pdf(from_ord_numbs)

        # render calculation result page 
        return render_template("calculated.html", rows=rows, price_t=price_t)

    else:
        con = sqlite3.connect('db.sqlite')
        db = con.cursor()
        db.execute('SELECT side FROM open_sides')
        open_sides = db.fetchall()
        db.execute('SELECT color FROM handle_colors')
        handle_colors = db.fetchall()
        paint_colors = db.execute('SELECT color FROM paint_colors').fetchall()
        models = db.execute('SELECT model FROM models').fetchall()
        covers = db.execute('SELECT color FROM covers').fetchall()
        sizes = db.execute('SELECT size FROM st_size').fetchall()
        door_types = db.execute('SELECT tipe FROM door_tipes').fetchall()
        yes_no = db.execute('SELECT y_n FROM yes_no').fetchall()
        latches = db.execute('SELECT latch FROM latches').fetchall()
        con.commit()
        con.close()
        return render_template("calculate.html", open_sides=open_sides, handle_colors=handle_colors, paint_colors=paint_colors,
                                models=models, covers=covers, sizes=sizes, door_types=door_types, yes_no=yes_no, latches=latches)


@app.route("/history")
@login_required
def history():

    # get all rows from user's table (calculation's history)
    con = sqlite3.connect('db.sqlite')
    con.row_factory = sqlite3.Row
    db = con.cursor()
    db.execute(f'SELECT * FROM {session["user_id"]} ORDER BY id DESC')
    rows_objects = db.fetchall()

    # make list of dictionaries for rendering
    rows = []
    for rows_object in rows_objects:
        e=0
        row = {}
        for i in rows_object:
            row[rows_object.keys()[e]] = i
            e+=1
        rows.append(row)
    con.commit()
    con.close()
    return render_template("/history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("login.html", "must provide username", 403)

        # Ensure user dont try to drop db
        if ("(" in request.form.get("username") or ";" in request.form.get("username") or "," in request.form.get("username")):
            return apology("register.html", "dont try to drop my db", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("login.html", "must provide password", 403)

        # Query database for username
        con = sqlite3.connect('db.sqlite')
        db = con.cursor()
        db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = db.fetchone()

        # Ensure username exists and password is correct
        if rows == None or not check_password_hash(rows[2], request.form.get("password")):
            return apology("login.html", "invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[1]
        global user_rights
        user_rights = rows[3]
        con.commit()
        con.close()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        global g_success
        if g_success > 0:
            g_success = 0
            success = True
        else:
            success = False
        return render_template("/login.html", success=success)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id and user_rights
    session.clear()
    global user_rights
    user_rights = ""

    # Redirect user to login form
    return redirect("/")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("change.html", "must provide username", 400)

        # Ensure that user exists
        con = sqlite3.connect('db.sqlite')
        db = con.cursor()
        db.execute("SELECT username FROM users WHERE username = ?", (request.form.get("username"),))
        if db.fetchone()[0] == None:
            return apology("change.html", "user not exists", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("change.html", "must provide password", 400)

        # Ensure username exists and password is correct
        db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = db.fetchone()
        if rows == None or not check_password_hash(rows[2], request.form.get("password")):
            return apology("change.html", "invalid username and/or password", 400)

        # Ensure password was submitted
        if not request.form.get("new_password"):
            return apology("change.html", "must provide new_password", 400)

        # Ensure new_password was submitted by 8 symbol
        if len(request.form.get("new_password")) != 8:
            return apology("change.html", "must provide 8 symbol password", 400)

        # Ensure confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("change.html", "must repeat password", 400)

        # Ensure password is a same as repeat_password
        if request.form.get("new_password") != request.form.get("confirmation"):
            return apology("change.html", "passwords do not matchs", 400)

        # Insert data to the database
        db.execute("UPDATE users SET hash = ? WHERE username = ?", (generate_password_hash(
            request.form.get("new_password"), method='pbkdf2:sha256', salt_length=8), request.form.get("username")))
        con.commit()
        con.close()

        # Redirect user to login
        global g_success
        g_success += 1
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("register.html", "must provide username", 400)

        # Ensure user dont try to drop db
        if ("(" in request.form.get("username") or ";" in request.form.get("username") or "," in request.form.get("username")):
            return apology("register.html", "dont try to drop my db", 400)

        # Ensure that new user
        try:
            con = sqlite3.connect('db.sqlite')
            db = con.cursor()
            db.execute("SELECT username FROM users WHERE username = ?", (request.form.get("username"),))
            if db.fetchone()[0] == request.form.get("username"):
                return apology("register.html", "user already exists, please log in", 400)
            con.commit()
            con.close()
        except:
            pass

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("register.html", "must provide password", 400)

        # Ensure password was submitted by 8 symbol
        if len(request.form.get("password")) != 8:
            return apology("register.html", "must provide 8 symbol password", 400)

        # Ensure confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("register.html", "must repeat password", 400)

        # Ensure password is a same as repeat_password
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("register.html", "passwords do not matchs", 400)

        # Insert data to the database
        con = sqlite3.connect('db.sqlite')
        db = con.cursor()
        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", (request.form.get("username"), generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)))
        db.execute("SELECT username FROM users WHERE username = ?", (request.form.get("username"),))
        row = db.fetchone()[0]
        id = row
        db.execute(f'''CREATE TABLE {id}(id INTEGER PRIMARY KEY, date DATETIME, install_date TEXT, from_ord_numbs TEXT,
                    from_door_tipes TEXT, from_st_size TEXT, from_open_sides TEXT, from_handle_colors TEXT, from_paint_colors_frame_color TEXT, from_paint_colors_quoter_color TEXT, 
                    from_covers_decor_color TEXT, from_models_out_side_model TEXT, from_covers_out_side_cover TEXT,  from_models_in_side_model TEXT, from_covers_in_side_cover TEXT, from_up_locks TEXT, from_strips_up_lock_strip TEXT,
                    from_main_locks TEXT, from_strips_main_lock_strip TEXT, from_handles TEXT, from_lock_cylinders TEXT, from_peepholes TEXT, from_latches TEXT, price NUMERIC, deinstalling NUMERIC, installing NUMERIC, service_cost NUMERIC, total_price NUMERIC)''')
        con.commit()
        con.close()

        # enable success message for login page
        global g_success
        g_success += 1

        # Redirect user to login
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("/register.html")


@app.route("/print", methods=["POST"])
@login_required
def print():
    # print out calculation result
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir + '/static/pdf_arch/'
    pdf_name = request.form.get("print") + '.pdf'
    return send_from_directory(filepath, pdf_name)


@app.route("/insert", methods=["GET", "POST"])
@login_required
def insert():
    # check administrator rights
    global user_rights
    if user_rights != "A" :
        return apology("index.html", "Administrator rights required!", 400)
    
    if request.method == "POST":

        # check providing t_name and value
        if not request.form.get("t_name") or not request.form.get("value"): 
            return apology("insert.html", 'must provide "Characteristics" and "New Value Name"', 400)

        # get t_name and value
        table_name = request.form.get("t_name")
        new_value = request.form.get("value").upper().strip()

        # get img if t_name = 'models'
        if 'file' in request.files:
            file = request.files['file']
            # check 'file selected'
            if file.filename == '':
                return apology("insert.html", 'No selected file', 400)

            # check required format
            if file and allowed_file(file.filename):
                if ".png" in file.filename:
                    filename = new_value + ".png"
                    filename = secure_filename(filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                elif ".jpg" in file.filename:
                    # convert to png
                    filename = secure_filename(file.filename)
                    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(img_path)
                    im = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                    rgb_im = im.convert('RGB')
                    rgb_im.save(os.path.join(app.config['UPLOAD_FOLDER'], new_value + '.png'))
                    os.remove(img_path)
            else: return apology("insert.html", 'Only .png and .jpg files are allowed', 400)

        # insert new data to the db
        con = sqlite3.connect('db.sqlite')
        db = con.cursor()
        db.execute(f"SELECT * FROM {table_name}")
        col_names = tuple(list(map(lambda x: x[0], db.description)))
        if len(col_names) < 3:
            db.execute(f"INSERT OR REPLACE INTO {table_name}{col_names} VALUES((SELECT id FROM {table_name} WHERE {col_names[1]} = ?),?)", (new_value, new_value))
        else:
            new_price = request.form.get("price")
            db.execute(f"INSERT OR REPLACE INTO {table_name}{col_names} VALUES((SELECT id FROM {table_name} WHERE {col_names[1]} = ?),?, ?)", (new_value, new_value, new_price))
        con.commit()
        con.close()

        # success message
        global g_success
        g_success += 1
        if g_success > 0:
            g_success = 0
            success = True
        else:
            success = False
        return render_template("insert.html", success=success)

    else:
        # make list of table names for selection
        con = sqlite3.connect('db.sqlite')
        db = con.cursor()
        t_names = db.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        con.commit()
        con.close()
        return render_template("insert.html", t_names=t_names[1:16])


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology("login.html", e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

