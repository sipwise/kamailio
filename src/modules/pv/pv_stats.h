/*
 * Copyright (C) 2001-2003 FhG Fokus
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
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

/*!
 * \file
 * \brief Headers for Stats Pseudo-variables
 */

#ifndef _PV_STATS_H_
#define _PV_STATS_H_

#include "../../core/pvar.h"

int pv_parse_stat_name(pv_spec_p sp, str *in);
int pv_get_stat(struct sip_msg *msg, pv_param_t *param, pv_value_t *res);

int pv_parse_sr_version_name(pv_spec_p sp, str *in);
int pv_get_sr_version(struct sip_msg *msg, pv_param_t *param, pv_value_t *res);

#endif
