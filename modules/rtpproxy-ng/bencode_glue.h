#ifndef _BENCODE_GLUE_H_
#define _BENCODE_GLUE_H_

/* Glue code and convenience functions between kamailio-specific stuff and the generic bencode.h */

#include "bencode.h"
#include "../../str.h"

static inline bencode_item_t *bencode_dictionary_add_str(bencode_item_t *dict, const char *key, str *str) {
	return bencode_dictionary_add(dict, key, bencode_string_len(dict->buffer, str->s, str->len));
}

#endif
