/*
 * AVP Headers
 *
 * Copyright (C) 2018 Kirill Solomko
 *
 * This file is part of SIP Router, a free SIP server.
 *
 * SIP Router is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version
 *
 * SIP Router is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../../sr_module.h"
#include "../../mod_fix.h"
#include "../../dprint.h"
#include "../../xavp.h"
#include "../../pvar.h"
#include "../../data_lump.h"
#include "../../parser/msg_parser.h"

MODULE_VERSION

#define MODULE_NAME "pv_headers"

#define XAVP_NAME "headers"

static str xavp_name = str_init(XAVP_NAME);

static void destroy(void);
static int mod_init(void);

static int pv_collect_headers(struct sip_msg* msg, char* _s1, char* _s2);
static int pv_apply_headers(struct sip_msg* msg, char* _s1, char* _s2);

static int pv_check_header(struct sip_msg* _m, str* hname, char* _s2);
static int pv_append_header(struct sip_msg* _m, str* hname, str* value);
static int pv_modify_header(struct sip_msg* _m, str* hname, str* modify);
static int pv_remove_header(struct sip_msg* _m, str* hname, char* _s2);

static int pv_set_xavp(str *xname, str *name, str *val);
static int pv_free_xavp(str *xname);

/*
 * Exported functions
 */
static cmd_export_t cmds[] = {
    {"pv_collect_headers", (cmd_function)pv_collect_headers, 0, 0, 0, ANY_ROUTE},
    {"pv_apply_headers", (cmd_function)pv_apply_headers, 0, 0, 0, ANY_ROUTE},
    {"pv_check_header", (cmd_function)pv_check_header, 1, fixup_str_null, fixup_free_str_null, ANY_ROUTE},
    {"pv_append_header", (cmd_function)pv_append_header, 2, fixup_str_str, fixup_free_str_str, ANY_ROUTE},
    {"pv_modify_header", (cmd_function)pv_modify_header, 2, fixup_str_str, fixup_free_str_str, ANY_ROUTE},
    {"pv_remove_header", (cmd_function)pv_remove_header, 1, fixup_str_null, fixup_free_str_null, ANY_ROUTE},
    {0, 0, 0, 0, 0, 0}
};


static param_export_t params[] = {
    {"xavp_name", PARAM_STR, &xavp_name},
    {0, 0, 0}
};

struct module_exports exports = {
	MODULE_NAME,
	DEFAULT_DLFLAGS, /* dlopen flags */
	cmds,      /* Exported functions */
	params,    /* Exported parameters */
	0,         /* exported statistics */
	0,         /* exported MI functions */
	0,         /* exported pseudo-variables */
	0,         /* extra processes */
	mod_init,  /* module initialization function */
	0,         /* response function */
	destroy,   /* destroy function */
	0          /* child initialization function */
};

static int mod_init(void)
{
    LM_INFO("%s module init...\n", MODULE_NAME);
    return 0;
}

static void destroy(void)
{
    pv_free_xavp(&xavp_name);
    LM_INFO("%s module unload...\n", MODULE_NAME);
}

static int pv_collect_headers(struct sip_msg* msg, char* _s1, char* _s2)
{
    struct hdr_field *hdr = NULL;
    str name, val;
    char hname[255], hval[255];

    if (parse_headers(msg, HDR_EOH_F, 0) < 0)
    {
        LM_ERR("error parsing headers\n");
        return -1;
    }

    for (hdr=msg->headers; hdr; hdr=hdr->next)
    {
        if (hdr->name.len == 12 && strncasecmp(hdr->name.s, "Record-Route", 12)==0)
            continue;
        if (hdr->name.len == 3  && strncasecmp(hdr->name.s, "Via", 3)==0)
            continue;
        //LM_INFO("header[%.*s]: %.*s\n", hdr->name.len, hdr->name.s, hdr->body.len, hdr->body.s);

        memcpy(&hval, hdr->body.s, hdr->body.len);
        hval[hdr->body.len] = '\0';
        val.s = hval;
        val.len = hdr->body.len;

        memcpy(&hname, hdr->name.s, hdr->name.len);
        hname[hdr->name.len] = '\0';
        name.s = hname;
        name.len = hdr->name.len;

        if (pv_set_xavp(&xavp_name, &name, &val) < 0)
            break;
    }

    return 1;
}

static int pv_apply_headers(struct sip_msg* msg, char* _s1, char* _s2)
{
    sr_xavp_t *xavp = NULL;
    sr_xavp_t *sub = NULL;
    sr_xavp_t *list[64];
    int l_idx = 0;

    xavp = xavp_get(&xavp_name, NULL);
    if (xavp == NULL)
    {
        LM_ERR("missing xavp %s, run pv_collect_headers() first\n", xavp_name.s);
        return -1;
    }

    if (xavp->val.type != SR_XTYPE_XAVP)
    {
        LM_ERR("not xavp child type %s\n" , xavp_name.s);
        return -1;
    }

    if (xavp && xavp->val.type == SR_XTYPE_XAVP)
        sub = xavp->val.v.xavp;

    while (sub)
    {
        *(list+l_idx++) = sub;
        sub = sub->next;
    }

    while (--l_idx >= 0) {
        sub = *(list+l_idx);
        //LM_INFO("A: %s -- %s\n", sub->name.s, sub->val.v.s.s);
        sr_hdr_del_z(msg, sub->name.s);
        if (sub->val.type != SR_XTYPE_NULL)
            sr_hdr_add_zs(msg, sub->name.s, &sub->val.v.s);
    }

    return 1;
}

static int pv_check_header(struct sip_msg* _m, str* hname, char* _s2)
{
    if (xavp_get_child(&xavp_name, hname) == NULL)
        return -1;

    return 1;
}

static int pv_append_header(struct sip_msg* _m, str* hname, str* value)
{
    if (hname == NULL)
        return -1;

/*
    // return error if the header already already exists
    if (xavp_get_child(&xavp_name, hname) != NULL)
        return -1;
*/

    return pv_set_xavp(&xavp_name, hname, value);
}

static int pv_modify_header(struct sip_msg* _m, str* hname, str* value)
{
    if (hname == NULL)
        return -1;

/*
    // return error if the header does not exist
    if (xavp_get_child(&xavp_name, hname) == NULL)
        return -1;
*/

    return pv_set_xavp(&xavp_name, hname, value);
}

static int pv_remove_header(struct sip_msg* _m, str* hname, char* _s2)
{
    if (hname == NULL)
        return -1;

    // return error if the header does not exist
    if (xavp_get_child(&xavp_name, hname) == NULL)
        return -1;

    return pv_set_xavp(&xavp_name, hname, NULL);
}

static int pv_set_xavp(str *xname, str *name, str *val) {

    sr_xavp_t **xavp = NULL;
    sr_xavp_t *root = NULL;
    sr_xavp_t *new = NULL;
    sr_xavp_t *sub = NULL;
    sr_xval_t xval;
    int idx_f = 0;

    if (xname == NULL || name == NULL)
    {
        LM_ERR("missing xavp/pv name\n");
        return -1;
    }

    memset(&xval, 0, sizeof(sr_xval_t));
    if (val == NULL)
        xval.type = SR_XTYPE_NULL;
    else
        xval.type = SR_XTYPE_STR;
    if (val != NULL)
        xval.v.s = *val;

    //LM_INFO("SET: %s=>%s = %s\n", xname->s, name->s, xval.v.s.s);

    root = xavp_get(xname, NULL);
    xavp = root ? &root->val.v.xavp : &new;
    if (xavp)
        sub = xavp_get_child(xname, name);
    if (sub == NULL)
    {
        //LM_INFO("XAVP ADD\n");

        if (xavp_add_value(name, &xval, xavp) == NULL)
        {
            LM_ERR("error creating xavp=>name %s=>%s\n", xname->s, name->s);
            xavp_destroy_list(xavp);
            return -1;
        }
        if (root == NULL)
        {
            //LM_INFO("XAVP NEW\n");
            memset(&xval, 0, sizeof(sr_xval_t));
            xval.type = SR_XTYPE_XAVP;
            xval.v.xavp = *xavp;
            if(xavp_add_value(xname, &xval, NULL)==NULL)
            {
                LM_ERR("error creating xavp=>name %s=>%s\n", xname->s, name->s);
                xavp_destroy_list(xavp);
                return -1;
            }
        }
    } else {
        //LM_INFO("XAVP SET: %s -- %s -> %s\n", sub->name.s, sub->val.v.s.s, xval.v.s.s);
        if (!xavp_set_value(name, idx_f, &xval, xavp)) {
            LM_ERR("error setting xavp value xavp=>name %s=>%s\n", xname->s, name->s);
            return -1;
        }
    }

    return 1;
}

static int pv_free_xavp(str* xname) {
    xavp_rm_by_name(&xavp_name, 1, NULL);
    return 1;
}

