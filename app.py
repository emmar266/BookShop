from flask import Flask, render_template, redirect, request, g, session, url_for
from database import get_db, close_db
from forms import SearchForm ,SignIn, Review, SForm, SignUp, ChangeNameForm, BrowseForm, ChangePass, AddBook, UpdateInventory, EditReview, UserPic, ShippingInfo, PaymentDetails,ComplaintForm, ResponseForm
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_session import Session
import os
from flask_mail import Mail, Message
from datetime import datetime 
#####################################################################################################
#           - Access the admin side of the website with username admin and password 123
#           - I tried setting up an email sending thing but there was an issue with connecting to the
#             email server which wouldn't work. I left in the code because i'm pretty sure it's all correct
#           - I'm particularly proud of my addbook function (line 450 ish) which adds a book as well as uploads
#             a book cover. Also I have a complaints function which a user will write and is viewable to the 
#             admin and the admin can respond
#             
#######################################################################################################




UPLOAD_FOLDER = "static"
#UPLOAD_FOLDER = 'C:\\Users\\Emma1\\Documents\\2020-2021\\ca1\\static'

app = Flask(__name__)

app.config['MAIL_SERVER'] ='smtp.gmail.com'
app.config['MAIL_PORT'] =465
app.config['MAIL_USE_TLS'] =True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] ='bookshopmail217@gmail.com'
app.config['MAIL_PASSWORD'] ='uiqflygjspepvjto'
app.config['MAIL_DEFAULT_SENDER'] = None
app.config['MAIL_MAX_EMAILS'] = 4

app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'this-is-my-secret-key'
app.config['SESSION_PERMANENT']= False
app.config['SESSION_TYPE']= 'filesystem'
Session(app)
mail = Mail(app)
@app.teardown_appcontext
def close_db_at_end_of_requests(e=None):
    close_db(e)

@app.before_request
def load_logged_in_user():
    g.user=session.get('username', None)


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('signIn', next = request.url))
        return view(**kwargs)
    return wrapped_view

def admin_only(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user != 'admin':
            return redirect(url_for('signIn', next = request.url))
        return view(**kwargs)
    return wrapped_view

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/',methods=['GET','POST'])
def home ():
    form = SForm()
    message =''
    if form.validate_on_submit():
        book_name = form.book_name.data
        author_name = form.author_name.data
        db = get_db()
        if book_name !='' and author_name =='':
            if db.execute(''' SELECT * FROM books WHERE book_name=?; ''',(book_name,)).fetchone() is not None:
                books = db.execute(''' SELECT * FROM books WHERE book_name=?; ''',(book_name,)).fetchall()
                return render_template('books.html', books=books)
            else: 
                message = "We currently don't sell this book"
        elif book_name =='' and author_name !='': 
            if db.execute(''' SELECT * FROM authors WHERE author_name=?; ''',(author_name,)).fetchone() is not None:
                author_id = db.execute(''' SELECT * FROM authors WHERE author_name=?; ''',(author_name,)).fetchone()['author_id']
                books = db.execute(''' SELECT * FROM books WHERE author_id=?; ''',(author_id,)).fetchall()
                return render_template('books.html', books = books)
            else:
                message = "This author is not in our database, or doesn't exist. Try again"
        elif book_name =='' and author_name =='':
            books = db.execute(''' SELECT * FROM books;''').fetchall()
            return render_template('books.html', books=books)
        elif book_name != '' and author_name !='':
            if db.execute(''' SELECT * FROM authors WHERE author_name=?; ''',(author_name,)).fetchone() is not None:
                author_id= db.execute(''' SELECT * FROM authors WHERE author_name=?; ''',(author_name,)).fetchone()['author_id']
            else: 
                return render_template('new_search.html', form=form, message='Author does not exist')
            print(author_id)                
            books = db.execute('''SELECT * FROM books WHERE book_name=? AND author_id=?; ''',(book_name, author_id)).fetchall()
            if author_id is not None and books is not None:
                if db.execute(''' SELECT * FROM books WHERE book_name=? and author_id=?; ''',(book_name, author_id)).fetchall():
                    return render_template('books.html', books=books, authors=author_id)
                else:
                    message = 'This author book combo is not in our database'
    return render_template('new_search.html', form=form, message=message)


@app.route('/sign_in', methods=['GET','POST'])
def signIn ():
    form = SignIn()
    if form.validate_on_submit():
        username = form.username.data
        username = username.lower()
        password = form.password.data
        db = get_db()
        user = db.execute(''' SELECT * FROM users WHERE username=?; ''',(username,)).fetchone()
        if user is None:
            form.username.errors.append('Unknown username')
        elif not check_password_hash(user['password'],password):
            form.password.errors.append('Incorrect Password')
        else:
            session.clear()
            session['username'] = username
            next_page = request.args.get('next')
            if not next_page:
                next_page = url_for('home')
            return redirect(next_page)
    return render_template('signIn.html', form=form)

@app.route('/signUp', methods=['GET','POST'])
def signUp():
    form = SignUp()
    if form.validate_on_submit():
        username = form.username.data
        username = username.lower()
        password = form.password.data
        password2 = form.password.data
        profile_pic = form.profile_pic.data
        filename = secure_filename(profile_pic.filename)
        profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db = get_db()
        db.execute(''' INSERT INTO users (username, password,profile_pic) VALUES(?,?,?); ''',(username, generate_password_hash(password), filename))
        db.commit()
        return redirect(url_for('signIn'))
    return render_template('signUp.html', form=form)


@app.route('/write_review', methods=['GET','POST'])
@login_required
def write_review():
    form = Review()        
    username = session['username']
    if form.validate_on_submit():            
        review = form.review.data
        rating = form.rating.data
        book_name = form.book_name.data
        date = form.date.data
        db = get_db()
        book_id = db.execute(''' SELECT * FROM books WHERE book_name=? ''',(book_name,)).fetchone()['book_id']
        if book_id is None:
            form.book_name.errors.append('This book is not in our Database')
        else:
            db.execute(''' INSERT INTO reviews (review, book_id, user_name, rating) VALUES(?,?,?,?)''',(review, book_id, username, rating))
            db.commit()
            return redirect(url_for('user'))
    return render_template('review.html', form=form)

@app.route('/delete_review/<int:review_id>')
@login_required
def delete_review(review_id):
    db = get_db()
    db.execute('''DELETE FROM reviews WHERE review_id=? ''',(review_id,))
    db.commit()
    return redirect(url_for('user'))

@app.route('/update_review/<int:review_id>', methods=['GET','POST'])
@login_required
def update_review(review_id):
    db = get_db()
    review = db.execute(''' SELECT * FROM reviews WHERE review_id=?; ''',(review_id,)).fetchone()['review']
    edit_review = review
    form = EditReview()
    if request.method =='GET':
        form.review.data = review
    if form.validate_on_submit():
        review = form.review.data
        db.execute(''' UPDATE reviews SET review=? WHERE review_id=? ''',(review,review_id))
        db.commit()
        return redirect('/')
    return render_template('edit_review.html', form=form, review=review)


@app.route('/book/<int:book_id>')
def book(book_id):
    db = get_db()
    message =''
    book = db.execute(''' SELECT * FROM books WHERE book_id =?;''', (book_id,)).fetchone()
    author_id = db.execute(''' SELECT * FROM books WHERE book_id=? ''',(book_id,)).fetchone()['author_id']
    author_name = db.execute(''' SELECT * FROM authors WHERE author_id=?''',(author_id,)).fetchone()['author_name']
    reviews = db.execute('''SELECT * FROM reviews WHERE book_id=?; ''',(book_id,)).fetchall()
    print(reviews)
    if len(reviews) != 0:
        message ='This should display the reviews'
    else:
        message = ''
    image = db.execute(''' SELECT * FROM books WHERE book_id=?; ''',(book_id,)).fetchone()['cover']
    return render_template('book.html',book=book, reviews=reviews, message=message, image1=image, author_name=author_name)

@app.route('/cart')
@login_required
def cart():
    book=''
    full = 0
    if 'cart' not in session:
        session['cart'] = {}
    names = {}
    db = get_db()
    for book_id in session['cart']:
        name = db.execute('''SELECT * FROM books WHERE book_id=?;''',(book_id,)).fetchone()['book_name']
        names[book_id] = name
        book = db.execute(''' SELECT * FROM books WHERE book_id=?; ''',(book_id,)).fetchone()
        price = db.execute(''' SELECT * FROM books WHERE book_id=?''',(book_id,)).fetchone()['price']
        quantity = session['cart'][book_id]
        full+= (price *quantity)
        full = round(full, 2)
    return render_template('cart.html', cart=session['cart'], names=names, book=book, full=full)

@app.route('/add_to_cart/<int:book_id>')
@login_required
def add_to_cart(book_id):
    if 'cart' not in session:
        session['cart'] = {} 
    if book_id not in session['cart']:
        session['cart'][book_id] = 0
    session['cart'][book_id]= session['cart'][book_id] + 1
    return redirect( url_for('cart') ) 


@app.route('/remove/<int:book_id>')
@login_required
def remove(book_id):
    if book_id not in session['cart']:
        session['cart'][book_id] = 0
    for bookId in session['cart'].copy():
        if book_id == int(bookId):
            session['cart'].pop(bookId)
    return redirect(url_for('cart'))


@app.route('/dec_quantity/<int:book_id>')
@login_required
def dec_quantity(book_id):
    if book_id not in session['cart']:
        session['cart'][book_id]=0
    if session['cart'][book_id] >1:
        session['cart'][book_id] = session['cart'][book_id] -1
    return redirect(url_for('cart'))

@app.route('/inc_quantity/<int:book_id>')
@login_required
def inc_quantity(book_id):
    db = get_db()
    stock_left = db.execute(''' SELECT * FROM inventory WHERE book_id=?; ''',(book_id,)).fetchone()['stock_left']
    if book_id not in session['cart']:
        session['cart'][book_id]=0
    if session['cart'][book_id] < stock_left:
        session['cart'][book_id] = session['cart'][book_id] +1
    return redirect(url_for('cart'))

#this was the easiest way to do this and i have no regrets for making an ENTIRE separate url thing just for the price, not one
#so i didn't actually end up using this but i'm going to leave it for the moment because i think i'll need it again for checkout.
@app.route('/full_price')
def full_price():
    db = get_db()
    full = 0
    #Now i have to do the big think
    print(session['cart'])
    for keys in session['cart']:
        price = db.execute(''' SELECT * FROM books WHERE book_id=?''',(keys,)).fetchone()['price']
        print(price)
        quantity = session['cart'][keys]
        full+= (price *quantity)
        print(full)
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET','POST'])
@login_required
def checkout():
    db = get_db()
    message = ''
    names = {}
    book=''
    username = session['username']
    full = 0
    form = PaymentDetails()
    for book_id in session['cart']:
        name = db.execute('''SELECT * FROM books WHERE book_id=?;''',(book_id,)).fetchone()['book_name']
        names[book_id] = name
        book = db.execute(''' SELECT * FROM books WHERE book_id=?; ''',(book_id,)).fetchone()
        price = db.execute(''' SELECT * FROM books WHERE book_id=?''',(book_id,)).fetchone()['price']
        quantity = session['cart'][book_id]
        full+= (price *quantity)
        full = round(full, 2)
        address = db.execute(''' SELECT * FROM shipping_info WHERE username=? ''',(username,)).fetchone()
    address = db.execute(''' SELECT * FROM shipping_info WHERE username=? ''',(username,)).fetchone()        
    if address is None:
            message += 'There is no address'
    if form.validate_on_submit():
        cardNum = form.cardNum.data
        cardHolder = form.cardHolder.data
        cvv = form.cvv.data
        for book_id in session['cart']:
            date = datetime.now().strftime(' %d-%m-%y')
            quantity = session['cart'][book_id]
            old_stock = db.execute(''' SELECT * FROM inventory WHERE book_id=? ''',(book_id,)).fetchone()['stock_left']
            new_stock = old_stock - quantity
            db.execute(''' UPDATE inventory SET stock_left=? WHERE book_id=? ''',(new_stock,book_id))
            db.commit()
            old_stock_sold = db.execute(''' SELECT * FROM inventory WHERE book_id=? ''',(book_id,)).fetchone()['stock_sold']
            stock_sold = old_stock_sold + quantity
            db.execute('''UPDATE inventory SET stock_sold=? WHERE book_id=? ''',(stock_sold,book_id))
            db.commit()
            db.execute('''INSERT INTO transactions(username, book_id,cost,quantity,date) VALUES(?,?,?,?,?) ''',(username, book_id,full,quantity,date))
            db.commit()
        session['cart'].clear()
        return render_template('thank.html')
    return render_template('checkOut.html', form=form, address=address, full=full,cart=session['cart'], names=names,book=book)




@app.route('/shippingInfo', methods=['GET','POST'])
@login_required
def shippingInfo():
    username = session['username']
    form = ShippingInfo()
    db = get_db()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name =form.last_name.data
        address1 = form.address1.data
        address2 = form.address2.data
        address3 = form.address3.data
        country = form.country.data
        postcode = form.postcode.data
        check = db.execute(''' SELECT * FROM shipping_info WHERE username=? ''',(username,)).fetchone()
        if check is None:
            if address2 == '':
                db.execute('''INSERT INTO shipping_info(username, first_name,last_name, address1,address3,country, post_code) values(?,?,?,?,?,?,?)''',(username,first_name,last_name,address1,address3, country, postcode))
                db.commit()
                return redirect(url_for('user'))
            else:
                db.execute('''INSERT INTO shipping_info(username, first_name,last_name, address1,address2,address3,country, post_code) values(?,?,?,?,?,?,?,?)''',(username,first_name,last_name,address1,address2,address3, country, postcode))
                db.commit()
                return redirect(url_for('user'))
        else:
            if address2=='':
                db.execute(''' UPDATE shipping_info SET first_name=?,last_name=?,address1=?,address3=?,country=?,
                post_code=? WHERE username=?; ''',(first_name,last_name,address1,address3,country,postcode,username))
                db.commit()
            else:
                db.execute(''' UPDATE shipping_info SET first_name=?,last_name=?,address1=?,address2=?,address3=?,country=?,
                post_code=? WHERE username=?; ''',(first_name,last_name,address1,address2,address3,country,postcode,username))
                db.commit()
    return render_template('shippingInfo.html', form=form)

@app.route('/user')
@login_required
def user():
    error = ''
    image1 = None
    username = session['username']
    db =get_db()
    message = ''
    if db.execute(''' SELECT * FROM users WHERE username=? ''',(username,)).fetchone()['profile_pic'] is None:
        error = 'No profile picture yet'
    else:
        image1 = db.execute(''' SELECT * FROM users WHERE username=? ''',(username,)).fetchone()['profile_pic']
    address = db.execute(''' SELECT * FROM shipping_info WHERE username=? ''',(username,)).fetchone()
    if address is None:
        message += 'There is no address'
    if db.execute(''' SELECT * FROM transactions WHERE username=?; ''',(username,)).fetchall() is None:
        message = "You've made no transactions yet"
    else:
        books = db.execute(''' SELECT * FROM books; ''').fetchall()
        transactionHistory = db.execute(''' SELECT * FROM transactions WHERE username=?; ''',(username,)).fetchall()
    reviews = db.execute(''' SELECT * FROM reviews WHERE user_name=?''',(username,)).fetchall()
    if len(reviews) == 0:
        message += 'You have not written any reviews yet'
    else:
        message = ''
    return render_template('users.html', message=message, reviews=reviews, image1=image1,address=address, transactions=transactionHistory, books=books)

@app.route('/user_pic', methods=['GET','POST'])
@login_required
def user_pic():
    username = session['username']
    db = get_db()
    form = UserPic()
    if form.validate_on_submit():
        profile_pic = form.profile_pic.data
        filename = secure_filename(profile_pic.filename)
        profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.execute(''' UPDATE users SET profile_pic=? WHERE username=?; ''' ,(filename,username))
        db.commit()
        return redirect(url_for('user'))
    return render_template('profile_pic.html', form=form)


@app.route('/changePassword', methods=['GET','POST'])
def changePassword():
    form = ChangePass()
    if form.validate_on_submit():
        db = get_db()
        username = form.username.data
        old_password = form.old_password.data
        new_password = form.new_password.data
        if db.execute(''' SELECT * FROM users WHERE username=?; ''',(username,)).fetchone() is None:
            form.username.errors.append('This username does not exist')
        else:
            user = db.execute(''' SELECT * FROM users WHERE username=?; ''',(username,)).fetchone()
            if not check_password_hash(user['password'],old_password):
                form.password.errors.append('Incorrect Password')
            else:
                db.execute(''' UPDATE users SET password=? WHERE username=?; ''',(generate_password_hash(new_password),username))
                db.commit()
                return redirect(url_for('signIn'))
    return render_template('changepass.html', form=form)


@app.route('/browse', methods=['GET','POST'])
def browse():
    form = BrowseForm()
    image1 = []
    db = get_db()
    books = db.execute(''' SELECT * FROM books;''').fetchall()
    authors = db.execute('''SELECT *FROM authors; ''').fetchall()
    if form.validate_on_submit():
        genre = form.genre.data
        books = db.execute(''' SELECT * FROM books WHERE genre=?; ''',(genre,)).fetchall()
    for book in books:
        image = db.execute(''' SELECT * FROM books WHERE book_name=?''',(book['book_name'],)).fetchone()['cover']
        image1.append(image)
    return render_template('browse.html', form=form, books=books,authors=authors, image1=image1)

@app.route('/add_book', methods=['GET','POST'])
@admin_only
def add_book():
    form = AddBook()
    if form.validate_on_submit():
        db = get_db()
        author_name = form.author_name.data
        book_name = form.book_name.data
        if db.execute('''SELECT * FROM books WHERE book_name=? ''',(book_name,)).fetchone() is not None:
            if db.execute('''SELECT * FROM authors WHERE author_name=? ''',(author_name,)).fetchone() is not None:
                form.book_name.errors.append('This book is already in the database')
        else:
            description = form.description.data
            genre = form.genre.data
            cover = form.cover.data
            price = float(form.price.data)
            filename = secure_filename(cover.filename)
            cover.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            db.execute('''INSERT INTO authors (author_name) VALUES(?) ''',(author_name,))
            db.commit
            author_id = db.execute(''' SELECT * FROM authors WHERE author_name=?''',(author_name,)).fetchone()['author_id']
            db.execute('''INSERT INTO books (book_name, author_id, description,cover, genre, price)  VALUES(?,?,?,?,?,?)''',(book_name,author_id, description, filename,genre,price))
            db.commit()
            return redirect(url_for('update_inventory'))
    return render_template('addbook.html',form=form)

@app.route('/update_inventory', methods=['GET','POST'])
@admin_only
def update_inventory():
    form = UpdateInventory()
    db = get_db()
    if form.validate_on_submit():
        book_name = form.book_name.data
        author = form.author_name.data
        inventory = form.incInventory.data
        if db.execute('''SELECT * FROM books WHERE book_name=? ''',(book_name,)).fetchone() is None:
            form.book_name.errors.append("This book doesn't exist in our database")
        elif db.execute(''' SELECT * FROM authors WHERE author_name=?''',(author,)).fetchone() is not None:
            author_id = db.execute('''SELECT * FROM authors WHERE author_name=?; ''',(author,)).fetchone()['author_id']
            if db.execute(''' SELECT * FROM books WHERE author_id=?;''',(author_id,)).fetchone() is None:
                form.author.errors.append('This book and author combo does not work')
            else:
                #the stuff with the stuff
                #so i wanna update the inventory not add to it
                book_id = db.execute('''SELECT * FROM books WHERE book_name=?; ''',(book_name,)).fetchone()['book_id']
                if db.execute('''SELECT * FROM inventory WHERE book_id=?; ''',(book_id,)).fetchone() is None:
                    db.execute('''INSERT INTO inventory (book_id,stock_left,stock_sold)VALUES(?,?,?)''',(book_id,inventory,0))
                    db.commit()
                else:
                    old_stock = db.execute('''SELECT * FROM inventory WHERE book_id=?; ''',(book_id,)).fetchone()['stock_left']
                    new_stock = inventory + int(old_stock)
                    db.execute(''' UPDATE inventory SET stock_left=? WHERE book_id=?;''',(new_stock,book_id))
                    db.commit()
        else:
            form.author_name.errors.append('This author does not exist')
    return render_template('incInvent.html', form=form)

@app.route('/inventory', methods=['GET','POST'])
@admin_only
def inventory():
    db = get_db()
    books = db.execute('''SELECT * FROM books; ''').fetchall()
    inventory = db.execute(''' SELECT * FROM inventory ; ''').fetchall()
    return render_template('inventory.html', inventory=inventory,book=books,invent_book=zip(inventory,books))




@app.route('/complaint',methods=['GET','POST'])
@login_required
def complaint():
    form = ComplaintForm()
    db = get_db()
    username = session['username']
    if form.validate_on_submit():
        typeCom = form.typeCom.data
        date = form.date.data
        email = form.email.data
        complaint = form.complaint.data
        db.execute('''INSERT INTO complaints (username,date,complaint,type,email)VALUES(?,?,?,?,?) ''',(username,date,complaint,typeCom,email))
        db.commit()
        return redirect(url_for('user'))
    return render_template('query.html', form=form)

@app.route('/viewComplaints', methods=['GET','POST'])
@admin_only
def viewComplaints():
    db = get_db()
    complaint = db.execute(''' SELECT * FROM complaints;''').fetchall()
    return render_template('viewComplaints.html', complaint=complaint)

#email sending that just does not work 
'''
@app.route('/response/<int:complaint_id>', methods=['GET','POST'])
@admin_only
def response(complaint_id):
    form = ResponseForm()
    db =get_db()
    if form.validate_on_submit():
        response =form.response.data
        date = form.date.data'''
        #email = db.execute(''' SELECT * FROM complaints WHERE complaint_id =?;''',(complaint_id,)).fetchone()['email']
        #msg = Message(response, recipients=['rainsfordemma@outlook.com'])
        #mail.send(msg)
        #return 'hi'
        #return redirect(url_for('viewComplaints'))
    #return render_template('response.html', form=form)

@app.route('/response/<int:complaint_id>', methods=['GET','POST'])
@admin_only
def response(complaint_id):
    form =  ResponseForm()
    db = get_db()
    username = db.execute(''' SELECT * FROM complaints WHERE complaint_id=?;''',(complaint_id,)).fetchone()['username']
    if form.validate_on_submit():
        response = form.response.data
        date = form.date.data
        db.execute(''' INSERT INTO responses (username,response,date, complaint_id) VALUES(?,?,?,?) ''',(username, response, date,complaint_id))
        db.commit()
        return redirect(url_for('viewComplaints'))
    return render_template('response.html', form=form)

#change how this looks
@app.route('/viewResponse', methods=['GET','POST'])
@login_required
def viewResponse():
    db = get_db()
    response = db.execute(''' SELECT * FROM responses;''').fetchall()
    return render_template('viewResponses.html', response=response)



    