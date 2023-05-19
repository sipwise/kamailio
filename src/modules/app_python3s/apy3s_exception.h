/*
 * Copyright (C) 2009 Sippy Software, Inc., http://www.sippysoft.com
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
 *
*/

#ifndef _PYTHON_SUPPORT_H
#define  _PYTHON_SUPPORT_H

#include <Python.h>
#include <stdarg.h>

extern PyObject *_sr_apy3s_format_exc_obj;

void apy3s_handle_exception(const char *, ...);

PyObject *InitTracebackModule(void);
#if PY_VERSION_HEX >= 0x03070000
const char *get_class_name(PyObject *);
const char *get_instance_class_name(PyObject *);
#else
char *get_class_name(PyObject *);
char *get_instance_class_name(PyObject *);
#endif

#endif
