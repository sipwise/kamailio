#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <unistd.h>

#include "../../sr_module.h"
#include "../../dprint.h"
#include "../../str.h"
#include "../../parser/msg_parser.h"
#include "../../mem/mem.h"
#include "../presence/bind_presence.h"
#include "add_events.h"
#include "presence_asfeature.h"

MODULE_VERSION

/* module functions */
static int mod_init(void);

/** SL API structure */
sl_api_t slb;
/* TM functions */
struct tm_binds tmb;

/** Presence API structure */
presence_api_t pres;

pua_api_t pua;

libxml_api_t libxml_api;

str outbound_proxy = {0, 0};
char* dnd_param = 0;

static param_export_t params[]={
	{"outbound_proxy",           STR_PARAM, &outbound_proxy.s},
	{"dnd_param",		STR_PARAM, &dnd_param},
	{0,                          0,         0}
};
static mi_export_t mi_cmds[] = {
//	{ "set_feature",	mi_set,		0,  0,  mi_child_init},
	{ 0,			0,			0,  0,  0}
};


/* module exports */
struct module_exports exports= {
    "presence_asfeature",	/* module name */
    DEFAULT_DLFLAGS,	/* dlopen flags */
    0,			/* exported functions */
    params,		/* exported parameters */
    0,			/* exported statistics */
    mi_cmds,			/* exported MI functions */
    0,			/* exported pseudo-variables */
    0,			/* extra processes */
    mod_init,		/* module initialization function */
    0,			/* response handling function */
    0,			/* destroy function */
    0			/* per-child init function */
};

/*
 * init module function
 */
static int mod_init(void)
{
	bind_presence_t bind_presence;
	load_tm_f  load_tm;
	bind_pua_t bind_pua;
	bind_libxml_t bind_libxml;

	/* bind the SL API */
	if (sl_load_api(&slb)!=0) {
		LM_ERR("cannot bind to SL API\n");
		return -1;
	}
	/* import the TM auto-loading function */
	if((load_tm=(load_tm_f)find_export("load_tm", NO_SCRIPT, 0))==NULL) {
		LM_ERR("can't import load_tm\n");
		return -1;
	}
	/* load all TM stuff */
	if(load_tm_api(&tmb)==-1) {
		LM_ERR("can't load tm functions\n");
		return -1;
	}

	bind_presence= (bind_presence_t)find_export("bind_presence", 1,0);
	if (!bind_presence) {
		LM_ERR("can't bind presence\n");
		return -1;
	}
	if (bind_presence(&pres) < 0) {
		LM_ERR("can't bind presence\n");
		return -1;
	}

	if (pres.add_event == NULL) {
		LM_ERR("could not import add_event\n");
		return -1;
	}
	bind_pua= (bind_pua_t)find_export("bind_pua", 1,0);
	if (!bind_pua) {
		LM_ERR("Can't bind pua\n");
		return -1;
	}
	if (bind_pua(&pua) < 0) {
		LM_ERR("mod_init Can't bind pua\n");
		return -1;
	}

	/* bind libxml wrapper functions */
	if((bind_libxml= (bind_libxml_t)find_export("bind_libxml_api", 1, 0))== NULL) {
		LM_ERR("can't import bind_libxml_api\n");
		return -1;
	}
	if(bind_libxml(&libxml_api)< 0) {
		LM_ERR("can not bind libxml api\n");
		return -1;
	}
	if(libxml_api.xmlNodeGetNodeByName==NULL) {
		LM_ERR("can not bind libxml api\n");
		return -1;
	}


	if(asfeature_add_events() < 0) {
		LM_ERR("failed to add as-feature-event events\n");
		return -1;
	}

	outbound_proxy.len = outbound_proxy.s ? strlen(outbound_proxy.s) : 0;

	return 0;
}
