CREATE TABLE htable (
    id INTEGER PRIMARY KEY NOT NULL,
    key_name VARCHAR(256) DEFAULT '' NOT NULL,
    key_type INTEGER DEFAULT 0 NOT NULL,
    value_type INTEGER DEFAULT 0 NOT NULL,
    key_value VARCHAR(512) DEFAULT '' NOT NULL,
    expires INTEGER DEFAULT 0 NOT NULL
);

INSERT INTO version (table_name, table_version) values ('htable','2');

