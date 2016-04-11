CREATE TABLE topos_d (
    id INTEGER PRIMARY KEY NOT NULL,
    rectime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    s_method VARCHAR(64) DEFAULT '' NOT NULL,
    s_cseq VARCHAR(64) DEFAULT '' NOT NULL,
    a_callid VARCHAR(255) DEFAULT '' NOT NULL,
    a_uuid VARCHAR(255) DEFAULT '' NOT NULL,
    b_uuid VARCHAR(255) DEFAULT '' NOT NULL,
    a_contact VARCHAR(128) DEFAULT '' NOT NULL,
    b_contact VARCHAR(128) DEFAULT '' NOT NULL,
    as_contact VARCHAR(128) DEFAULT '' NOT NULL,
    bs_contact VARCHAR(128) DEFAULT '' NOT NULL,
    a_tag VARCHAR(255) DEFAULT '' NOT NULL,
    b_tag VARCHAR(255) DEFAULT '' NOT NULL,
    a_rr TEXT DEFAULT '' NOT NULL,
    b_rr TEXT DEFAULT '' NOT NULL,
    s_rr TEXT DEFAULT '' NOT NULL,
    iflags INTEGER DEFAULT 0 NOT NULL,
    a_uri VARCHAR(128) DEFAULT '' NOT NULL,
    b_uri VARCHAR(128) DEFAULT '' NOT NULL,
    r_uri VARCHAR(128) DEFAULT '' NOT NULL,
    a_srcaddr VARCHAR(128) DEFAULT '' NOT NULL,
    b_srcaddr VARCHAR(128) DEFAULT '' NOT NULL,
    a_socket VARCHAR(128) DEFAULT '' NOT NULL,
    b_socket VARCHAR(128) DEFAULT '' NOT NULL
);

CREATE INDEX topos_d_rectime_idx ON topos_d (rectime);
CREATE INDEX topos_d_a_callid_idx ON topos_d (a_callid);

INSERT INTO version (table_name, table_version) values ('topos_d','1');

CREATE TABLE topos_t (
    id INTEGER PRIMARY KEY NOT NULL,
    rectime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    s_method VARCHAR(64) DEFAULT '' NOT NULL,
    s_cseq VARCHAR(64) DEFAULT '' NOT NULL,
    a_callid VARCHAR(255) DEFAULT '' NOT NULL,
    a_uuid VARCHAR(255) DEFAULT '' NOT NULL,
    b_uuid VARCHAR(255) DEFAULT '' NOT NULL,
    direction INTEGER DEFAULT 0 NOT NULL,
    x_via TEXT DEFAULT '' NOT NULL,
    x_vbranch VARCHAR(255) DEFAULT '' NOT NULL,
    x_rr TEXT DEFAULT '' NOT NULL,
    y_rr TEXT DEFAULT '' NOT NULL,
    s_rr TEXT DEFAULT '' NOT NULL,
    x_uri VARCHAR(128) DEFAULT '' NOT NULL,
    a_contact VARCHAR(128) DEFAULT '' NOT NULL,
    b_contact VARCHAR(128) DEFAULT '' NOT NULL,
    as_contact VARCHAR(128) DEFAULT '' NOT NULL,
    bs_contact VARCHAR(128) DEFAULT '' NOT NULL,
    x_tag VARCHAR(255) DEFAULT '' NOT NULL,
    a_tag VARCHAR(255) DEFAULT '' NOT NULL,
    b_tag VARCHAR(255) DEFAULT '' NOT NULL,
    a_srcaddr VARCHAR(128) DEFAULT '' NOT NULL,
    b_srcaddr VARCHAR(128) DEFAULT '' NOT NULL,
    a_socket VARCHAR(128) DEFAULT '' NOT NULL,
    b_socket VARCHAR(128) DEFAULT '' NOT NULL
);

CREATE INDEX topos_t_rectime_idx ON topos_t (rectime);
CREATE INDEX topos_t_a_callid_idx ON topos_t (a_callid);

INSERT INTO version (table_name, table_version) values ('topos_t','1');

