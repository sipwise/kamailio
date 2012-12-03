#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "../../sr_module.h"
#include "../../mod_fix.h"

MODULE_VERSION

static void mod_destroy();
static int mod_init();
static int child_init(int rank);

static int lcr_rate(sip_msg_t *msg, char *su, char *sq);

static cmd_export_t cmds[] = {
	{"lcr_rate", (cmd_function)lcr_rate, 1, 0, 0,
	REQUEST_ROUTE | FAILURE_ROUTE},
	{0,}
};

struct module_exports exports = {
	"lcr_rate",
	DEFAULT_DLFLAGS,
	cmds,
	0,
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
	return 0;
}

static int child_init(int rank) {
	return 0;
}

static void mod_destroy() {
	;
}

static int lcr_rate(sip_msg_t *msg, char *su, char *sq) {
	return 0;
}
