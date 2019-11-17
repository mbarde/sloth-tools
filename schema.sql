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
VALUES ('Wohnzimmer-Ecke', '5201', '5204', 3);

INSERT INTO node (title, codeOn, codeOff, iterations)
VALUES ('Flur-Ecke', '4433', '4436', 3);

INSERT INTO node (title, codeOn, codeOff, iterations)
VALUES ('Esstisch 🍽️', '5393', '5396', 3);
