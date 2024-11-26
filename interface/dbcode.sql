CREATE TABLE tests (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    button      VARCHAR(20),
    success     INT,
    force_val   TEXT,
    time_val    TEXT,
    date        DATE,
    time        TIME
)