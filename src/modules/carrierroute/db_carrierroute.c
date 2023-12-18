
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
 * ../../modules/carrierroute/kamailio-carrierroute.xml.
 * It can be regenerated by running 'make modules' in the db/schema
 * directory of the source code. You need to have xsltproc and
 * docbook-xsl stylesheets installed.
 * ALL CHANGES DONE HERE WILL BE LOST IF THE FILE IS REGENERATED
 * @endcond
 */

#include "db_carrierroute.h"

/* database variables */
/* TODO assign read-write or read-only URI, introduce a parameter in XML */

//extern str carrierroute_db_url;
db1_con_t *carrierroute_dbh = NULL;
db_func_t carrierroute_dbf;

str carrierroute_table = str_init("carrierroute");

/* column names */
str carrierroute_id_col = str_init("id");
str carrierroute_carrier_col = str_init("carrier");
str carrierroute_domain_col = str_init("domain");
str carrierroute_scan_prefix_col = str_init("scan_prefix");
str carrierroute_flags_col = str_init("flags");
str carrierroute_mask_col = str_init("mask");
str carrierroute_prob_col = str_init("prob");
str carrierroute_strip_col = str_init("strip");
str carrierroute_rewrite_host_col = str_init("rewrite_host");
str carrierroute_rewrite_prefix_col = str_init("rewrite_prefix");
str carrierroute_rewrite_suffix_col = str_init("rewrite_suffix");
str carrierroute_description_col = str_init("description");

/* table version */
const unsigned int carrierroute_version = 3;

str carrierfailureroute_table = str_init("carrierfailureroute");

/* column names */
str carrierfailureroute_id_col = str_init("id");
str carrierfailureroute_carrier_col = str_init("carrier");
str carrierfailureroute_domain_col = str_init("domain");
str carrierfailureroute_scan_prefix_col = str_init("scan_prefix");
str carrierfailureroute_host_name_col = str_init("host_name");
str carrierfailureroute_reply_code_col = str_init("reply_code");
str carrierfailureroute_flags_col = str_init("flags");
str carrierfailureroute_mask_col = str_init("mask");
str carrierfailureroute_next_domain_col = str_init("next_domain");
str carrierfailureroute_description_col = str_init("description");

/* table version */
const unsigned int carrierfailureroute_version = 2;

str carrier_name_table = str_init("carrier_name");

/* column names */
str carrier_name_id_col = str_init("id");
str carrier_name_carrier_col = str_init("carrier");

/* table version */
const unsigned int carrier_name_version = 1;

str domain_name_table = str_init("domain_name");

/* column names */
str domain_name_id_col = str_init("id");
str domain_name_domain_col = str_init("domain");

/* table version */
const unsigned int domain_name_version = 1;


/*
 * Closes the DB connection.
 */
void carrierroute_db_close(void)
{
	if(carrierroute_dbh) {
		carrierroute_dbf.close(carrierroute_dbh);
		carrierroute_dbh = NULL;
	}
}


/*!
 * Initialises the DB API, check the table version and closes the connection.
 * This should be called from the mod_init function.
 *
 * \return 0 means ok, -1 means an error occurred.
 */
int carrierroute_db_init(void)
{
	if(!carrierroute_db_url.s || !carrierroute_db_url.len) {
		LM_ERR("you have to set the db_url module parameter.\n");
		return -1;
	}
	if(db_bind_mod(&carrierroute_db_url, &carrierroute_dbf) < 0) {
		LM_ERR("can't bind database module.\n");
		return -1;
	}
	if((carrierroute_dbh = carrierroute_dbf.init(&carrierroute_db_url))
			== NULL) {
		LM_ERR("can't connect to database.\n");
		return -1;
	}
	if(!DB_CAPABILITY(carrierroute_dbf, DB_CAP_RAW_QUERY)) {
		LM_ERR("database does not support required raw queries capability\n");
		return -1;
	}
	if(db_check_table_version(&carrierroute_dbf, carrierroute_dbh,
			   &carrierroute_table, carrierroute_version)
			< 0) {
		DB_TABLE_VERSION_ERROR(carrierroute_table);
		goto dberror;
	}
	if(db_check_table_version(&carrierroute_dbf, carrierroute_dbh,
			   &carrierfailureroute_table, carrierfailureroute_version)
			< 0) {
		DB_TABLE_VERSION_ERROR(carrierfailureroute_table);
		goto dberror;
	}
	if(db_check_table_version(&carrierroute_dbf, carrierroute_dbh,
			   &carrier_name_table, carrier_name_version)
			< 0) {
		DB_TABLE_VERSION_ERROR(carrier_name_table);
		goto dberror;
	}
	if(db_check_table_version(&carrierroute_dbf, carrierroute_dbh,
			   &domain_name_table, domain_name_version)
			< 0) {
		DB_TABLE_VERSION_ERROR(domain_name_table);
		goto dberror;
	}

	carrierroute_db_close();
	return 0;

dberror:
	carrierroute_db_close();
	return -1;
}


/*!
 * Initialize the DB connection without checking the table version and DB URL.
 * This should be called from child_init. An already existing database
 * connection will be closed, and a new one created.
 *
 * \return 0 means ok, -1 means an error occurred.
 */
int carrierroute_db_open(void)
{
	if(carrierroute_dbh) {
		carrierroute_dbf.close(carrierroute_dbh);
	}
	if((carrierroute_dbh = carrierroute_dbf.init(&carrierroute_db_url))
			== NULL) {
		LM_ERR("can't connect to database.\n");
		return -1;
	}
	return 0;
}
