/*
 * TLS module
 *
 * Copyright (C) 2005,2006 iptelorg GmbH
 *
 * Permission to use, copy, modify, and distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

/*!
 * \file
 * \brief Kamailio TLS support :: OpenSSL initialization functions
 * \ingroup tls
 * Module: \ref tls
 */


#ifndef _TLS_INIT_H
#define _TLS_INIT_H

#include "../../core/ip_addr.h"
#include "tls_domain.h"

typedef struct sr_tls_methods_s
{
	const WOLFSSL_METHOD *TLSMethod;
	int TLSMethodMin;
	int TLSMethodMax;
} sr_tls_methods_t;
extern sr_tls_methods_t sr_tls_methods[];

/*
 * just once, pre-initialize the tls subsystem
 */
int tls_pre_init(void);

/**
 * just once, prepare for init of all modules
 */
int tls_h_mod_pre_init_f(void);

/*
 * just once, initialize the tls subsystem after all mod inits
 */
int tls_h_mod_init_f(void);


/*
 * just once before final cleanup
 */
void tls_h_mod_destroy_f(void);


/*
 * for each socket
 */
int tls_h_init_si_f(struct socket_info *si);

/*
 * Make sure that all server domains in the configuration have corresponding
 * listening socket in SER
 */
int tls_check_sockets(tls_domains_cfg_t *cfg);

#endif /* _TLS_INIT_H */
