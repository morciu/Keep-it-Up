from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from cs50 import SQL
from functools import wraps

from werkzeug.security import check_password_hash, generate_password_hash



# Configure application
app = Flask(__name__)

# Session secret key
app.secret_key = "butts"

#Set up database
db = SQL("sqlite:////home/morciu/mysite/Keep it up/days.db")

# Return error page
def error():
    return render_template("error.html")


# Decorator function to require the user to be logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
@login_required
def index():
    # Main page
    return render_template("index.html", username=session.get("username"))


@app.route("/login", methods=["GET", "POST"])
def login():
    # End any current sessions
    session.clear()

    # Login page
    if request.method == "POST":
        # Check if forms are filled in
        if not request.form.get("user") or not request.form.get("password"):
            return error()

        # Store username and password into variables
        username = request.form.get("user")
        password = request.form.get("password")

        # Check if username is in database
        user_search = db.execute("SELECT username FROM users WHERE username=:username;", username=username)
        if len(user_search) != 1:
            return error()

        # Check if password is correct
        password_search = db.execute("SELECT hash FROM users WHERE username=:username;", username=username)[0]['hash']
        if not check_password_hash(password_search, password):
            return error()

        # Start a session for this user
        user_id = db.execute("SELECT id FROM users WHERE username=:username;", username=username)[0]['id']
        session["user_id"] = user_id
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Register page
    if request.method == "POST":
        # Check if all fields are filled in
        if not request.form.get("user") or not request.form.get("password") or not request.form.get("reconfirm"):
            return error()

        # Check if password field is identical to reconfirm field
        elif request.form.get("password") != request.form.get("reconfirm"):
            return error()

        else:
            # Store username and password into variables
            username = request.form.get("user")
            password = generate_password_hash(request.form.get("password"))
            currency = request.form.get("currency")
            print(password)
            print(currency)

            # Check if username already exists in database
            user_search = db.execute("SELECT username FROM users WHERE username=:username;", username=username)
            if len(user_search) != 0:
                return error()

            # Update the user table
            db.execute("INSERT INTO 'users' ('username', 'hash', 'currency') VALUES (:username, :p_hash, :currency);", username=username, p_hash=password, currency=currency)

            return render_template("index.html")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    # Clear session data
    session.clear()

    return redirect("/")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    # Add tasks and stuff

    # Check if forms are filled in
    if request.method == "POST":
        if not request.form.get("task"):
            return error()
        if not request.form.get("start"):
            return error()
        if not request.form.get("deadline"):
            return error()

        # Store information in variables
        task_name = request.form.get("task")
        if request.form.get("description"):
            task_desc = request.form.get("description")
        start = request.form.get("start")
        deadline = request.form.get("deadline")

        # update database
        if request.form.get("description"):
            db.execute("INSERT INTO tasks ('user_id', 'name', 'description', 'start', 'deadline', 'completed') VALUES (:user_id, :name, :desc, :start, :end, 0);", user_id=session["user_id"], name=task_name, desc=task_desc, start=start, end=deadline)
        else:
            db.execute("INSERT INTO tasks ('user_id', 'name', 'description', 'start', 'deadline', 'completed') VALUES (:user_id, :name, NULL, :start, :end, 0);", user_id=session["user_id"], name=task_name, start=start, end=deadline)


        return redirect("/")

    else:
        return render_template("add.html")


@app.route("/add_warranty", methods=["GET", "POST"])
@login_required
def add_warranty():
    """Display a form to register warranties"""
    if request.method == "POST":
        # Check if all boxes are filled in
        if not request.form.get("product"):
            print("product")
            return error()
        if not request.form.get("store"):
            print("store")
            return error()
        if not request.form.get("receipt"):
            print("receipt")
            return error()
        if not request.form.get("start"):
            print("start")
            return error()
        if not request.form.get("end"):
            print("end")
            return error()
        if not request.form.get("price"):
            print("price")
            return error()

        # Store filled in information in variables
        user_id = session['user_id']
        print(user_id)
        product = request.form.get("product")
        print(product)
        store = request.form.get("store")
        print(store)
        if request.form.get("link"):
            link = request.form.get("link")
            print(link)
        price = request.form.get("price")
        print(price)
        receipt = request.form.get("receipt")
        print(receipt)
        start = request.form.get("start")
        print(start)
        end = request.form.get("end")
        print(end)


        # Update 'warranties' table
        if link:
            db.execute("INSERT INTO warranties ('user_id', 'product', 'store', 'link', 'price', 'receipt', 'start', 'end') VALUES (:user_id, :product, :store, :link, :price, :receipt, :start, :end);", user_id=user_id, product=product, store=store, link=link, price=price, receipt=receipt, start=start, end=end)
        else:
            db.execute("INSERT INTO warranties ('user_id', 'product', 'store', 'link', 'price', 'receipt', 'start', 'end') VALUES (:user_id, :product, :store, :price, :receipt, :start, :end);", user_id=user_id, product=product, store=store, price=price, receipt=receipt, start=start, end=end)

        return render_template("add_warranty.html")

    else:
        return render_template("add_warranty.html")

@app.route("/add_event", methods=["GET", "POST"])
@login_required
def add_event():
    '''Display a form that registers a new event'''
    if request.method == "POST":
        # Check if all forms are filled in
        if not request.form.get("event"):
            return error()
        if not request.form.get("date"):
            return error()

        # Set up variables for form info
        event = request.form.get("event")
        date = request.form.get("date")

        # Register new event in sql database 'events'
        if request.form.get("description"):
            db.execute("INSERT INTO 'events' ('user_id', 'event', 'description', 'date') VALUES (:user_id, :event, :description, :date);", user_id=session['user_id'], event=event, description=request.form.get("description"), date=date)
        else:
            db.execute("INSERT INTO 'events' ('user_id', 'event', 'description', 'date') VALUES (:user_id, :event, NULL, :date);", user_id=session['user_id'], event=event, date=date)

        # Refresh page
        return render_template("add_event.html")

    else:
        return render_template("add_event.html")


@app.route("/today", methods=["GET", "POST"])
@login_required
def today():
    ''' Display today's tasks '''
    # Query today's tasks
    rows = db.execute("SELECT * FROM tasks WHERE user_id=:user_id AND deadline >= date('now') AND start <= date('now');", user_id=session["user_id"])
    # Query today's expiring warranties
    warranties = db.execute("SELECT * FROM warranties WHERE user_id=:user_id AND end = date('now');", user_id=session["user_id"])
    # Get user currency
    user = db.execute("SELECT * FROM users WHERE id=:user_id;", user_id=session["user_id"])
    currency = user[0]['currency']
    # Query today's events
    events = db.execute("SELECT * FROM events WHERE user_id=:user_id AND date = date('now');", user_id=session['user_id'])
    # Query today's user input
    user_input = db.execute("SELECT * FROM 'daily_input' WHERE user_id=:user_id and date = date('now');", user_id=session['user_id'])


    if request.method == "POST":
        # Loop through today's tasks, find which task is clicked and if it's completed or not
        for i in range(1, len(rows)+1):
            if request.form.get(str(i)):
                # Get the database id nr for the selected item
                task_id = rows[i-1]['id']

                # Updated the 'completed' field in SQL
                if request.form[str(i)] == 'n':
                    db.execute("UPDATE tasks SET completed=1 WHERE id=:task_id;", task_id=task_id)
                elif request.form[str(i)] == 'y':
                    db.execute("UPDATE tasks SET completed=0 WHERE id=:task_id;", task_id=task_id)
                elif request.form[str(i)] == 'delete':
                    # Delete that entry from the database
                    db.execute("DELETE FROM tasks WHERE id=:task_id;", task_id=task_id)

                # Update 'rows' dictionary
                rows = db.execute("SELECT * FROM tasks WHERE user_id=:user_id AND deadline >= date('now') AND start <= date('now');", user_id=session["user_id"])

                # Update today's events
                events = db.execute("SELECT * FROM events WHERE user_id=:user_id AND date = date('now');", user_id=session['user_id'])

                # Refresh page
                return render_template("today.html", rows=rows, warranties=warranties, currency=currency, events=events, user_input=user_input)


        if request.form.get("earned") or request.form.get("spent"):
            if request.form.get("earned"):
                earned = request.form.get("earned")
            else:
                earned = 0
            if request.form.get("spent"):
                spent = request.form.get("spent")
            else:
                spent = 0
            rating = request.form.get("rating")

            # Update the 'daily_input' table with the info
            db.execute("INSERT INTO 'daily_input' (user_id, date, earned, spent, rating) VALUES (:user_id, date('now'), :earned, :spent, :rating);", user_id=session['user_id'], earned=earned, spent=spent, rating=rating)



        return render_template("today.html", rows=rows, warranties=warranties, currency=currency, events=events, user_input=user_input)
    else:
        return render_template("today.html", rows=rows, warranties=warranties, currency=currency, events=events, user_input=user_input)


@app.route("/this_week", methods=["GET", "POST"])
@login_required
def this_week():
    ''' Display this week's tasks '''
    # Query this week's tasks
    rows = db.execute("SELECT * FROM tasks WHERE user_id=:user_id AND (start >= date('now', 'weekday 0', '-6 days') AND start <= date('now', 'weekday 0')) OR (deadline >= date('now', 'weekday 0', '-6 days') AND deadline <= date('now', 'weekday 0'));", user_id=session["user_id"])
    # Query for expiring warranties this week
    warranties = db.execute("SELECT * FROM warranties WHERE user_id=:user_id AND end >= date('now', 'weekday 0', '-6 days') and end <= date('now', 'weekday 0');", user_id=session["user_id"])
    user = db.execute("SELECT * FROM users WHERE id=:user_id;", user_id=session["user_id"])
    currency = user[0]['currency']
    # Query this week's events
    events = db.execute("SELECT * FROM events WHERE user_id=:user_id AND date >= date('now', 'weekday 0', '-6 days') AND date <= date('now', 'weekday 0');", user_id=session['user_id'])
    # Query this week's user input
    user_input = db.execute("SELECT sum(earned), sum(spent), avg(rating) FROM daily_input WHERE user_id=:user_id AND date >= date('now', 'weekday 0', '-6 days') AND date <= date('now', 'weekday 0');", user_id=session['user_id'])
    print(user_input)
    print(user_input[0]['sum(earned)'])

    if request.method == "POST":
        # Loop through this week's, find which task is clicked and if it's completed or not
        for i in range(1, len(rows)+1):
            print(rows[i-1])
            if request.form.get(str(i)):
                task_id = rows[i-1]['id']
                print(request.form.get(str(i)))
                print(task_id)

                # Updated the 'completed' field in SQL
                if request.form[str(i)] == 'n':
                    db.execute("UPDATE tasks SET completed=1 WHERE id=:task_id;", task_id=task_id)
                elif request.form[str(i)] == 'y':
                    db.execute("UPDATE tasks SET completed=0 WHERE id=:task_id;", task_id=task_id)
                elif request.form[str(i)] == 'delete':
                    # Delete that entry from the database
                    db.execute("DELETE FROM tasks WHERE id=:task_id;", task_id=task_id)

                # Update 'rows' dictionary
                rows = db.execute("SELECT * FROM tasks WHERE user_id=:user_id AND (start >= date('now', 'weekday 0', '-6 days') AND start <= date('now', 'weekday 0')) OR (deadline >= date('now', 'weekday 0', '-6 days') AND deadline <= date('now', 'weekday 0'));", user_id=session["user_id"])

                # Update today's events
                events = db.execute("SELECT * FROM events WHERE user_id=:user_id AND date >= date('now', 'weekday 0', '-6 days') AND date <= date('now', 'weekday 0');", user_id=session['user_id'])

                # Refresh page
                return render_template("this_week.html", rows=rows, warranties=warranties, currency=currency, events=events, user_input=user_input)
                print("This week should render!")

    else:
        return render_template("this_week.html", rows=rows, warranties=warranties, currency=currency, events=events, user_input=user_input)


@app.route("/this_month", methods=["GET", "POST"])
@login_required
def this_month():
    ''' Display this week's tasks '''
    # Query this month's tasks
    rows = db.execute("SELECT * FROM tasks WHERE user_id=:user_id AND (start >= date('now', 'start of month') AND start <= date('now', 'start of month', '+1 month', '-1 day')) OR (deadline >= date('now', 'start of month') AND deadline <= date('now', 'start of month', '+1 month', '-1 day'));", user_id=session["user_id"])
    # Query for expiring warranties this month
    warranties = db.execute("SELECT * FROM warranties WHERE user_id=:user_id AND end >= date('now', 'start of month') and end <= date('now', 'start of month', '+1 month', '-1 day');", user_id=session["user_id"])
    user = db.execute("SELECT * FROM users WHERE id=:user_id;", user_id=session["user_id"])
    currency = user[0]['currency']
    # Query this month's events
    events = db.execute("SELECT * FROM events WHERE user_id=:user_id AND date >= date('now', 'start of month') and date <= date('now', 'start of month', '+1 month', '-1 day');", user_id=session['user_id'])
    # Query this month's user input
    user_input = db.execute("SELECT sum(earned), sum(spent), avg(rating) FROM daily_input WHERE user_id=:user_id AND date >= date('now', 'start of month') AND date <= date('now', 'start of month', '+1 month', '-1 day');", user_id=session['user_id'])

    if request.method == "POST":
        # Loop through this year's, find which task is clicked and if it's completed or not
        for i in range(1, len(rows)+1):
            if request.form.get(str(i)):
                task_id = rows[i-1]['id']

                # Updated the 'completed' field in SQL
                if request.form[str(i)] == 'n':
                    db.execute("UPDATE tasks SET completed=1 WHERE id=:task_id;", task_id=task_id)
                elif request.form[str(i)] == 'y':
                    db.execute("UPDATE tasks SET completed=0 WHERE id=:task_id;", task_id=task_id)
                elif request.form[str(i)] == 'delete':
                    # Delete that entry from the database
                    db.execute("DELETE FROM tasks WHERE id=:task_id;", task_id=task_id)

                # Update 'rows' dictionary
                rows = db.execute("SELECT * FROM tasks WHERE user_id=:user_id AND (start >= date('now', 'start of month') AND start <= date('now', 'start of month', '+1 month', '-1 day')) OR (deadline >= date('now', 'start of month') AND deadline <= date('now', 'start of month', '+1 month', '-1 day'));", user_id=session["user_id"])

                # Update today's events
                events = db.execute("SELECT * FROM events WHERE user_id=:user_id AND date >= date('now', 'start of month') and date <= date('now', 'start of month', '+1 month', '-1 day');", user_id=session['user_id'])

                # Refresh page
                return render_template("this_month.html", rows=rows, warranties=warranties, currency=currency, events=events, user_input=user_input)
    else:
        return render_template("this_month.html", rows=rows, warranties=warranties, currency=currency, events=events, user_input=user_input)


@app.route("/this_year", methods=["GET", "POST"])
@login_required
def this_year():
    ''' Display this week's tasks '''
    # Query this year's tasks
    rows = db.execute("SELECT * FROM tasks WHERE user_id=:user_id AND (start >= date('now', 'start of year') AND start <= date('now', 'start of year', '+12 months', '-1 day')) OR (deadline >= date('now', 'start of year') AND deadline <= date('now', 'start of year', '+12 months', '-1 day'));", user_id=session["user_id"])
    # Query for expiring warranties this month
    warranties = db.execute("SELECT * FROM warranties WHERE user_id=:user_id AND end >= date('now', 'start of year') and end <= date('now', 'start of year', '+12 months', '-1 day');", user_id=session["user_id"])
    user = db.execute("SELECT * FROM users WHERE id=:user_id;", user_id=session["user_id"])
    currency = user[0]['currency']
    # Query this year's events
    events = db.execute("SELECT * FROM events WHERE user_id=:user_id AND date >= date('now', 'start of year') and date <= date('now', 'start of year', '+12 months', '-1 day');", user_id=session['user_id'])
     # Query this year's user input
    user_input = db.execute("SELECT sum(earned), sum(spent), avg(rating) FROM daily_input WHERE user_id=:user_id AND date >= date('now', 'start of year') AND date <= date('now', 'start of year', '+12 months', '-1 day');", user_id=session['user_id'])


    if request.method == "POST":
        # Loop through this year's, find which task is clicked and if it's completed or not
        for i in range(1, len(rows)+1):
            if request.form.get(str(i)):
                task_id = rows[i-1]['id']

                # Updated the 'completed' field in SQL
                if request.form[str(i)] == 'n':
                    db.execute("UPDATE tasks SET completed=1 WHERE id=:task_id;", task_id=task_id)
                elif request.form[str(i)] == 'y':
                    db.execute("UPDATE tasks SET completed=0 WHERE id=:task_id;", task_id=task_id)
                elif request.form[str(i)] == 'delete':
                    # Delete that entry from the database
                    db.execute("DELETE FROM tasks WHERE id=:task_id;", task_id=task_id)

                # Update 'rows' dictionary
                rows = db.execute("SELECT * FROM tasks WHERE user_id=:user_id AND deadline >= date('now', 'start of year') AND deadline <= date('now', 'start of year', '+12 months', '-1 day');", user_id=session["user_id"])

                # Update today's events
                events = db.execute("SELECT * FROM events WHERE user_id=:user_id AND date >= date('now', 'start of year') and date <= date('now', 'start of year', '+12 months', '-1 day');", user_id=session['user_id'])

                # Refresh page
                return render_template("this_year.html", rows=rows, warranties=warranties, currency=currency, events=events, user_input=user_input)
    else:
        return render_template("this_year.html", rows=rows, warranties=warranties, currency=currency, events=events, user_input=user_input)


@app.route("/warranties")
@login_required
def warranties():
    '''Display all warranties'''
    warranties = db.execute("SELECT * FROM warranties WHERE user_id=:user_id;", user_id=session['user_id'])

    return render_template("warranties.html", warranties=warranties)