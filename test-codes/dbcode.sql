CREATE TABLE tests (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    button      VARCHAR(20),
    success     INT,
    force_val   TEXT,
    time_val    TEXT,
    date        DATE,
    time        TIME
);

CREATE TABLE profiles (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    pName       VARCHAR(255) UNIQUE,
    pressTime   INT,
    nTimes      INT,
    interval    INT
);

INSERT INTO profiles (pName) VALUES ('Custom');
INSERT INTO profiles (pName, pressTime, nTimes, interval) VALUES ('Reset', 1, 10, 5);
INSERT INTO profiles (pName, pressTime, nTimes, interval) VALUES ('WPS/Info', 5, 10, 5);
UPDATE profiles SET pressTime = 0, nTimes = 0, interval = 0 WHERE id == 1;
INSERT INTO profiles (pName, pressTime, nTimes, interval) VALUES ('XDXD', 7, 7, 7);
DELETE FROM profiles WHERE pName == "XDXD";
INSERT INTO tests (button, success, force_val, time_val, date, time) VALUES ('WPS', '[1, 1, 1, 1, 1]', '[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]', '[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]', '12-1-2025', '15:29')