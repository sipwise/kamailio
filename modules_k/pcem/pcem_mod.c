/*
 * $Id$
 * 
 * PacketCable Event Messages module
 *
 * Copyright (C) 2012 Sipwise GmbH
 *
 * This file is part of Kamailio, a free SIP server.
 *
 * Kamailio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version
 *
 * Kamailio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 */

#include <stdio.h>
#include <string.h>

#include "../../sr_module.h"
#include "../../dprint.h"
#include "../../mem/mem.h"
#include "../../modules/tm/tm_load.h"
#include "../../str.h"
#include "../rr/api.h"
#include "pcem_mod.h"
#include "pcem_logic.h"

MODULE_VERSION

struct tm_binds tmb;
struct rr_binds rrb;

static int mod_init(void);
static void destroy(void);
static int child_init(int rank);

int pcem_qos_flag = -1; /* don't send qos messages by default */
int pcem_all_flag = -1; /* don't send any messages by default */

/*
static int bind_acc(acc_api_t* api);
static int acc_register_engine(acc_engine_t *eng);
static int acc_init_engines(void);
static acc_engine_t *_acc_engines=NULL;
*/
static int _pcem_module_initialized = 0;

/*
static int acc_fixup(void** param, int param_no);
static int free_acc_fixup(void** param, int param_no);
*/


static cmd_export_t cmds[] = {
/*
	{"pcem_test", (cmd_function)w_pkg_em_test, 1,
		acc_fixup, free_acc_fixup,
		ANY_ROUTE},
*/
	{0, 0, 0, 0, 0, 0}
};



static param_export_t params[] = {
	/*{"test_str",             INT_PARAM, &test_str.s             },*/
	{"qos_flag", INT_PARAM, &pcem_qos_flag },
	{"all_flag", INT_PARAM, &pcem_all_flag },
	{0,0,0}
};


struct module_exports exports= {
	"pcem",
	DEFAULT_DLFLAGS, /* dlopen flags */
	cmds,       /* exported functions */
	params,     /* exported params */
	0,          /* exported statistics */
	0,          /* exported MI functions */
	0,          /* exported pseudo-variables */
	0,          /* extra processes */
	mod_init,   /* initialization module */
	0,          /* response function */
	destroy,    /* destroy function */
	child_init  /* per-child init function */
};


static int mod_init( void )
{
	if ((pcem_qos_flag != -1) && 
		!flag_in_range(pcem_qos_flag)) {
		LM_ERR("pcem_qos_flag set to invalid value\n");
		return -1;
	}
	if ((pcem_all_flag != -1) && 
		!flag_in_range(pcem_all_flag)) {
		LM_ERR("pcem_all_flag set to invalid value\n");
		return -1;
	}

	/* load the TM API */
	if (load_tm_api(&tmb)!=0) {
		LM_ERR("can't load TM API\n");
		return -1;
	}

	/* load the RR API */
	if (load_rr_api(&rrb)!=0) {
		LM_ERR("can't load RR API\n");
		return -1;
	}
	/* we need the append_fromtag on in RR */
	if (!rrb.append_fromtag) {
		LM_ERR("'append_fromtag' RR param is not enabled\n");
		return -1;
	}

	/* listen for all incoming requests  */
	if ( tmb.register_tmcb( 0, 0, TMCB_REQUEST_IN, pcem_onreq, 0, 0 ) <=0 ) {
		LM_ERR("cannot register TMCB_REQUEST_IN callback\n");
		return -1;
	}

	_pcem_module_initialized = 1;

	return 0;
}


static int child_init(int rank)
{
	if (rank==PROC_INIT || rank==PROC_MAIN || rank==PROC_TCP_MAIN)
		return 0; /* do nothing for the main process */

	return 0;
}


static void destroy(void)
{
}

