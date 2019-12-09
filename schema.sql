DROP TABLE IF EXISTS node;

CREATE TABLE node (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  codeOn TEXT NOT NULL,
  codeOff TEXT NOT NULL,
  iterations INTEGER,
  state BOOLEAN DEFAULT FALSE
);

INSERT INTO node (title, codeOn, codeOff, iterations)
VALUES ('Bücherregal 📚', '1361', '1364', 3);

INSERT INTO node (title, codeOn, codeOff, iterations)
VALUES ('Wohnzimmer-Ecke 🛋️', '5201', '5204', 3);

INSERT INTO node (title, codeOn, codeOff, iterations)
VALUES ('Flur-Ecke 🚪', '4433', '4436', 3);

INSERT INTO node (title, codeOn, codeOff, iterations)
VALUES ('Esstisch 🍽️', '5393', '5396', 3);

INSERT INTO node (title, codeOn, codeOff, iterations)
VALUES ('Baby Ambient 👶', '4195665', '4195668', 3);

/*
INSERT INTO node (title, codeOn, codeOff, iterations)
VALUES ('B', '4198737', '4198740', 3);
*/

INSERT INTO node (title, codeOn, codeOff, iterations)
VALUES ('Schlafzimmer 🛏️', '4199505', '4199508', 3);

/*
INSERT INTO node (title, codeOn, codeOff, iterations)
VALUES ('D', '4199697', '4199700', 3);
*/
