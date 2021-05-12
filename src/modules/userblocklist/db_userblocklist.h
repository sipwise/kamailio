/*!
 * \file
 * \ingroup db
 * \brief Database support for modules.
 *
 * Database support functions for modules.
 *
 * @cond
 * WARNING:
 * This file was autogenerated from the XML source file
 * ../../modules/userblocklist/kamailio-userblocklist.xml.
 * It can be regenerated by running 'make modules' in the db/schema
 * directory of the source code. You need to have xsltproc and
 * docbook-xsl stylesheets installed.
 * ALL CHANGES DONE HERE WILL BE LOST IF THE FILE IS REGENERATED
 * @endcond
 */

#ifndef db_userblocklist_h
#define db_userblocklist_h


/* necessary includes */
#include "../../lib/srdb1/db.h"
#include "../../core/str.h"
#include "../../core/ut.h"

#include <string.h>


/* database variables */

extern str userblocklist_db_url;
extern db1_con_t * userblocklist_dbh;
extern db_func_t userblocklist_dbf;

#define userblocklist_DB_URL { "db_url", PARAM_STR, &userblocklist_db_url },

#define userblocklist_DB_TABLE { "userblocklist_table", PARAM_STR, &userblocklist_table },

extern str userblocklist_table;

/* column names */
extern str userblocklist_id_col;
extern str userblocklist_username_col;
extern str userblocklist_domain_col;
extern str userblocklist_prefix_col;
extern str userblocklist_allowlist_col;
#define userblocklist_DB_COLS \
{ "userblocklist_id_col", PARAM_STR, &userblocklist_id_col }, \
{ "userblocklist_username_col", PARAM_STR, &userblocklist_username_col }, \
{ "userblocklist_domain_col", PARAM_STR, &userblocklist_domain_col }, \
{ "userblocklist_prefix_col", PARAM_STR, &userblocklist_prefix_col }, \
{ "userblocklist_allowlist_col", PARAM_STR, &userblocklist_allowlist_col }, \

/* table version */
extern const unsigned int userblocklist_version;

#define globalblocklist_DB_TABLE { "globalblocklist_table", PARAM_STR, &globalblocklist_table },

extern str globalblocklist_table;

/* column names */
extern str globalblocklist_id_col;
extern str globalblocklist_prefix_col;
extern str globalblocklist_allowlist_col;
extern str globalblocklist_description_col;
#define globalblocklist_DB_COLS \
{ "globalblocklist_id_col", PARAM_STR, &globalblocklist_id_col }, \
{ "globalblocklist_prefix_col", PARAM_STR, &globalblocklist_prefix_col }, \
{ "globalblocklist_allowlist_col", PARAM_STR, &globalblocklist_allowlist_col }, \
{ "globalblocklist_description_col", PARAM_STR, &globalblocklist_description_col }, \

/* table version */
extern const unsigned int globalblocklist_version;


/*
 * Closes the DB connection.
 */
void userblocklist_db_close(void);

/*!
 * Initialises the DB API, check the table version and closes the connection.
 * This should be called from the mod_init function.
 *
 * \return 0 means ok, -1 means an error occurred.
 */
int userblocklist_db_init(void);

/*!
 * Initialize the DB connection without checking the table version and DB URL.
 * This should be called from child_init. An already existing database
 * connection will be closed, and a new one created.
 *
 * \return 0 means ok, -1 means an error occurred.
 */
int userblocklist_db_open(void);

#endif
