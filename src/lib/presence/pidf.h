/* 
 * Copyright (C) 2005 iptelorg GmbH
 *
 * This file is part of ser, a free SIP server.
 *
 * ser is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version
 *
 * For a license to use the ser software under conditions
 * other than those described here, or to purchase support for this
 * software, please contact iptel.org by e-mail at the following addresses:
 *    info@iptel.org
 *
 * ser is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

#ifndef __PRESENCE_PIDF_H
#define __PRESENCE_PIDF_H

#include <cds/sstr.h>
#include <presence/pres_doc.h>

int create_pidf_document(presentity_info_t *p, str_t *dst, str_t *dst_content_type);
int create_cpim_pidf_document(presentity_info_t *p, str_t *dst, str_t *dst_content_type);

int parse_pidf_document(presentity_info_t **dst, const char *data, int data_len);
int parse_cpim_pidf_document(presentity_info_t **dst, const char *data, int data_len);

#endif
