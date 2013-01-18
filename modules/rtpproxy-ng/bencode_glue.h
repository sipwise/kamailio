#ifndef _BENCODE_GLUE_H_
#define _BENCODE_GLUE_H_

/* Glue code and convenience functions between kamailio-specific stuff and the generic bencode.h */

#include "bencode.h"
#include "../../str.h"

static inline bencode_item_t *bencode_dictionary_add_str(bencode_item_t *dict, const char *key, str *str) {
	return bencode_dictionary_add(dict, key, bencode_string_len(dict->buffer, str->s, str->len));
}
static inline int bencode_dictionary_get_str(str *out, bencode_item_t *dict, const char *key) {
	int len;
	const char *s;
	s = bencode_dictionary_get_string(dict, key, &len);
	if (!s)
		return -1;
	out->s = (void *) s;
	out->len = len;
	return 0;
}
static inline int bencode_dictionary_get_str_pkg(str *out, bencode_item_t *dict, const char *key) {
	int len;
	char *s;
	s = bencode_dictionary_get_string_dup(dict, key, &len);
	if (!s)
		return -1;
	out->s = s;
	out->len = len;
	return 0;
}

#endif
