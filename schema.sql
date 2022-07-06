DROP TABLE IF EXISTS node;

CREATE TABLE node (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  codeOn TEXT NOT NULL,
  codeOff TEXT NOT NULL,
  protocol TEXT,
  pulselenth TEXT,
  iterations INTEGER,
  state BOOLEAN DEFAULT FALSE
);

DROP TABLE IF EXISTS event;

CREATE TABLE event (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nodeIdRef INTEGER NOT NULL,
  switchOn BOOLEAN NOT NULL,
  mode INTEGER NOT NULL, /* 0: fixed, 1: sunrise, 2: sunset */
  weekdays INTEGER NOT NULL,
  hour INTEGER NOT NULL,
  minute INTEGER NOT NULL,
  sunriseOffset INTEGER NOT NULL, /* offset in minutes (can be + or -) */
  sunsetOffset INTEGER NOT NULL, /* offset in minutes (can be + or -) */
  randomOffset INTEGER NOT NULL /* offset in minutes (should only be +) */
);
