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

#include "../../dprint.h"
#include "../../parser/parse_from.h"
#include "../../parser/parse_content.h"
#include "../../modules/tm/tm_load.h"
#include "../rr/api.h"
#include "../../flags.h"
#include "pcem_mod.h"
#include "pcem_logic.h"

extern struct tm_binds tmb;
extern struct rr_binds rrb;

#define is_pcem_flag_set(_rq,_flag)  (((_flag) != -1) && (isflagset((_rq), (_flag)) == 1))
#define reset_pcem_flag(_rq,_flag)   (resetflag((_rq), (_flag)))

#define is_all_on(_rq)  is_pcem_flag_set(_rq,pcem_all_flag)
#define is_qos_on(_rq)  is_pcem_flag_set(_rq,pcem_qos_flag)

static void tmcb_func( struct cell* t, int type, struct tmcb_params *ps );

static inline int pcem_preparse_req(struct sip_msg *req)
{
/*
	if((parse_headers(req,HDR_CALLID_F|HDR_CSEQ_F|HDR_FROM_F|HDR_TO_F,0)<0)
	   || (parse_from_header(req)<0 ) ) {
		LM_ERR("failed to preparse request\n");
		return -1;
	}
*/
	return 0;	
}

void pcem_onreq( struct cell* t, int type, struct tmcb_params *ps )
{
	int tmcb_types;
	int is_invite;

	LM_ERR("pcem_onreq called for t(%p) event type %d\n", t, type);

	if(ps->req && (is_all_on(ps->req) || is_qos_on(ps->req))) {
		LM_ERR("it's a request, is_all_on=%d, is_qos_on=%d, processing request\n",
			is_all_on(ps->req), is_qos_on(ps->req));

		if (pcem_preparse_req(ps->req)<0)
			return;

		is_invite = (ps->req->REQ_METHOD==METHOD_INVITE)?1:0;
	
		tmcb_types =
			/* get completed transactions */
			TMCB_RESPONSE_OUT |
			/* get incoming replies ready for processing */
			TMCB_RESPONSE_IN |
			/* get failed transactions */
			(is_invite?TMCB_ON_FAILURE:0);

		if (tmb.register_tmcb( 0, t, tmcb_types, tmcb_func, 0, 0 ) <= 0) {
			LM_ERR("cannot register additional callbacks\n");
			return;
		}

		/*
		if(!rrb.is_direction(ps->req,RR_FLOW_UPSTREAM) ) {
			LM_DBG("detected an UPSTREAM req -> flaging it\n");
			ps->req->msg_flags |= FL_REQ_UPSTREAM;
		}
		*/
	}
}


static inline void pcem_onreply_in(struct cell *t, struct sip_msg *req,
				struct sip_msg *reply, int code)
{
	LM_ERR("got a reply_in, code=%d\n", code);
}

static inline void pcem_onreply(struct cell *t, struct sip_msg *req,
				struct sip_msg *reply, int code)
{
	LM_ERR("got a reply, code=%d\n", code);
}

static inline void pcem_onfailure(struct cell *t, struct sip_msg *req,
				struct sip_msg *reply, int code)
{
	LM_ERR("got a failure\n");
}

static void tmcb_func( struct cell* t, int type, struct tmcb_params *ps )
{
	LM_ERR("pcem callback called for t(%p) event type %d, reply code %d\n",
			t, type, ps->code);
	if (type&TMCB_RESPONSE_OUT) {
		pcem_onreply( t, ps->req, ps->rpl, ps->code);
	} else if (type&TMCB_ON_FAILURE) {
		pcem_onfailure( t, ps->req, ps->rpl, ps->code);
	} else if (type&TMCB_RESPONSE_IN) {
		pcem_onreply_in( t, ps->req, ps->rpl, ps->code);
	}
}

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

#include "../../dprint.h"
#include "../../parser/parse_from.h"
#include "../../parser/parse_content.h"
#include "../../modules/tm/tm_load.h"
#include "../rr/api.h"
#include "../../flags.h"
#include "pcem_mod.h"
#include "pcem_logic.h"

extern struct tm_binds tmb;
extern struct rr_binds rrb;

#define is_pcem_flag_set(_rq,_flag)  (((_flag) != -1) && (isflagset((_rq), (_flag)) == 1))
#define reset_pcem_flag(_rq,_flag)   (resetflag((_rq), (_flag)))

#define is_all_on(_rq)  is_pcem_flag_set(_rq,pcem_all_flag)
#define is_qos_on(_rq)  is_pcem_flag_set(_rq,pcem_qos_flag)

static void tmcb_func( struct cell* t, int type, struct tmcb_params *ps );

static inline int pcem_preparse_req(struct sip_msg *req)
{
/*
	if((parse_headers(req,HDR_CALLID_F|HDR_CSEQ_F|HDR_FROM_F|HDR_TO_F,0)<0)
	   || (parse_from_header(req)<0 ) ) {
		LM_ERR("failed to preparse request\n");
		return -1;
	}
*/
	return 0;	
}

void pcem_onreq( struct cell* t, int type, struct tmcb_params *ps )
{
	int tmcb_types;
	int is_invite;

	LM_ERR("pcem_onreq called for t(%p) event type %d\n", t, type);

	if(ps->req && (is_all_on(ps->req) || is_qos_on(ps->req))) {
		LM_ERR("it's a request, is_all_on=%d, is_qos_on=%d, processing request\n",
			is_all_on(ps->req), is_qos_on(ps->req));

		if (pcem_preparse_req(ps->req)<0)
			return;

		is_invite = (ps->req->REQ_METHOD==METHOD_INVITE)?1:0;
	
		tmcb_types =
			/* get completed transactions */
			TMCB_RESPONSE_OUT |
			/* get incoming replies ready for processing */
			TMCB_RESPONSE_IN |
			/* get failed transactions */
			(is_invite?TMCB_ON_FAILURE:0);

		if (tmb.register_tmcb( 0, t, tmcb_types, tmcb_func, 0, 0 ) <= 0) {
			LM_ERR("cannot register additional callbacks\n");
			return;
		}

		/*
		if(!rrb.is_direction(ps->req,RR_FLOW_UPSTREAM) ) {
			LM_DBG("detected an UPSTREAM req -> flaging it\n");
			ps->req->msg_flags |= FL_REQ_UPSTREAM;
		}
		*/
	}
}


static inline void pcem_onreply_in(struct cell *t, struct sip_msg *req,
				struct sip_msg *reply, int code)
{
	LM_ERR("got a reply_in, code=%d\n", code);
}

static inline void pcem_onreply(struct cell *t, struct sip_msg *req,
				struct sip_msg *reply, int code)
{
	LM_ERR("got a reply, code=%d\n", code);
}

static inline void pcem_onfailure(struct cell *t, struct sip_msg *req,
				struct sip_msg *reply, int code)
{
	LM_ERR("got a failure\n");
}

static void tmcb_func( struct cell* t, int type, struct tmcb_params *ps )
{
	LM_ERR("pcem callback called for t(%p) event type %d, reply code %d\n",
			t, type, ps->code);
	if (type&TMCB_RESPONSE_OUT) {
		pcem_onreply( t, ps->req, ps->rpl, ps->code);
	} else if (type&TMCB_ON_FAILURE) {
		pcem_onfailure( t, ps->req, ps->rpl, ps->code);
	} else if (type&TMCB_RESPONSE_IN) {
		pcem_onreply_in( t, ps->req, ps->rpl, ps->code);
	}
}

