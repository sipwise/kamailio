/*
 * SNMPStats Module
 * Copyright (C) 2006 SOMA Networks, INC.
 * Written by: Jeffrey Magder (jmagder@somanetworks.com)
 *
 * This file is part of Kamailio, a free SIP server.
 *
 * Kamailio is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version
 *
 * Kamailio is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301
 * USA
 *
 *
 * Note: this file originally auto-generated by mib2c using
 *        : mib2c.notify.conf,v 5.3 2004/04/15 12:29:19 dts12 Exp $
 *
 * This file contains function prototypes for sending all traps supported by the
 * SNMPStats module.
 *
 */

#ifndef KAMAILIOMIBNOTIFICATIONS_H
#define KAMAILIOMIBNOTIFICATIONS_H


/*
 * Sends off a kamailioMsgQueueDepthMinorEvent trap to the master agent,
 * assigning the following variable bindings:
 *
 *  - kamailioMsgQueueDepth          = msgQueueDepth
 *  - kamailioMsgQueueMinorThreshold = minorThreshold
 *
 */
int send_kamailioMsgQueueDepthMinorEvent_trap(
		int msgQueueDepth, int minorThreshold);

/*
 * Sends off a kamailioMsgQueueDepthMajorEvent trap to the master agent,
 * assigning the following variable bindings:
 *
 *  - kamailioMsgQueueDepth          = msgQueueDepth
 *  - kamailioMsgQueueMajorThreshold = majorThreshold
 *
 */
int send_kamailioMsgQueueDepthMajorEvent_trap(
		int msgQueueDepth, int majorThreshold);

/*
 * Sends off a kamailioDialogLimitMinorEvent trap to the master agent,
 * assigning the following variable bindings:
 *
 *  - kamailioCurNumDialogs             = numDialogs
 *  - kamailioDialogLimitMinorThreshold = threshold
 *
 */
int send_kamailioDialogLimitMinorEvent_trap(int numDialogs, int threshold);

/*
 * Sends off a kamailioDialogLimitMinorEvent trap to the master agent,
 * assigning the following variable bindings:
 *
 *  - kamailioCurNumDialogs             = numDialogs
 *  - kamailioDialogLimitMinorThreshold = threshold
 *
 */
int send_kamailioDialogLimitMajorEvent_trap(int numDialogs, int threshold);

#endif /* KAMAILIOMIBNOTIFICATIONS_H */