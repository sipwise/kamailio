#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <swrate/swrate.h>
#include "../../sr_module.h"
#include "../../mod_fix.h"
#include "../../pvar.h"
#include "../../mem/mem.h"
#include "../../mem/shm_mem.h"

MODULE_VERSION

struct peer {
	unsigned int id;
	double cost;
	unsigned int weight;
	str s;
};

static void mod_destroy();
static int mod_init();
static int child_init(int rank);

static int lcr_rate(sip_msg_t *msg, char *su, char *sq);

static cmd_export_t cmds[] = {
	{"lcr_rate", (cmd_function)lcr_rate, 2, fixup_spve_spve, 0,
	REQUEST_ROUTE | FAILURE_ROUTE},
	{0,}
};

static char *gw_uri_avp_param;
static int gw_uri_avp_type;
static int_str gw_uri_avp;

static char *db_host;
static unsigned int db_port;
static char *db_user;
static char *db_pass;
static char *db_db;

static param_export_t params[] = {
	{"gw_uri_avp",		STR_PARAM, &gw_uri_avp_param},
	{"db_host",		STR_PARAM, &db_host},
	{"db_port",		INT_PARAM, &db_port},
	{"db_user",		STR_PARAM, &db_user},
	{"db_pass",		STR_PARAM, &db_pass},
	{"db_db",		STR_PARAM, &db_db},
	{0,},
};

static int swrate_done;
static SWRATE swrate_handle;

struct module_exports exports = {
	"lcr_rate",
	DEFAULT_DLFLAGS,
	cmds,
	params,
	0,
	0,
	0,
	0,
	mod_init,
	0,
	mod_destroy,
	child_init
};

static int mod_init() {
	pv_spec_t avp_spec;
	str s;
	unsigned short avp_flags;

	if (!gw_uri_avp_param || !*gw_uri_avp_param) {
		LM_ERR("gw_uri_avp not set\n");
		return -1;
	}

	s.s = gw_uri_avp_param;
	s.len = strlen(s.s);

	if (!pv_parse_spec(&s, &avp_spec) || avp_spec.type != PVT_AVP) {
		LM_ERR("malformed or non AVP definition <%s>\n", gw_uri_avp_param);
		return -1;
	}

	if (pv_get_avp_name(0, &(avp_spec.pvp), &gw_uri_avp, &avp_flags)) {
		LM_ERR("invalid AVP definition <%s>\n", gw_uri_avp_param);
		return -1;
	}
	gw_uri_avp_type = avp_flags;

	return 0;
}

static int child_init(int rank) {
	return 0;
}

static void mod_destroy() {
	;
}

static int check_swrate_init() {
	if (swrate_done)
		return 0;
	if (swrate_init(&swrate_handle, db_host, db_port, db_db, db_user, db_pass, NULL, 0, 1, 0)) {
		LM_ERR("failed to initialized libswrate\n");
		return -1;
	}
	swrate_done = 1;
	return 0;
}

struct peer *load_peers(int *num, str *user, str *domain) {
	struct usr_avp *avp;
	int_str val;
	struct peer *ret, *j;
	int len, i;
	char *c;
	str s;
	swr_rate_t rate;
	time_t now;

	len = 4;
	ret = pkg_malloc(len * sizeof(*ret));
	if (!ret) {
		LM_ERR("out of pkg memory\n");
		return NULL;
	}
	i = 0;
	time(&now);

	while (1) {
		avp = search_first_avp(gw_uri_avp_type, gw_uri_avp, &val, 0);
		if (!avp)
			break;

		if (i == len) {
			len <<= 1;
			j = pkg_realloc(ret, len * sizeof(*ret));
			if (!j) {
				pkg_free(ret);
				LM_ERR("out of pkg memory\n");
				return NULL;
			}
			ret = j;
		}

		j = &ret[i];

		j->s.len = val.s.len;
		j->s.s = pkg_malloc(val.s.len);
		if (!j->s.s) {
			pkg_free(ret);
			LM_ERR("out of pkg memory\n");
			return NULL;
		}
		memcpy(j->s.s, val.s.s, val.s.len);
		c = memrchr(j->s.s, '|', val.s.len);
		if (!c) {
			pkg_free(ret);
			LM_ERR("separator not found in string <%.*s>\n", val.s.len, j->s.s);
			return NULL;
		}

		c++;
		s.s = c;
		s.len = val.s.len - (c - j->s.s);
		if (str2int(&s, &j->id)) {
			pkg_free(ret);
			LM_ERR("could not convert string <%.*s> to int\n", s.len, s.s);
			return NULL;
		}

		j->weight = i;

		if (swrate_get_peer_rate(&rate, &swrate_handle, j->id, user->s, domain->s, now)) {
			pkg_free(ret);
			LM_ERR("failed to get rate for call, peer id %u, user <%.*s>@<%.*s>\n",
				j->id, user->len, user->s, domain->len, domain->s);
			return NULL;
		}
		j->cost = rate.init_rate;

		destroy_avp(avp);
		i++;
	}

	*num = i;
	return ret;
}

static int peers_cmp(const void *aa, const void *bb) {
	const struct peer *a = aa, *b = bb;

	if (a->cost < b->cost)
		return -1;
	if (a->cost > b->cost)
		return 1;
	if (a->weight < b->cost)
		return -1;
	return 1;
}

static int save_peers(struct peer *peers, int num) {
	int i;
	int_str val;

	for (i = 0; i < num; i++) {
		val.s = peers[i].s;
		if (add_avp(gw_uri_avp_type|AVP_VAL_STR, gw_uri_avp, val))
			LM_ERR("add_avp failed\n");
		pkg_free(val.s.s);
	}

	pkg_free(peers);
	return 0;
}

static int lcr_rate(sip_msg_t *msg, char *su, char *sq) {
	struct peer *peers;
	int num_peers;
	str user, domain;

	if (check_swrate_init())
		return -1;

	if (fixup_get_svalue(msg, (gparam_t *) su, &user)) {
		LM_ERR("failed to get user parameter\n");
		return -1;
	}
	if (fixup_get_svalue(msg, (gparam_t *) sq, &domain)) {
		LM_ERR("failed to get domain parameter\n");
		return -1;
	}

	peers = load_peers(&num_peers, &user, &domain);
	if (!peers)
		return -1;
	qsort(peers, num_peers, sizeof(*peers), peers_cmp);
	save_peers(peers, num_peers);

	return 0;
}
