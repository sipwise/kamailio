/*
 * Kamailio TLS module
 *
 * Copyright (C) 2010 iptelorg GmbH
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

/**
 * openssl BIOs for reading/writing via a fixed memory buffer.
 * @file
 * @ingroup tls
 */

#include "tls_bio.h"
#include "../../core/compiler_opt.h"
#include "../../core/dprint.h"
#include "../../core/ut.h"
#include "tls_cfg.h"

/* 0xf2 should be unused (as of openssl 1.0.0 max.
   internal defined BIO is 23) */
#define BIO_TYPE_TLS_MBUF 0x4f2

/* debugging */
#ifdef NO_TLS_BIO_DEBUG
#undef TLS_BIO_DEBUG
#endif
#ifdef TLS_BIO_DEBUG
#ifdef __SUNPRO_C
#define TLS_BIO_DBG(...)                                   \
	LOG_FP(DEFAULT_FACILITY, cfg_get(tls, tls_cfg, debug), \
			"tls_BIO: " LOC_INFO, __VA_ARGS__)
#else
#define TLS_BIO_DBG(args...)                               \
	LOG_FP(DEFAULT_FACILITY, cfg_get(tls, tls_cfg, debug), \
			"tls_BIO: " LOC_INFO, ##args)
#endif /* __SUNPRO_c */
#else  /* TLS_BIO_DEBUG */
#ifdef __SUNPRO_C
#define TLS_BIO_DBG(...)
#else
#define TLS_BIO_DBG(fmt, args...)
#endif /* __SUNPRO_c */
#endif /* TLS_BIO_DEBUG */


static int tls_bio_mbuf_new(WOLFSSL_BIO *b);
static int tls_bio_mbuf_free(WOLFSSL_BIO *b);
static int tls_bio_mbuf_write(WOLFSSL_BIO *b, const char *buf, int num);
static int tls_bio_mbuf_read(WOLFSSL_BIO *b, char *buf, int num);
static int tls_bio_mbuf_puts(WOLFSSL_BIO *b, const char *s);
static long tls_bio_mbuf_ctrl(WOLFSSL_BIO *b, int cmd, long arg1, void *arg2);


static WOLFSSL_BIO_METHOD *tls_mbuf_method = NULL;


/** returns a custom tls_mbuf BIO. */
WOLFSSL_BIO_METHOD *tls_BIO_mbuf(void)
{
	if(tls_mbuf_method != NULL) {
		return tls_mbuf_method;
	}
	tls_mbuf_method = wolfSSL_BIO_meth_new(BIO_TYPE_TLS_MBUF, "sr_tls_mbuf");
	if(tls_mbuf_method == NULL) {
		LM_ERR("cannot get a new bio method structure\n");
		return NULL;
	}
	wolfSSL_BIO_meth_set_write(tls_mbuf_method, tls_bio_mbuf_write);
	wolfSSL_BIO_meth_set_read(tls_mbuf_method, tls_bio_mbuf_read);
	wolfSSL_BIO_meth_set_puts(tls_mbuf_method, tls_bio_mbuf_puts);
	wolfSSL_BIO_meth_set_gets(tls_mbuf_method, NULL);
	wolfSSL_BIO_meth_set_ctrl(tls_mbuf_method, tls_bio_mbuf_ctrl);
	wolfSSL_BIO_meth_set_create(tls_mbuf_method, tls_bio_mbuf_new);
	wolfSSL_BIO_meth_set_destroy(tls_mbuf_method, tls_bio_mbuf_free);
	return tls_mbuf_method;
}


/** create an initialize a new tls_BIO_mbuf.
 * @return new BIO on success (!=0), 0 on error.
 */
WOLFSSL_BIO *tls_BIO_new_mbuf(struct tls_mbuf *rd, struct tls_mbuf *wr)
{
	WOLFSSL_BIO *ret;

	TLS_BIO_DBG("tls_BIO_new_mbuf called (%p, %p)\n", rd, wr);
	ret = wolfSSL_BIO_new(tls_BIO_mbuf());
	if(unlikely(ret == 0))
		return 0;
	if(unlikely(tls_BIO_mbuf_set(ret, rd, wr) == 0)) {
		wolfSSL_BIO_free(ret);
		return 0;
	}
	return ret;
}


/** sets the read and write mbuf for an  mbuf BIO.
 * @return 1 on success, 0 on error (openssl BIO convention).
 */
int tls_BIO_mbuf_set(WOLFSSL_BIO *b, struct tls_mbuf *rd, struct tls_mbuf *wr)
{
	struct tls_bio_mbuf_data *d;

	TLS_BIO_DBG("tls_BIO_mbuf_set called (%p => %p, %p)\n", b, rd, wr);
	d = wolfSSL_BIO_get_data(b);
	if(unlikely(d == 0)) {
		BUG("null BIO ptr data\n");
		return 0;
	}
	d->rd = rd;
	d->wr = wr;
	wolfSSL_BIO_set_init(b, 1);
	return 1;
}


/** create a new BIO.
 * (internal openssl use via the tls_mbuf method)
 * @return 1 on success, 0 on error.
 */
static int tls_bio_mbuf_new(WOLFSSL_BIO *b)
{
	struct tls_bio_mbuf_data *d;

	TLS_BIO_DBG("tls_bio_mbuf_new called (%p)\n", b);
	wolfSSL_BIO_set_init(b, 0);
	wolfSSL_BIO_set_data(b, NULL);
	d = wolfSSL_Malloc(sizeof(*d));
	memset(d, 0, sizeof(*d));
	if(unlikely(d == 0))
		return 0;
	wolfSSL_BIO_set_data(b, d);
	return 1;
}


/** destroy a tls mbuf BIO.
 * (internal openssl use via the tls_mbuf method)
 * @return 1 on success, 0 on error.
 */
static int tls_bio_mbuf_free(WOLFSSL_BIO *b)
{
	TLS_BIO_DBG("tls_bio_mbuf_free called (%p)\n", b);
	if(unlikely(b == 0))
		return 0;
	do {
		struct tls_bio_mbuf_data *d;
		d = wolfSSL_BIO_get_data(b);
		if(likely(d)) {
			wolfSSL_OPENSSL_free(d);
			wolfSSL_BIO_set_data(b, NULL);
			wolfSSL_BIO_set_init(b, 0);
		}
	} while(0);
	return 1;
}


/** read from a mbuf.
 * (internal openssl use via the tls_mbuf method)
 * @return bytes read on success (0< ret <=dst_len), -1 on empty buffer & sets
 *  should_retry_read, -1 on some other errors (w/o should_retry_read set).
 */
static int tls_bio_mbuf_read(WOLFSSL_BIO *b, char *dst, int dst_len)
{
	struct tls_bio_mbuf_data *d;
	struct tls_mbuf *rd;
	int ret;

	ret = 0;
	if(likely(dst)) {
		d = wolfSSL_BIO_get_data(b);
		wolfSSL_BIO_clear_retry_flags(b);
		if(unlikely(d == 0 || d->rd->buf == 0)) {
			if(d == 0)
				BUG("tls_BIO_mbuf %p: read called with null b->ptr\n", b);
			else {
				/* this form of calling read with a null buffer is used
				   as a shortcut when no data is available =>
				   simulate EAGIAN/WANT_READ */
				TLS_BIO_DBG("read (%p, %p, %d) called with null read buffer"
							"(%p->%p) => simulating EAGAIN/WANT_READ\n",
						b, dst, dst_len, d, d->rd);
				BIO_set_retry_read(b);
			}
			return -1;
		}
		rd = d->rd;
		if(unlikely(rd->used == rd->pos && dst_len)) {
			/* mimic non-blocking read behaviour */
			TLS_BIO_DBG("read (%p, %p, %d) called with full rd (%d)"
						" => simulating EAGAIN/WANT_READ\n",
					b, dst, dst_len, rd->used);
			BIO_set_retry_read(b);
			return -1;
		}
		ret = MIN_int(rd->used - rd->pos, dst_len);
		/* copy data from rd.buf into dst */
		memcpy(dst, rd->buf + rd->pos, ret);
		TLS_BIO_DBG("read(%p, %p, %d) called with rd=%p pos=%d => %d bytes\n",
				b, dst, dst_len, rd->buf, rd->pos, ret);
		rd->pos += ret;
		/*		if (unlikely(rd->pos < rd->used))
			wolfSSL_BIO_set_retry_read(b);
*/
	}
	return ret;
}


/** write to a mbuf.
 * (internal openssl use via the tls_mbuf method)
 * @return bytes written on success (0<= ret <=src_len), -1 on error or buffer
 * full (in this case sets should_retry_write).
 */
static int tls_bio_mbuf_write(WOLFSSL_BIO *b, const char *src, int src_len)
{
	struct tls_bio_mbuf_data *d;
	struct tls_mbuf *wr;
	int ret;

	ret = 0;
	d = wolfSSL_BIO_get_data(b);
	wolfSSL_BIO_clear_retry_flags(b);
	if(unlikely(d == 0 || d->wr->buf == 0)) {
		if(d == 0)
			BUG("tls_BIO_mbuf %p: write called with null b->ptr\n", b);
		else {
			/* this form of calling write with a null buffer is used
			   as a shortcut when no data is available =>
			   simulate EAGAIN/WANT_WRITE */
			TLS_BIO_DBG("write (%p, %p, %d) called with null buffer"
						" => simulating WANT_WRITE\n",
					b, src, src_len);
			BIO_set_retry_write(b);
		}
		return -1;
	}
	wr = d->wr;
	if(unlikely(wr->size == wr->used && src_len)) {
		/* mimic non-blocking socket behaviour */
		TLS_BIO_DBG("write (%p, %p, %d) called with full wr buffer (%d)"
					" => simulating WANT_WRITE\n",
				b, src, src_len, wr->used);
		BIO_set_retry_write(b);
		return -1;
	}
	ret = MIN_int(wr->size - wr->used, src_len);
	memcpy(wr->buf + wr->used, src, ret);
	wr->used += ret;
	/*	if (unlikely(ret < src_len))
		wolfSSL_BIO_set_retry_write();
*/
	TLS_BIO_DBG("write called (%p, %p, %d) => %d\n", b, src, src_len, ret);
	return ret;
}


static long tls_bio_mbuf_ctrl(WOLFSSL_BIO *b, int cmd, long arg1, void *arg2)
{
	long ret;
	ret = 0;
	switch(cmd) {
		case BIO_CTRL_GET_CLOSE:
		case BIO_CTRL_SET_CLOSE:
			ret = 0;
			break;
		case BIO_CTRL_DUP:
		case BIO_CTRL_FLUSH:
			ret = 1;
			break;
		case BIO_CTRL_RESET:
		case BIO_CTRL_INFO:
		case BIO_CTRL_PENDING:
		case BIO_CTRL_WPENDING:
		default:
			ret = 0;
			break;
	}
	TLS_BIO_DBG(
			"ctrl called (%p, %d, %ld, %p) => %ld\n", b, cmd, arg1, arg2, ret);
	return ret;
}


static int tls_bio_mbuf_puts(WOLFSSL_BIO *b, const char *s)
{
	int len;

	TLS_BIO_DBG("puts called (%p, %s)\n", b, s);
	len = strlen(s);
	return tls_bio_mbuf_write(b, s, len);
}

/* vi: set ts=4 sw=4 tw=79:ai:cindent: */
