DROP TABLE IF EXISTS node;

CREATE TABLE node (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  codeOn TEXT NOT NULL,
  codeOff TEXT NOT NULL,
  iterations INTEGER,
  state BOOLEAN DEFAULT FALSE
);

DROP TABLE IF EXISTS event;

CREATE TABLE event (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nodeIdRef INTEGER NOT NULL,
  switchOn BOOLEAN NOT NULL,
  weekdays INTEGER NOT NULL,
  hour INTEGER NOT NULL,
  minute INTEGER NOT NULL
)
