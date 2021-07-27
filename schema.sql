DROP TABLE IF EXISTS users;

CREATE TABLE users 
(
    profile_pic TEXT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    user_id INTEGER PRIMARY KEY AUTOINCREMENT
);


DROP TABLE IF EXISTS books;

CREATE TABLE books
(
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre TEXT NOT NULL,
    book_name TEXT NOT NULL,
    author_id TEXT NOT NULL,
    description TEXT NOT NULL,
    cover TEXT NOT NULL,
    price FLOAT NOT NUll
);

INSERT INTO books (cover,price,book_name,genre,author_id, description)
VALUES
    ("persuasion.jpg" ,3.99,"Persuasion","classic",12032, "Twenty-seven-year old Anne Elliot is Austen's most adult heroine. Eight years before the story proper begins, she is happily betrothed to a naval officer, Frederick Wentworth, but she precipitously breaks off the engagement when persuaded by her friend Lady Russell that such a match is unworthy. The breakup produces in Anne a deep and long-lasting regret. When later Wentworth returns from sea a rich and successful captain, he finds Anne's family on the brink of financial ruin and his own sister a tenant in Kellynch Hall, the Elliot estate"),
    ( "c+p.jpg",4.99,"Crime and Punishment","classic",11032,"Raskolnikov, a destitute and desperate former student, wanders through the slums of St Petersburg and commits a random murder without remorse or regret. He imagines himself to be a great man, a Napoleon: acting for a higher purpose beyond conventional moral law. But as he embarks on a dangerous game of cat and mouse with a suspicious police investigator, Raskolnikov is pursued by the growing voice of his conscience and finds the noose of his own guilt tightening around his neck. Only Sonya, a downtrodden prostitute, can offer the chance of redemption."),
    ("thefinalempire.jpg",13.99,"The Final Empire","fantasy",14032,"The mists rule the night...The lord ruler owns the world. For a thousand years the ash fell. For a thousand years, the Skaa slaved in misery and lived in fear. For a thousand years, the Lord Ruler reigned with absolute power and ultimate terror, divinely invincible. Every attempted revolt has failed miserably. A new kind of uprising is being planned, one that depends on the cunning of a brilliant criminal mastermind and the courage of an unlikely heroine, a Skaa street urchin, who must learn to master Allomancy, the power of a mistborn."),
    ("harrypotter1.jpg",10.99,"Harry Potter and the Philosphers stone","childrens",13032,"Harry Potter's life is miserable. His parents are dead and he's stuck with his heartless relatives, who force him to live in a tiny closet under the stairs. But his fortune changes when he receives a letter that tells him the truth about himself: he's a wizard. A mysterious visitor rescues him from his relatives and takes him to his new home, Hogwarts School of Witchcraft and Wizardry.After a lifetime of bottling up his magical powers, Harry finally feels like a normal kid. But even within the Wizarding community, he is special. He is the boy who lived: the only person to have ever survived a killing curse inflicted by the evil Lord Voldemort, who launched a brutal takeover of the Wizarding world, only to vanish after failing to kill Harry."),
    ("neverwhere.jpg" ,11.99,"Neverwhere","fantasy",17032,"Under the streets of London there's a place most people could never even dream of. A city of monsters and saints, murderers and angels, knights in armour and pale girls in black velvet. This is the city of the people who have fallen between the cracks.Richard Mayhew, a young businessman, is going to find out more than enough about this other London. A single act of kindness catapults him out of his workday existence and into a world that is at once eerily familiar and utterly bizarre. And a strange destiny awaits him down here, beneath his native city: Neverwhere."),
    ("prideandprejudice.jpg",2.99,"Pride and Prejudice","classic",12032,"Set in England in the early 19th century, Pride and Prejudice tells the story of Mr. and Mrs. Bennet's five unmarried daughters after the rich and eligible Mr. Bingley and his status-conscious friend, Mr. Darcy, have moved into their neighborhood.When Elizabeth Bennet meets Mr. Darcy she is repelled by his overbearing pride, and prejudice towards her family. But the Bennet girls are in need of financial security in the shape of husbands, so when Darcy's friend, the affable Mr. Bingley, forms an attachment to Jane, Darcy becomes increasingly hard to avoid. Polite society will be turned upside down in this witty drama of friendship, rivalry, and love—Jane Austen's classic romance novel.");



DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews
(
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    review TEXT NOT NULL,
    book_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    user_name TEXT NOT NULL
);


DROP TABLE IF EXISTS authors;

CREATE TABLE authors
(
    author_id INTEGER PRIMARY KEY,
    author_name TEXT NOT NULL
);

INSERT INTO authors (author_id, author_name)
VALUES
    (12032, "Jane Austen"),
    (11032, "Fyodor Dostoevsky"),
    (14032, "Brandon Sanderson"),
    (13032, "J.K ROWLING"),
    (17032,"Neil Gaiman");

DROP TABLE IF EXISTS company_reviews;

CREATE TABLE company_reviews
(
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    review TEXT NOT NULL,
    book_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    date DATE NOT NULL
);
INSERT INTO company_reviews (review,book_id,user_name, rating,date)
VALUES 
    ("Came very quickly", 12032, "brutus", '','');



DROP TABLE IF EXISTS inventory;
CREATE TABLE inventory
(
    book_id INTEGER PRIMARY KEY,
    stock_left INTEGER,
    stock_sold INTEGER
);

INSERT INTO inventory (book_id,stock_left,stock_sold)
VALUES 
    (1, 20, 0),
    (2,17, 2),
    (3,6, 2),
    (4, 7, 10), 
    (5, 8,2),
    (6,17,10);

DROP TABLE IF EXISTS shipping_info;
CREATE TABLE shipping_info
(
    username TEXT PRIMARY KEY NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    address1 TEXT NOT NULL,
    address2 TEXT,
    address3 TEXT NOT NULL,
    country TEXT NOT NULL,
    post_code TEXT NOT NULL


);
DROP TABLE IF EXISTS payment;
CREATE TABLE payment
(
    username TEXT PRIMARY KEY NOT NULL,
    cardholder TEXT NOT NULL,
    cardNum INTEGER NOT NULL,
    cvv INTEGER NOT NULL
);
DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions
(
    transaction_id INTEGER PRIMARY KEY NOT NULL,
    date DATE NOT NULL,
    username TEXT NOT NULL,
    book_id INTEGER NOT NULL,
    cost INTEGER NOT NULL,
    quantity INTEGER NOT NULL
);

DROP TABLE IF EXISTS complaints;
CREATE TABLE complaints
(
    complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    date DATE NOT NULL,
    complaint TEXT NOT NULL,
    type TEXT NOT NULL,
    email TEXT NOT NULL
);
DROP TABLE IF EXISTS responses;
CREATE TABLE responses
(
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    response TEXT NOT NULL,
    date DATE NOT NULL,
    complaint_id INTEGER NOT NULL
);



