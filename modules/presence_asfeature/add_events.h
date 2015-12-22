#ifndef _ASFEATURE_ADD_EV_H_
#define _ASFEATURE_ADD_EV_H_

int asfeature_add_events(void);
int	asfeature_publ_handler(struct sip_msg* msg);
int	asfeature_subs_handler(struct sip_msg* msg);
#endif
