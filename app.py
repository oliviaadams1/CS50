import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # transactions = db.execute("SELECT * FROM transactions WHERE user_id=:id", id=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id=:id",
                      id=session["user_id"])
    cash = cash[0]['cash']
    sum = cash

    # Select what stocks the user owns from db
    stocks = db.execute(
        "SELECT stock, shares, name FROM transactions WHERE user_id=:id", id=session["user_id"])

    # For each stock the user owns
    for stock in stocks:
        symbol = stock["stock"]
        quote = lookup(symbol)

        # Lookup the current price of the stock
        stock["price"] = quote["price"]

        # Find the total price of the shares of the stock the user owns
        stock["total"] = stock["price"] * stock["shares"]

        # User's total of cash and investments
        sum += stock["total"]

        # Convert prices into USD
        stock["price"] = usd(stock["price"])
        stock["total"] = usd(stock["total"])

    # print("price for", stock["stock"], "is", stock["price"], "total for", stock["shares"], "is", stock["total"])
    # Return after all iterations
    return render_template("index.html", stocks=stocks, cash=cash, sum=sum)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        # if no symbol entered
        if not request.form.get("symbol"):
            return apology("Please enter stock symbol", 400)

         # If stock name does not exist
        elif lookup(request.form.get("symbol")) == None:
            return apology("must provide legitimate stock symbol", 400)

        # if no shares entered
        elif not request.form.get("shares"):
            return apology("Please enter number of shares", 400)

        else:
            # Get user's balance
            cash = db.execute(
                "SELECT cash FROM users WHERE id =:id", id=session["user_id"])
            cash = cash[0]['cash']

            # look up stock name and price
            stock = lookup(request.form.get("symbol"))
            price = stock["price"]
            symbol = stock["symbol"]
            name = stock["name"]

            # Get number of shares from user input

            try:
                if int(request.form.get("shares")) <= 0:
                    return apology("Invalid number of shares", 400)
            except ValueError:
                return apology("Invalid number of shares", 400)

            shares = int(request.form.get("shares"))

            # Calculate purchase cost and remainder after purchase
            purchase = price * shares
            remainder = cash - purchase

            # if not enough money
            if remainder < 0:
                return apology("Insufficient Funds", 400)

            # Check if the user ownes shares of this stock
            row = db.execute("SELECT * FROM transactions WHERE user_id =:id and stock=:symbol",
                             id=session["user_id"], symbol=symbol)

            # If the user does not own shares of this stock
            if len(row) != 1:
                # Log the transaction, set the cash, and add the transaction into user history
                db.execute("INSERT INTO transactions (user_id, stock, name, shares, price, time) VALUES(:id, :symbol, :name, :shares, :price, :time)",
                           id=session["user_id"], symbol=symbol, name=name, shares=shares, price=price, time=(datetime.now()))
                db.execute("UPDATE users SET cash = :remainder WHERE id = :id",
                           id=session["user_id"], remainder=remainder)
                db.execute("INSERT INTO history (user_id, stock, name, shares, price, time) VALUES(:id, :symbol, :name, :shares, :price, :time)",
                           id=session["user_id"], symbol=symbol, name=name, shares=shares, price=price, time=(datetime.now()))
                flash("Bought!")
                return redirect("/")

            # if the user does own shares of this stock
            else:
                # Get the previous number of shares
                prevshares = row
                prevshares = prevshares[0]["shares"]
                # Add shares the user is currently buying to the shares the user already has
                totshares = prevshares + shares

                # Update the total shares in the db, update the user's cash, and log the transaction in history
                db.execute("UPDATE transactions SET shares=:totshares WHERE user_id=:id and stock=:symbol",
                           totshares=totshares, id=session["user_id"], symbol=symbol)
                db.execute("UPDATE users SET cash = :remainder WHERE id = :id",
                           id=session["user_id"], remainder=remainder)
                db.execute("INSERT INTO history (user_id, stock, name, shares, price, time) VALUES(:id, :symbol, :name, :shares, :price, :time)",
                           id=session["user_id"], symbol=symbol, name=name, shares=shares, price=price, time=(datetime.now()))
                return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Select symbol, name, shares, price, and time from db
    stocks = db.execute(
        "SELECT * FROM history WHERE user_id=:id", id=session["user_id"])

    # Return after all iterations
    return render_template("history.html", stocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # if no stock was entered
        if not request.form.get("symbol"):
            return apology("must provide stock to quote", 400)

        # If stock name does not exist
        if lookup(request.form.get("symbol")) == None:
            return apology("must provide legitimate stock symbol", 400)

        else:
            # Render stock name, price, and symbol
            quote = lookup(request.form.get("symbol"))
            return render_template("quoted.html", quote=quote)

    else:
        # If request method is get
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

          # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

          # Ensure password was submitted
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Ensure that there is no user with same username
        elif len(rows) != 0:
            return apology("username already used", 400)

        # If everything is okay, allow the user to register, store username and hash of password in DB
        else:
            hash = generate_password_hash(request.form.get("password"))
            username = request.form.get("username")
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            # Keep user signed in
            row = db.execute(
                "SELECT id FROM users WHERE username =?", request.form.get("username"))
            session["user_id"] = row[0]["id"]
            # Tell the user they have registered
            flash("Registered!")

            # Redirect user to home page
            return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        # if no symbol entered
        if not request.form.get("symbol"):
            return apology("Please enter stock symbol", 400)

        # if no shares entered
        elif not request.form.get("shares"):
            return apology("Please enter number of shares", 400)

        else:
            # Get user's balance
            cash = db.execute(
                "SELECT cash FROM users WHERE id =:id", id=session["user_id"])
            cash = cash[0]['cash']

            # look up stock name and price
            stock = request.form.get("symbol")
            quote = lookup(stock)

            price = quote["price"]
            symbol = quote["symbol"]
            name = quote["name"]

            # Get number of shares from user input
            shares = request.form.get("shares")
            shares = int(shares)

            # Calculate purchase cost and remainder after purchase
            purchase = price * shares
            remainder = cash + purchase

            # Check if the user owns shares of this stock
            row = db.execute("SELECT * FROM transactions WHERE user_id =:id and stock=:symbol",
                             id=session["user_id"], symbol=symbol)

            # If the user does not own shares of this stock
            if len(row) != 1:
                return apology("You do not currently own shares of this stock", 400)

            # if the user does own shares of this stock
            else:
                # Get the previous number of shares
                prevshares = row
                prevshares = prevshares[0]["shares"]

                if shares > prevshares:
                    return apology("You do not own that many shares of this stock", 400)
                # Subtract shares the user is currently selling from the shares the user already has
                totshares = prevshares - shares

                # Update the total shares in the db, update the user's cash, and log the transaction in history
                db.execute("UPDATE transactions SET shares=:totshares WHERE user_id=:id and stock=:symbol",
                           totshares=totshares, id=session["user_id"], symbol=symbol)

                if totshares < 0:
                    db.execute("DELETE FROM transactions WHERE user_id=:id AND stock=:stock",
                               id=session["user_id"], stock=stock)

        db.execute("UPDATE users SET cash = :remainder WHERE id = :id",
                   id=session["user_id"], remainder=remainder)
        db.execute("INSERT INTO history (user_id, stock, name, shares, price, time) VALUES(:id, :symbol, :name, :shares, :price, :time)",
                   id=session["user_id"], symbol=symbol, name=name, shares=shares, price=price, time=(datetime.now()))
        flash("Sold!")
        return redirect("/")

    else:
        stocks = db.execute(
            "SELECT stock, shares FROM transactions WHERE user_id=:id", id=session["user_id"])
        return render_template("sell.html", stocks=stocks)
