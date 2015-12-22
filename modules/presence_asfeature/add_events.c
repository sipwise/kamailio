#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libxml/parser.h>
#include "../../parser/parse_content.h"
#include "../presence/event_list.h"
#include "../pua/pua.h"
#include "presence_asfeature.h"
#include "add_events.h"

static str pu_415_rpl  = str_init("Unsupported media type");
static str unk_dev = str_init("<notKnown/>");
static str content_type =str_init("application/x-as-feature-event+xml");
// -4
static str dnd_xml = str_init("<?xml version='1.0' encoding='ISO-8859-1'?><DoNotDisturbEvent><device>%s</device><doNotDisturbOn>%s</doNotDisturbOn></DoNotDisturbEvent>");
// -8
static str fwd_xml = str_init("<?xml version='1.0' encoding='ISO-8859-1'?><ForwardingEvent><device>%s</device><forwardingType>%s</forwardingType><forwardStatus>%s</forwardStatus><forwardTo>%s</forwardTo></ForwardingEvent>");

int asfeature_add_events(void)
{
	pres_ev_t event;
	
	/* constructing message-summary event */
	memset(&event, 0, sizeof(pres_ev_t));
	event.name.s = "as-feature-event";
	event.name.len = 16;

	event.content_type.s = "application/x-as-feature-event+xml";
	event.content_type.len = 34;
	event.default_expires= 3600;
	event.type = PUBL_TYPE;
	event.req_auth = 0;
	event.evs_publ_handl = asfeature_publ_handler;
	event.evs_subs_handl = asfeature_subs_handler;
//	event.etag_not_new;
//	get_rules_doc_t* get_rules_doc;
//	get_pidf_doc_t* get_pidf_doc;
//	apply_auth_t*  apply_auth_nbody;
//	is_allowed_t*  get_auth_status;
//	agg_nbody_t* agg_nbody;
//	free_body_t* free_body;
//	aux_body_processing_t* aux_body_processing;
//	free_body_t* aux_free_body;
//	struct pres_ev* wipeer;
//	struct pres_ev* next;

	if (pres.add_event(&event) < 0) {
		LM_ERR("failed to add event \"as-feature-event\"\n");
		return -1;
	}		
	return 0;
}

int asfeature_publ_handler(struct sip_msg* msg) {
	str body= {0, 0};
	xmlDocPtr doc= NULL;

	LM_ERR("asfeature_publ_handl start\n");
	if ( get_content_length(msg) == 0 )
		return 1;
	
	body.s=get_body(msg);
	if (body.s== NULL) {
		LM_ERR("cannot extract body from msg\n");
		goto error;
	}
	/* content-length (if present) must be already parsed */

	body.len = get_content_length( msg );
	doc= xmlParseMemory( body.s, body.len );
	if(doc== NULL)
	{
		LM_ERR("bad body format\n");
		if(slb.freply(msg, 415, &pu_415_rpl) < 0)
		{
			LM_ERR("while sending '415 Unsupported media type' reply\n");
		}
		goto error;
	}
	xmlFreeDoc(doc);
	xmlCleanupParser();
	xmlMemoryDump();
	return 1;

error:
	xmlFreeDoc(doc);
	xmlCleanupParser();
	xmlMemoryDump();
	return -1;
}
int asfeature_subs_handler(struct sip_msg* msg) {
	str body= {0, 0};
	xmlDocPtr doc= NULL;
	xmlNodePtr top_elem= NULL;
	xmlNodePtr param = NULL;
	char *dndact=NULL,*fwdact=NULL,*fwdtype=NULL,*fwdDN=NULL,*device=NULL;
	publ_info_t publ;
	str pres_uri;
	char id_buf[512];
	int id_buf_len;




	LM_ERR("asfeature_subs_handl start\n");
	pres_uri.s = msg->first_line.u.request.uri.s;
	pres_uri.len = msg->first_line.u.request.uri.len;

	if ( get_content_length(msg) == 0 ){
		LM_ERR("no body. (ok for initial)\n");
		return 1;
	}
	body.s=get_body(msg);
	if (body.s== NULL)
	{
		LM_ERR("cannot extract body from msg\n");
		goto error;
	}
	/* content-length (if present) must be already parsed */

	body.len = get_content_length( msg );
	doc=xmlParseMemory( body.s, body.len );
	if(doc== NULL)
	{
		LM_ERR("bad body format\n");
		if(slb.freply(msg, 415, &pu_415_rpl) < 0)
		{
			LM_ERR("while sending '415 Unsupported media type' reply\n");
		}
		goto error;
	}
	top_elem=libxml_api.xmlDocGetNodeByName(doc, "SetDoNotDisturb", NULL);
	if(top_elem != NULL) {
		LM_ERR(" got SetDoNotDisturb\n");
		param = libxml_api.xmlNodeGetNodeByName(top_elem, "doNotDisturbOn", NULL);
		if(param!= NULL) {
			dndact= (char*)xmlNodeGetContent(param);
			if(dndact== NULL)  {
				LM_ERR("while extracting value from 'doNotDisturbOn' in 'SetDoNotDisturb'\n");
				goto error;
			}
			LM_ERR("got 'doNotDisturbOn'=%s in 'SetDoNotDisturb'\n",dndact);
		}
		param = libxml_api.xmlNodeGetNodeByName(top_elem, "device", NULL);
		if(param!= NULL) {
			device= (char*)xmlNodeGetContent(param);
			if(device== NULL)  {
				LM_ERR("while extracting value from 'device' in 'SetDoNotDisturb'\n");
				goto error;
			}
			if (strlen(device)==0)
			    device=unk_dev.s;
			LM_ERR("got 'device'=%s in 'SetDoNotDisturb'\n",device);
		}
		body.len=dnd_xml.len -4 +strlen(dndact)+strlen(device);
		body.s=pkg_malloc(body.len+1);
		if(body.s== NULL)  {
			LM_ERR("while extracting allocating body for publish in 'SetDoNotDisturb'\n");
			goto error;
		}
		sprintf(body.s,dnd_xml.s,device,dndact);
		LM_ERR("body for dnd publish is %d, %s\n",body.len,body.s);
		memset(&publ, 0, sizeof(publ_info_t));
		publ.pres_uri = &pres_uri;
		publ.body = &body;
		id_buf_len = snprintf(id_buf, sizeof(id_buf), "asfeature_PUBLISH.%.*s",
			pres_uri.len, pres_uri.s);
		LM_ERR("ID = %.*s\n",id_buf_len,id_buf);
		publ.id.s = id_buf;
		publ.id.len = id_buf_len;
		publ.content_type = content_type;
		publ.expires = 3600;
		
		/* make UPDATE_TYPE, as if this "publish dialog" is not found.
		   by pua it will fallback to INSERT_TYPE anyway */
		publ.flag|= INSERT_TYPE;
		publ.source_flag |= ASFEATURE_PUBLISH;
		publ.event |= ASFEATURE_EVENT;
		publ.extra_headers= NULL;

		if(pua.send_publish(&publ) < 0) {
			LM_ERR("error while sending publish\n");
			pkg_free(body.s);
			goto error;
		}
		pkg_free(body.s);
	}
	top_elem=libxml_api.xmlDocGetNodeByName(doc, "SetForwarding", NULL);
	if(top_elem != NULL) {
		LM_ERR(" got SetForwarding\n");
		param = libxml_api.xmlNodeGetNodeByName(top_elem, "forwardDN", NULL);
		if(param!= NULL) {
			fwdDN= (char*)xmlNodeGetContent(param);
			if(fwdDN== NULL) {
				LM_ERR("while extracting value from 'forwardDN' in 'SetForwarding'\n");
				goto error;
			}
			LM_ERR("got 'forwardDN'=%s in 'SetForwarding'\n",fwdDN);
		}
		param = libxml_api.xmlNodeGetNodeByName(top_elem, "forwardingType", NULL);
		if(param!= NULL) {
			fwdtype= (char*)xmlNodeGetContent(param);
			if(fwdtype== NULL) {
				LM_ERR("while extracting value from 'forwardingType' in 'SetForwarding'\n");
				goto error;
			}
			LM_ERR("got 'forwardingType'=%s in 'SetForwarding'\n",fwdtype);
		}
		param = libxml_api.xmlNodeGetNodeByName(top_elem, "activateForward", NULL);
		if(param!= NULL) {
			fwdact= (char*)xmlNodeGetContent(param);
			if(fwdact== NULL) {
				LM_ERR("while extracting value from 'activateForward' in 'SetForwarding'\n");
				goto error;
			}
			LM_ERR("got 'activateForward'=%s in 'SetForwarding'\n",fwdact);
		}
		param = libxml_api.xmlNodeGetNodeByName(top_elem, "device", NULL);
		if(param!= NULL) {
			device= (char*)xmlNodeGetContent(param);
			if(device== NULL)  {
				LM_ERR("while extracting value from 'device' in 'SetForwarding'\n");
				goto error;
			}
			LM_ERR("got 'device'=%s in 'SetDoNotDisturb'\n",device);
		}
		body.len=fwd_xml.len -8 + strlen(device) + strlen(device) +strlen(fwdtype) + strlen(fwdact) +strlen(fwdDN);
		body.s=pkg_malloc(body.len+1);
		if(body.s== NULL)  {
			LM_ERR("while extracting allocating body for publish in 'SetForwarding'\n");
			goto error;
		}
		sprintf(body.s,fwd_xml.s,device,fwdtype,fwdact,fwdDN);
		LM_ERR("body for dnd publish is %d %s\n",body.len,body.s);
		memset(&publ, 0, sizeof(publ_info_t));
		publ.pres_uri = &pres_uri;
		publ.body = &body;
		id_buf_len = snprintf(id_buf, sizeof(id_buf), "ASFEATURE_PUBLISH.%.*s",
			pres_uri.len, pres_uri.s);
		LM_ERR("ID = %.*s\n",id_buf_len,id_buf);
		publ.id.s = id_buf;
		publ.id.len = id_buf_len;
		publ.content_type = content_type;
		publ.expires = 3600;
		
		/* make UPDATE_TYPE, as if this "publish dialog" is not found.
		   by pua it will fallback to INSERT_TYPE anyway */
		publ.flag|= INSERT_TYPE;
		publ.source_flag |= ASFEATURE_PUBLISH;
		publ.event |= ASFEATURE_EVENT;
		publ.extra_headers= NULL;

		if(pua.send_publish(&publ) < 0) {
			LM_ERR("error while sending publish\n");
			pkg_free(body.s);
			goto error;
		}
		pkg_free(body.s);
	}

	xmlFreeDoc(doc);
	xmlCleanupParser();
	xmlMemoryDump();
	return 1;

error:
	xmlFreeDoc(doc);
	xmlCleanupParser();
	xmlMemoryDump();
	return -1;

}
