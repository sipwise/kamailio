%define name    kamailio
%define ver 6.0.2
%define rel dev1.0%{dist}

%if 0%{?fedora}
%define dist_name fedora
%define dist_version %{?fedora}
%bcond_without cnxcc
%bcond_with dnssec
%bcond_without evapi
%bcond_without http_async_client
%bcond_without ims
%bcond_without jansson
%bcond_without json
%bcond_without lua
%bcond_without lwsc
%bcond_without kazoo
%bcond_without memcached
%bcond_without mongodb
%bcond_without nats
%bcond_without perl
%bcond_without phonenum
%bcond_with python2
%bcond_without python3
%bcond_without rabbitmq
%bcond_without redis
%bcond_without ruby
%bcond_without sctp
%bcond_without websocket
%bcond_without xmlrpc
%bcond_without wolfssl
%endif

%if 0%{?rhel} == 8
%if 0%{?centos_ver}
%define dist_name centos
%define dist_version %{?centos}
%define dist .el8.centos
%endif
%if 0%{?almalinux_ver}
%define dist_name centos
%define dist_version %{?almalinux}
%define dist .el8.almalinux
%endif
%if 0%{?rocky_ver}
%define dist_name centos
%define dist_version %{?rocky}
%define dist .el8.rocky
%endif
%if 0%{?centos_ver} == 0 && 0%{?almalinux_ver} == 0 && 0%{?rocky_ver} == 0
%define dist_name rhel
%define dist_version %{?rhel}
%endif
%bcond_without cnxcc
%bcond_with dnssec
%bcond_without evapi
%bcond_without http_async_client
%bcond_without ims
%bcond_without jansson
%bcond_without json
%bcond_without lua
%bcond_without lwsc
%bcond_without kazoo
%bcond_without memcached
%bcond_without mongodb
%bcond_without nats
%bcond_without perl
%bcond_without phonenum
%bcond_without python2
%bcond_without python3
%bcond_without rabbitmq
%bcond_without redis
%bcond_without ruby
%bcond_without sctp
%bcond_without websocket
%bcond_without xmlrpc
%bcond_without wolfssl
%endif

%if 0%{?rhel} == 9 || 0%{?rhel} == 10
%if 0%{?centos_ver}
%define dist_name centos
%define dist_version %{?centos}
%define dist .el%{?centos_ver}.centos
%endif
%if 0%{?almalinux_ver}
%define dist_name centos
%define dist_version %{?almalinux}
%define dist .el%{?almalinux_ver}.almalinux
%endif
%if 0%{?rocky_ver}
%define dist_name centos
%define dist_version %{?rocky}
%define dist .el%{?rocky_ver}.rocky
%endif
%if 0%{?centos_ver} == 0 && 0%{?almalinux_ver} == 0 && 0%{?rocky_ver} == 0
%define dist_name rhel
%define dist_version %{?rhel}
%endif
%bcond_without cnxcc
%bcond_with dnssec
%bcond_without evapi
%bcond_without http_async_client
%bcond_without ims
%bcond_without jansson
%bcond_without json
%bcond_without lua
%bcond_without lwsc
%bcond_without kazoo
%bcond_without memcached
%bcond_without mongodb
%bcond_without nats
%bcond_without perl
%bcond_without phonenum
%bcond_with python2
%bcond_without python3
%bcond_without rabbitmq
%bcond_without redis
%bcond_without ruby
%bcond_without sctp
%bcond_without websocket
%bcond_without xmlrpc
%bcond_without wolfssl
%endif

%if 0%{?suse_version}
%define dist_name opensuse
%define dist_version %{?suse_version}
%bcond_without cnxcc
%bcond_with dnssec
%bcond_with evapi
%bcond_without http_async_client
%bcond_without ims
%bcond_without jansson
%bcond_without json
%bcond_without lua
%bcond_without lwsc
%bcond_with kazoo
%bcond_without memcached
%bcond_with mongodb
%bcond_with nats
%bcond_without perl
%bcond_with phonenum
%bcond_without python2
%bcond_without python3
%bcond_with rabbitmq
%bcond_without redis
%bcond_without ruby
%bcond_without sctp
%bcond_without websocket
%bcond_without xmlrpc
%bcond_without wolfssl
%endif

# redefine buggy openSUSE Leap _sharedstatedir macro. More info at https://bugzilla.redhat.com/show_bug.cgi?id=183370
%if 0%{?suse_version} == 1315
%define _sharedstatedir /var/lib
%endif

# Defining missing macros on OpenSUSE Leap
%if 0%{?suse_version} == 1315
%define _fillupdir /var/adm/fillup-templates
%endif
%if 0%{?suse_version} == 1330
%define _fillupdir /var/adm/fillup-templates
%endif

# Package groups for OpenSUSE is different than others
%if 0%{?suse_version}
%define PKGGROUP System/Daemons
%else
%define PKGGROUP System Environment/Daemons
%endif


Summary:    Kamailio - the Open Source SIP Server
Name:       %name
Version:    %ver
Release:    %rel
Packager:   Sergey Safarov <s.safarov@gmail.com>
License:    GPL-2.0
Group:      %{PKGGROUP}
Source:     https://kamailio.org/pub/kamailio/%{ver}/src/%{name}-%{ver}_src.tar.gz
URL:        https://kamailio.org/
Vendor:     kamailio.org
BuildRoot:  %{_tmppath}/%{name}-%{ver}-buildroot
Conflicts:  kamailio-acc_json < %ver
Conflicts:  kamailio-auth-ephemeral < %ver, kamailio-bdb < %ver
Conflicts:  kamailio-carrierroute < %ver, kamailio-cpl < %ver
Conflicts:  kamailio-dialplan < %ver, kamailio-dnssec < %ver
Conflicts:  kamailio-geoip < %ver, kamailio-gzcompress < %ver
Conflicts:  kamailio-http_client < %ver
Conflicts:  kamailio-ims < %ver, kamailio-java < %ver, kamailio-json < %ver
Conflicts:  kamailio-jwt < %ver
Conflicts:  kamailio-kazoo < %ver
Conflicts:  kamailio-lcr < %ver, kamailio-ldap < %ver, kamailio-lost < %ver, kamailio-lua < %ver
Conflicts:  kamailio-nats < %ver
Conflicts:  kamailio-rabbitmq < %ver
Conflicts:  kamailio-memcached < %ver, kamailio-mongodb < %ver, kamailio-mysql < %ver
Conflicts:  kamailio-outbound < %ver, kamailio-perl < %ver
Conflicts:  kamailio-postgresql < %ver, kamailio-presence < %ver
Conflicts:  kamailio-python < %ver
Conflicts:  kamailio-radius < %ver, kamailio-redis < %ver
Conflicts:  kamailio-regex < %ver, kamailio-ruby < %ver
Conflicts:  kamailio-sctp < %ver, kamailio-secfilter < %ver, kamailio-sipdump < %ver
Conflicts:  kamailio-slack < %ver
Conflicts:  kamailio-snmpstats < %ver, kamailio-sqlang < %ver, kamailio-sqlite < %ver
Conflicts:  kamailio-tls < %ver, kamailio-unixodbc < %ver
Conflicts:  kamailio-utils < %ver, kamailio-websocket < %ver
Conflicts:  kamailio-xhttp-pi < %ver, kamailio-xmlops < %ver
Conflicts:  kamailio-xmlrpc < %ver, kamailio-xmpp < %ver
Conflicts:  kamailio-uuid < %ver
BuildRequires:  bison, flex, which, make, gcc, gcc-c++, pkgconfig, readline-devel
Requires:  systemd
BuildRequires:  systemd-devel

%if 0%{?suse_version} == 1315 || 0%{?suse_version} == 1330
Requires:  filesystem
BuildRequires:  shadow
%endif


%description
Kamailio is an Open Source SIP Server released under GPL, able
to handle thousands of call setups per second. Among features: asynchronous TCP,
UDP and SCTP, secure communication via TLS for VoIP (voice, video); IPv4 and
IPv6; SIMPLE instant messaging and presence with embedded XCAP server and MSRP
relay; ENUM; DID and least cost routing; load balancing; routing fail-over;
accounting, authentication and authorization; support for many backend systems
such as MySQL, Postgres, Oracle, Radius, LDAP, Redis, Cassandra; XMLRPC control
interface, SNMP monitoring. It can be used to build large VoIP servicing
platforms or to scale up SIP-to-PSTN gateways, PBX systems or media servers
like Asterisk™, FreeSWITCH™ or SEMS.


%if %{with jansson}
%package    acc_json
Summary:    Account transaction information in a JSON dictionary
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
Requires:   libevent
BuildRequires:  libevent-devel
%if 0%{?suse_version}
Requires:   libjansson
BuildRequires:  libjansson-devel
%else
Requires:   jansson
BuildRequires:  jansson-devel
%endif

%description    acc_json
Account transaction information in a JSON dictionary.
%endif


%package    auth-ephemeral
Summary:    Functions for authentication using ephemeral credentials
Requires:   openssl, kamailio = %ver
BuildRequires:  openssl-devel

%description    auth-ephemeral
Functions for authentication using ephemeral credentials.


%package    auth-xkeys
Summary:    Functions for authentication using shared keys
Group:      %{PKGGROUP}
Requires:   kamailio = %ver

%description    auth-xkeys
Functions for authentication using shared keys.


%package    bdb
Summary:    Berkeley database connectivity for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
%if 0%{?suse_version}
Requires:   libdb-4_8
BuildRequires:  libdb-4_8-devel
%else
Requires:   libdb
BuildRequires:  libdb-devel
%endif

%description    bdb
Berkeley database connectivity for Kamailio.


%package    carrierroute
Summary:    The carrierroute module for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver

%description    carrierroute
The carrierroute module for Kamailio.


%package    cfgt
Summary:    Unit test config file execution tracing module for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver

%description    cfgt
The unit test config file execution tracing module for Kamailio.


%if %{with cnxcc}
%package    cnxcc
Summary:    Module provides a mechanism to limit call duration
Group:      %{PKGGROUP}
Requires:   libevent, hiredis, kamailio = %ver
BuildRequires:  libevent-devel, hiredis-devel

%description    cnxcc
Module which provides a mechanism to limit call duration based on credit information parameters for Kamailio.
%endif


%package    cpl
Summary:    CPL (Call Processing Language) interpreter for Kamailio
Group:      %{PKGGROUP}
Requires:   which, libxml2, kamailio = %ver
BuildRequires:  libxml2-devel

%description    cpl
CPL (Call Processing Language) interpreter for Kamailio.


%package    crypto
Summary:    Module to support cryptographic extensions
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
%if 0%{?rhel} || 0%{?fedora}
Requires:   openssl-libs
BuildRequires:  openssl-devel
%endif
%if 0%{?suse_version}
Requires:   libopenssl1_0_0
BuildRequires:  libopenssl-devel
%endif

%description    crypto
This module provides various cryptography tools for use in Kamailio configuration file.  It relies on OpenSSL libraries for cryptographic operations (libssl, libcrypto).


%package    dialplan
Summary:    String translations based on rules for Kamailio
Group:      %{PKGGROUP}
Requires:   pcre2, kamailio = %ver
BuildRequires:  pcre2-devel

%description    dialplan
String translations based on rules for Kamailio.


%package    dmq_userloc
Summary:    User location records replication between multiple servers
Group:      %{PKGGROUP}
Requires:   kamailio = %ver

%description    dmq_userloc
User location (usrloc) records replication between multiple servers via DMQ module for Kamailio.


%if %{with dnssec}
%package    dnssec
Summary:    DNSSEC support for Kamailio
Group:      %{PKGGROUP}
Requires:   dnssec-tools-libs, kamailio = %ver
BuildRequires:  dnssec-tools-libs-devel

%description    dnssec
DNSSEC support for Kamailio.
%endif


%if %{with evapi}
%package    evapi
Summary:    Module can be used to create an event message flow from Kamailio to any application that can connect to a TCP socket
Group:      %{PKGGROUP}
Requires:   libev, kamailio = %ver
BuildRequires:  libev-devel

%description    evapi
The remote application can also issue messages received by Kamailio.
There is no protocol definition, it is all up to the author of the routing script.
Events can be generated for any event in Kamailio. For 3rd party transaction control, a transaction can be automatically
suspended when sending the event, to be resumed at a later point, maybe triggered by an incoming message on the event socket.
%endif


%package    geoip
Summary:    MaxMind GeoIP support for Kamailio
Group:      %{PKGGROUP}
Requires:   libmaxminddb, kamailio = %ver
BuildRequires:  libmaxminddb-devel

%description    geoip
MaxMind GeoIP support for Kamailio.


%package    gzcompress
Summary:    Compressed body (SIP and HTTP) handling for kamailio
Group:      %{PKGGROUP}
Requires:   zlib, kamailio = %ver
BuildRequires:  zlib-devel

%description    gzcompress
Compressed body (SIP and HTTP) handling for kamailio.


%if %{with http_async_client}
%package    http_async_client
Summary:    Async HTTP client module for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
Requires:   libevent
BuildRequires:  libevent-devel
%if 0%{?suse_version}
Requires:   libcurl4
BuildRequires:  libcurl-devel
%else
Requires:   libcurl
BuildRequires:  libcurl-devel
%endif

%description   http_async_client
This module implements protocol functions that use the libcurl to communicate with HTTP servers in asynchronous way.
%endif

%package    http_client
Summary:    HTTP client module for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
%if 0%{?suse_version}
Requires:   libcurl4, libxml2-tools
BuildRequires:  libcurl-devel, libxml2-devel
%else
Requires:   libxml2, libcurl, zlib
BuildRequires:  libxml2-devel, libcurl-devel, zlib-devel
%endif

%description    http_client
This module implements protocol functions that use the libcurl to communicate with HTTP servers.


%if %{with ims}
%package    ims
Summary:    IMS modules and extensions module for Kamailio
Group:      %{PKGGROUP}
Requires:   libxml2, kamailio = %ver
BuildRequires:  libxml2-devel libmnl-devel

%description    ims
IMS modules and extensions module for Kamailio.
%endif


%if %{with jansson}
%package    jansson
Summary:    JSON string handling and RPC modules for Kamailio using JANSSON library
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
Requires:   libevent
BuildRequires:  libevent-devel
%if 0%{?suse_version}
Requires:   libjson-c2
BuildRequires:  libjansson-devel
%else
Requires:   json-c
BuildRequires:  jansson-devel
%endif

%description    jansson
JSON string handling and RPC modules for Kamailio using JANSSON library.
%endif


%if %{with json}
%package    json
Summary:    JSON string handling and RPC modules for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
Requires:   libevent
BuildRequires:  libevent-devel
%if 0%{?suse_version}
Requires:   libjson-c2
BuildRequires:  libjson-c-devel
%else
Requires:   json-c
BuildRequires:  json-c-devel
%endif

%description    json
JSON string handling and RPC modules for Kamailio.
%endif


%package    jwt
Summary:    JWT (JSON Web Token) functions module for Kamailio
Group:      %{PKGGROUP}
Requires:   libjwt, kamailio = %ver
BuildRequires:  libjwt-devel

%description    jwt
This module provides JWT (JSON Web Token) functions to be used in Kamailio configuration file.
It relies on libjwt (at least v1.12.0) library (https://github.com/benmcollins/libjwt).


%if %{with kazoo}
%package    kazoo
Summary:    Kazoo middle layer connector support for Kamailio
Group:      %{PKGGROUP}
Requires:   libuuid, librabbitmq, json-c, kamailio = %ver
BuildRequires:  libuuid-devel, librabbitmq-devel, json-c-devel
Requires:   libevent
BuildRequires:  libevent-devel

%description    kazoo
Kazoo module for Kamailio.
%endif


%package    lcr
Summary:    Least cost routing for Kamailio
Group:      %{PKGGROUP}
Requires:   pcre2, kamailio = %ver
BuildRequires:  pcre2-devel

%description    lcr
Least cost routing for Kamailio.


%package    ldap
Summary:    LDAP search interface for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
%if 0%{?suse_version}
Requires:   openldap2 libsasl2-3
BuildRequires:  openldap2-devel cyrus-sasl-devel
%else
Requires:   openldap
BuildRequires:  openldap-devel
%endif

%description    ldap
LDAP search interface for Kamailio.

%package    lost
Summary:    HELD (RFC6155) and LOST (RFC5222) location-based routing
Group:      %{PKGGROUP}
Requires:   libxml2, kamailio = %ver
BuildRequires:  libxml2-devel

%description    lost
HELD (RFC6155) and LOST (RFC5222) location-based routing support for Kamailio.

%if %{with lua}
%package    lua
Summary:    Lua extensions for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
BuildRequires:  lua-devel

%description    lua
Lua extensions for Kamailio.
%endif


%if %{with lwsc}
%package    lwsc
Summary:    Websocket client implementation to interact with external systems, similar to http client
Group:      %{PKGGROUP}
Requires:   libwebsockets, kamailio = %ver
BuildRequires:  libwebsockets-devel

%description    lwsc
Websocket client implementation to interact with external systems, similar to http client.
%endif


%if %{with memcached}
%package    memcached
Summary:    Memcached configuration file support for Kamailio
Group:      %{PKGGROUP}
Requires:   libmemcached, kamailio = %ver
BuildRequires:  libmemcached-devel

%description    memcached
Memcached configuration file support for Kamailio.
%endif


%if %{with mongodb}
%package    mongodb
Summary:    MongoDB database connectivity for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
Requires:   mongo-c-driver
BuildRequires:  mongo-c-driver-devel

%description    mongodb
MongoDB database connectivity for Kamailio.
%endif


%package    mysql
Summary:    MySQL database connectivity for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
BuildRequires:  zlib-devel
%if 0%{?suse_version}
Requires:   libmysqlclient18
BuildRequires:  libmysqlclient-devel
%else
BuildRequires:  mariadb-devel
%endif

%description    mysql
MySQL database connectivity for Kamailio.


%if %{with nats}
%package    nats
Summary:    NATS consumer for Kamailio
Group:      %{PKGGROUP}
Requires:   libnats, kamailio = %ver
BuildRequires:    libnats-devel

%description    nats
The module provides an NATS consumer for Kamailio. NATS is a real time distributed messaging platform, more details about it can be found at nats.io.
%endif


%package    outbound
Summary:    Outbound (RFC 5626) support for Kamailio
Group:      %{PKGGROUP}
Requires:   openssl, kamailio = %ver
BuildRequires:  openssl-devel

%description    outbound
RFC 5626, "Managing Client-Initiated Connections in the Session Initiation
Protocol (SIP)" support for Kamailio.


%if %{with perl}
%package    perl
Summary:    Perl extensions and database driver for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
%if 0%{?suse_version}
Requires:   perl
BuildRequires:  perl
%else
Requires:   perl-libs
BuildRequires:  perl-ExtUtils-Embed
%endif

%description    perl
Perl extensions and database driver for Kamailio.
%endif


%if %{with phonenum}
%package    phonenum
Summary:    Phonenum module the Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
Requires:   libphonenumber
BuildRequires:  libphonenumber-devel libicu-devel protobuf-devel

%description    phonenum
Phonenum module the Kamailio.
%endif


%package    postgresql
Summary:    PostgreSQL database connectivity for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
%if 0%{?suse_version}
Requires:   libpq5
BuildRequires:  postgresql-devel
%else
Requires:   postgresql-libs
BuildRequires:  postgresql-devel
%endif

%description    postgresql
PostgreSQL database connectivity for Kamailio.


%package    presence
Summary:    SIP Presence (and RLS, XCAP, etc) support for Kamailio
Group:      %{PKGGROUP}
Requires:   libxml2, kamailio = %ver, kamailio-xmpp = %ver
BuildRequires:  libxml2-devel
%if 0%{?suse_version}
Requires:   libcurl4
BuildRequires:  libcurl-devel
%else
Requires:   libcurl
BuildRequires:  libcurl-devel
%endif

%description    presence
SIP Presence (and RLS, XCAP, etc) support for Kamailio.


%package    python
Summary:    Python extensions for Kamailio
Group:      %{PKGGROUP}
%if %{with python2}
Requires:   python2, kamailio = %ver
BuildRequires:  python2, python2-devel
%endif
%if %{with python3}
%if 0%{?rhel} == 8 || 0%{?rhel} == 9
Requires:   python3.12, kamailio = %ver
BuildRequires:  python3.12, python3.12-devel
%else
Requires:   python3, kamailio = %ver
BuildRequires:  python3, python3-devel
%endif
%endif

%description    python
Python extensions for Kamailio.


%if %{with rabbitmq}
%package    rabbitmq
Summary:    RabbitMQ related modules
Group:      %{PKGGROUP}
Requires:   libuuid, librabbitmq, kamailio = %ver
BuildRequires:    librabbitmq-devel, libuuid-devel

%description    rabbitmq
RabbitMQ module for Kamailio.
%endif


%package    radius
Summary:    RADIUS modules for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
%if 0%{?fedora} || 0%{?suse_version} || 0%{?rhel}
Requires:   radcli
BuildRequires:  radcli-devel
%else
Requires:   radiusclient-ng
BuildRequires:  radiusclient-ng-devel
%endif

%description    radius
RADIUS modules for Kamailio.


%if %{with redis}
%package    redis
Summary:    Redis configuration file support for Kamailio
Group:      %{PKGGROUP}
Requires:   hiredis, kamailio = %ver
BuildRequires:  hiredis-devel

%description    redis
Redis configuration file support for Kamailio.
%endif


%package    regex
Summary:    PCRE mtaching operations for Kamailio
Group:      %{PKGGROUP}
Requires:   pcre2, kamailio = %ver
BuildRequires:  pcre2-devel

%description    regex
PCRE mtaching operations for Kamailio.


%package    rtjson
Summary:    SIP routing based on JSON specifications
Group:      %{PKGGROUP}
Requires:   kamailio = %ver

%description    rtjson
SIP routing based on JSON specifications.


%if %{with ruby}
%package    ruby
Summary:    Ruby extensions for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
BuildRequires:  ruby-devel

%description    ruby
Ruby extensions for Kamailio.
%endif


%if %{with sctp}
%package    sctp
Summary:    SCTP transport for Kamailio
Group:      %{PKGGROUP}
Requires:   lksctp-tools, kamailio = %ver
BuildRequires:  lksctp-tools-devel

%description    sctp
SCTP transport for Kamailio.
%endif


%package    secfilter
Summary:    Additional layer of security over our communications
Group:      %{PKGGROUP}
Requires:   kamailio = %ver

%description    secfilter
Additional layer of security over our communications.


%package    sipdump
Summary:    This module writes SIP traffic and some associated details into local files
Group:      %{PKGGROUP}
Requires:   kamailio = %ver

%description    sipdump
This module writes SIP traffic and some associated details into local files


%package    sipjson
Summary:    This module serializes SIP message attributes into a JSON document
Group:      %{PKGGROUP}
Requires:   kamailio = %ver

%description    sipjson
This module serializes SIP message attributes into a JSON document


%package    slack
Summary:    Slack integration module for Kamailio
Group:      %{PKGGROUP}

Requires:   kamailio = %ver, kamailio-http_client = %ver
%if 0%{?suse_version}
Requires:   libcurl4
BuildRequires:  libcurl-devel
%else
Requires:   libcurl
BuildRequires:  libcurl-devel
%endif

%description    slack
This module provides integration with Slack over webhooks.


%package    smsops
Summary:    Tools for handling SMS packets in SIP messages
Group:      %{PKGGROUP}
Requires:   kamailio = %ver

%description    smsops
This module collects the Transformations for 3GPP-SMS.


%package    snmpstats
Summary:    SNMP management interface (scalar statistics) for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
%if 0%{?suse_version}
Requires:   libsnmp30
BuildRequires:  net-snmp-devel
%else
Requires:   net-snmp-libs
BuildRequires:  net-snmp-devel
%endif

%description    snmpstats
SNMP management interface (scalar statistics) for Kamailio.


%package    statsc
Summary:    Statistics collecting module providing reports for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver

%description    statsc
This module provides a statistics collector engine.


%package    statsd
Summary:    Send commands to statsd server
Group:      %{PKGGROUP}
Requires:   kamailio = %ver

%description    statsd
Send commands to statsd server.


%package        sqlang
Summary:        Squirrel Language (SQLang) for Kamailio
Group:          %{PKGGROUP}
Requires:       kamailio = %version
BuildRequires:  gcc-c++

%description    sqlang
Squirrel Language (SQLang) for Kamailio


%package    sqlite
Summary:    SQLite database connectivity for Kamailio
Group:      %{PKGGROUP}
Requires:   sqlite, kamailio = %ver
BuildRequires:  sqlite-devel

%description    sqlite
SQLite database connectivity for Kamailio.


%package    tls
Summary:    TLS transport for Kamailio
Group:      %{PKGGROUP}
Requires:   openssl, kamailio = %ver
BuildRequires:  openssl-devel

%description    tls
TLS transport for Kamailio.


%if %{with wolfssl}
%package    tls_wolfssl
Summary:    TLS transport for Kamailio based on wolfSSL
Group:      %{PKGGROUP}
BuildRequires: pkgconfig(wolfssl)

%description    tls_wolfssl
TLS transport for Kamailio based on wolfSSL
%endif


%package    tcpops
Summary:    On demand and per socket control to the TCP options
Group:      %{PKGGROUP}
Requires:   kamailio = %ver

%description    tcpops
On demand and per socket control to the TCP options.


%package    topos
Summary:    Topology stripping module for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver

%description    topos
This module offers topology hiding by stripping the routing headers that could show topology details.


%package    unixodbc
Summary:    UnixODBC database connectivity for Kamailio
Group:      %{PKGGROUP}
Requires:   unixODBC, kamailio = %ver
BuildRequires:  unixODBC-devel

%description    unixodbc
UnixODBC database connectivity for Kamailio.


%package    utils
Summary:    Non-SIP utitility functions for Kamailio
Group:      %{PKGGROUP}
Requires:   libxml2, kamailio = %ver
BuildRequires:  libxml2-devel
%if 0%{?suse_version}
Requires:   libcurl4
BuildRequires:  libcurl-devel
%else
Requires:   libcurl
BuildRequires:  libcurl-devel
%endif

%description    utils
Non-SIP utitility functions for Kamailio.


%if %{with websocket}
%package    websocket
Summary:    WebSocket transport for Kamailio
Group:      %{PKGGROUP}
Requires:   libunistring, openssl, kamailio = %ver
BuildRequires:  libunistring-devel, openssl-devel

%description    websocket
WebSocket transport for Kamailio.
%endif


%package    xhttp-pi
Summary:    Web-provisioning interface for Kamailio
Group:      %{PKGGROUP}
Requires:   libxml2, kamailio = %ver
BuildRequires:  libxml2-devel

%description    xhttp-pi
Web-provisioning interface for Kamailio.


%package    xmlops
Summary:    XML operation functions for Kamailio
Group:      %{PKGGROUP}
Requires:   libxml2, kamailio = %ver
BuildRequires:  libxml2-devel

%description    xmlops
XML operation functions for Kamailio.


%if %{with xmlrpc}
%package    xmlrpc
Summary:    XMLRPC transport and encoding for Kamailio RPCs and MI commands
Group:      %{PKGGROUP}
Requires:   libxml2, kamailio = %ver
BuildRequires:  libxml2-devel

%description    xmlrpc
XMLRPC transport and encoding for Kamailio RPCs and MI commands.
%endif

%package    xmpp
Summary:    SIP/XMPP IM gateway for Kamailio
Group:      %{PKGGROUP}
Requires:   kamailio = %ver
%if 0%{?suse_version}
Requires:   libexpat1
BuildRequires:  libexpat-devel
%else
Requires:   expat
BuildRequires:  expat-devel
%endif

%description    xmpp
SIP/XMPP IM gateway for Kamailio.


%package        uuid
Summary:        UUID generator for Kamailio
Group:          %{PKGGROUP}
Requires:   kamailio = %ver
%if 0%{?suse_version}
Requires:       libuuid1
BuildRequires:  libuuid-devel
%else
Requires:       libuuid
BuildRequires:  libuuid-devel
%endif

%description    uuid
UUID module for Kamailio.


%prep
%setup -n %{name}-%{ver}

# on latest dist need to add --atexit=no for Kamailio options. More details GH #2616
sed -i -e 's|/usr/sbin/kamailio|/usr/sbin/kamailio --atexit=no|' pkg/kamailio/obs/kamailio.service
sed -i -e 's|/usr/sbin/kamailio|/usr/sbin/kamailio --atexit=no|' pkg/kamailio/obs/kamailio@.service

rm -f misc/examples/pkg/sipcapture.cfg


%build
%if 0%{?fedora} || 0%{?suse_version} || 0%{?rhel} >= 8
export RADCLI=1
%endif
make cfg prefix=/usr \
    basedir=%{buildroot} \
    cfg_prefix=%{buildroot} \
    doc_prefix=%{buildroot} \
    doc_dir=%{_docdir}/kamailio/ \
    cfg_target=%{_sysconfdir}/kamailio/ modules_dirs="modules"
make
make every-module skip_modules="app_mono db_cassandra db_oracle iptrtpproxy \
    jabber ndb_cassandra osp" \
%if 0%{?fedora} || 0%{?suse_version} || 0%{?rhel} >= 8
    RADCLI=1 \
%endif
%if 0%{?rhel} >= 8
    PYTHON3=python3.12 \
%endif
    WOLFSSL_INTERNAL=no \
    group_include="kstandard kautheph kberkeley kcarrierroute \
%if %{with cnxcc}
    kcnxcc \
%endif
    kcpl \
%if %{with dnssec}
    kdnssec \
%endif
%if %{with evapi}
    kev \
%endif
    kgeoip2 \
    kgzcompress \
%if %{with http_async_client}
    khttp_async \
%endif
    kxhttp_prom \
%if %{with ims}
    kims \
%endif
%if %{with jansson}
    kjansson \
%endif
%if %{with json}
    kjson \
%endif
    kjsonrpcs \
    kjwt \
%if %{with kazoo}
    kkazoo \
%endif
    kldap \
%if %{with lua}
    klua \
%endif
%if %{with lwsc}
    klwsc \
%endif
%if %{with memcached}
    kmemcached \
%endif
%if %{with xmlrpc}
    kmi_xmlrpc \
%endif
%if %{with mongodb}
    kmongodb \
%endif
    kmysql koutbound \
%if %{with nats}
    knats \
%endif
%if %{with perl}
    kperl \
%endif
%if %{with phonenum}
    kphonenum \
%endif
    kpostgres kpresence \
%if %{with python2}
    kpython \
%endif
%if %{with python3}
    kpython3 \
%endif
%if %{with rabbitmq}
    krabbitmq \
%endif
    kradius \
%if %{with redis}
    kredis \
%endif
%if %{with ruby}
    kruby \
%endif
%if %{with sctp}
    ksctp \
%endif
    ksnmpstats ksqlite \
%if "%{?_unitdir}" != ""
    ksystemd \
%endif
    ktls \
%if %{with wolfssl}
    ktls_wolfssl \
%endif
    kunixodbc kutils \
%if %{with websocket}
    kwebsocket \
%endif
    kxml kxmpp kuuid"

make utils



%install
rm -rf %{buildroot}

make install
make install-modules-all skip_modules="app_mono db_cassandra db_oracle \
    iptrtpproxy jabber osp" \
%if 0%{?fedora} || 0%{?suse_version} || 0%{?rhel} >= 8
    RADCLI=1 \
%endif
%if 0%{?rhel} >= 8
    PYTHON3=python3.12 \
%endif
    WOLFSSL_INTERNAL=no \
    group_include="kstandard kautheph kberkeley kcarrierroute \
%if %{with cnxcc}
    kcnxcc \
%endif
    kcpl \
%if %{with dnssec}
    kdnssec \
%endif
%if %{with evapi}
    kev \
%endif
    kgeoip2 \
    kgzcompress \
%if %{with http_async_client}
    khttp_async \
%endif
    kxhttp_prom \
%if %{with ims}
    kims \
%endif
%if %{with jansson}
    kjansson \
%endif
%if %{with json}
    kjson \
%endif
    kjsonrpcs \
    kjwt \
%if %{with kazoo}
    kkazoo \
%endif
    kldap \
%if %{with lua}
    klua \
%endif
%if %{with lwsc}
    klwsc \
%endif
%if %{with memcached}
    kmemcached \
%endif
%if %{with xmlrpc}
    kmi_xmlrpc \
%endif
%if %{with mongodb}
    kmongodb \
%endif
    kmysql koutbound \
%if %{with nats}
    knats \
%endif
%if %{with perl}
    kperl \
%endif
%if %{with phonenum}
    kphonenum \
%endif
    kpostgres kpresence \
%if %{with python2}
    kpython \
%endif
%if %{with python3}
    kpython3 \
%endif
%if %{with rabbitmq}
    krabbitmq \
%endif
    kradius \
%if %{with redis}
    kredis \
%endif
%if %{with ruby}
    kruby \
%endif
%if %{with sctp}
    ksctp \
%endif
    ksnmpstats ksqlite \
%if "%{?_unitdir}" != ""
    ksystemd \
%endif
    ktls \
%if %{with wolfssl}
    ktls_wolfssl \
%endif
    kunixodbc kutils \
%if %{with websocket}
    kwebsocket \
%endif
    kxml kxmpp kuuid"

make install-cfg-pkg

install -d %{buildroot}%{_sharedstatedir}/kamailio

install -d %{buildroot}%{_unitdir}
install -Dpm 0644 pkg/kamailio/obs/kamailio.service %{buildroot}%{_unitdir}/kamailio.service
install -Dpm 0644 pkg/kamailio/obs/kamailio@.service %{buildroot}%{_unitdir}/kamailio@.service
install -Dpm 0644 pkg/kamailio/obs/kamailio.tmpfiles %{buildroot}%{_tmpfilesdir}/kamailio.conf

%if 0%{?suse_version}
install -d %{buildroot}%{_fillupdir}
install -m644 pkg/kamailio/obs/kamailio.sysconfig \
        %{buildroot}%{_fillupdir}/sysconfig.kamailio
%else
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m644 pkg/kamailio/obs/kamailio.sysconfig \
        %{buildroot}%{_sysconfdir}/sysconfig/kamailio
%endif

%if 0%{?suse_version}
%py_compile -O %{buildroot}%{_libdir}/kamailio/kamctl/dbtextdb
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
%py_byte_compile %{__python3} %{buildroot}%{_libdir}/kamailio/kamctl/dbtextdb
%endif

# Removing devel files
rm -f %{buildroot}%{_libdir}/kamailio/lib*.so

%pre
if ! /usr/bin/id kamailio &>/dev/null; then
       /usr/sbin/useradd --system \
                         --user-group \
                         --shell /bin/false \
                         --comment "Kamailio SIP Server" \
                         --home-dir %{_rundir}/kamailio kamailio || \
                %logmsg "Unexpected error adding user \"kamailio\". Aborting installation."
fi

%clean
rm -rf %{buildroot}


%post
%if "%{?_unitdir}" == ""
/sbin/chkconfig --add kamailio
%else
%tmpfiles_create kamailio.conf
/usr/bin/systemctl -q enable kamailio.service
%endif


%preun
if [ $1 = 0 ]; then
%if "%{?_unitdir}" == ""
    /sbin/service kamailio stop > /dev/null 2>&1
    /sbin/chkconfig --del kamailio
%else
    %{?systemd_preun kamailio.service}
%endif
fi

%if "%{?_unitdir}" == ""
%postun
%{?systemd_postun kamailio.service}
%endif

%files
%defattr(-,root,root)
%dir %{_docdir}/kamailio
%doc %{_docdir}/kamailio/INSTALL
%doc %{_docdir}/kamailio/README

%dir %{_docdir}/kamailio/modules
%doc %{_docdir}/kamailio/modules/README.acc
%doc %{_docdir}/kamailio/modules/README.acc_diameter
%doc %{_docdir}/kamailio/modules/README.alias_db
%doc %{_docdir}/kamailio/modules/README.app_jsdt
%doc %{_docdir}/kamailio/modules/README.async
%doc %{_docdir}/kamailio/modules/README.auth
%doc %{_docdir}/kamailio/modules/README.auth_db
%doc %{_docdir}/kamailio/modules/README.auth_diameter
%doc %{_docdir}/kamailio/modules/README.avp
%doc %{_docdir}/kamailio/modules/README.avpops
%doc %{_docdir}/kamailio/modules/README.benchmark
%doc %{_docdir}/kamailio/modules/README.blst
%doc %{_docdir}/kamailio/modules/README.call_control
%doc %{_docdir}/kamailio/modules/README.cfg_db
%doc %{_docdir}/kamailio/modules/README.cfg_rpc
%doc %{_docdir}/kamailio/modules/README.cfgutils
%doc %{_docdir}/kamailio/modules/README.corex
%doc %{_docdir}/kamailio/modules/README.counters
%doc %{_docdir}/kamailio/modules/README.ctl
%doc %{_docdir}/kamailio/modules/README.db_cluster
%doc %{_docdir}/kamailio/modules/README.db_flatstore
%doc %{_docdir}/kamailio/modules/README.db_text
%doc %{_docdir}/kamailio/modules/README.db2_ops
%doc %{_docdir}/kamailio/modules/README.debugger
%doc %{_docdir}/kamailio/modules/README.dialog
%doc %{_docdir}/kamailio/modules/README.dispatcher
%doc %{_docdir}/kamailio/modules/README.diversion
%doc %{_docdir}/kamailio/modules/README.dlgs
%doc %{_docdir}/kamailio/modules/README.dmq
%doc %{_docdir}/kamailio/modules/README.domain
%doc %{_docdir}/kamailio/modules/README.domainpolicy
%doc %{_docdir}/kamailio/modules/README.drouting
%doc %{_docdir}/kamailio/modules/README.enum
%doc %{_docdir}/kamailio/modules/README.exec
%doc %{_docdir}/kamailio/modules/README.file_out
%doc %{_docdir}/kamailio/modules/README.group
%doc %{_docdir}/kamailio/modules/README.htable
%doc %{_docdir}/kamailio/modules/README.imc
%doc %{_docdir}/kamailio/modules/README.influxdbc
%doc %{_docdir}/kamailio/modules/README.ipops
%doc %{_docdir}/kamailio/modules/README.kemix
%doc %{_docdir}/kamailio/modules/README.kex
%doc %{_docdir}/kamailio/modules/README.lrkproxy
%doc %{_docdir}/kamailio/modules/README.mangler
%doc %{_docdir}/kamailio/modules/README.math
%doc %{_docdir}/kamailio/modules/README.matrix
%doc %{_docdir}/kamailio/modules/README.maxfwd
%doc %{_docdir}/kamailio/modules/README.mediaproxy
%doc %{_docdir}/kamailio/modules/README.misctest
%doc %{_docdir}/kamailio/modules/README.mohqueue
%doc %{_docdir}/kamailio/modules/README.mqueue
%doc %{_docdir}/kamailio/modules/README.msilo
%doc %{_docdir}/kamailio/modules/README.msrp
%doc %{_docdir}/kamailio/modules/README.mtree
%doc %{_docdir}/kamailio/modules/README.nat_traversal
%doc %{_docdir}/kamailio/modules/README.nathelper
%doc %{_docdir}/kamailio/modules/README.p_usrloc
%doc %{_docdir}/kamailio/modules/README.path
%doc %{_docdir}/kamailio/modules/README.pdb
%doc %{_docdir}/kamailio/modules/README.pdt
%doc %{_docdir}/kamailio/modules/README.permissions
%doc %{_docdir}/kamailio/modules/README.pike
%doc %{_docdir}/kamailio/modules/README.pipelimit
%doc %{_docdir}/kamailio/modules/README.posops
%doc %{_docdir}/kamailio/modules/README.prefix_route
%doc %{_docdir}/kamailio/modules/README.pv
%doc %{_docdir}/kamailio/modules/README.pv_headers
%doc %{_docdir}/kamailio/modules/README.pvtpl
%doc %{_docdir}/kamailio/modules/README.pua_rpc
%doc %{_docdir}/kamailio/modules/README.qos
%doc %{_docdir}/kamailio/modules/README.ratelimit
%doc %{_docdir}/kamailio/modules/README.registrar
%doc %{_docdir}/kamailio/modules/README.rr
%doc %{_docdir}/kamailio/modules/README.rtimer
%doc %{_docdir}/kamailio/modules/README.rtpproxy
%doc %{_docdir}/kamailio/modules/README.rtpengine
%doc %{_docdir}/kamailio/modules/README.sanity
%doc %{_docdir}/kamailio/modules/README.sca
%doc %{_docdir}/kamailio/modules/README.sdpops
%doc %{_docdir}/kamailio/modules/README.seas
%doc %{_docdir}/kamailio/modules/README.sipcapture
%doc %{_docdir}/kamailio/modules/README.siprepo
%doc %{_docdir}/kamailio/modules/README.sipt
%doc %{_docdir}/kamailio/modules/README.siptrace
%doc %{_docdir}/kamailio/modules/README.siputils
%doc %{_docdir}/kamailio/modules/README.sl
%doc %{_docdir}/kamailio/modules/README.sms
%doc %{_docdir}/kamailio/modules/README.smsops
%doc %{_docdir}/kamailio/modules/README.speeddial
%doc %{_docdir}/kamailio/modules/README.sqlops
%doc %{_docdir}/kamailio/modules/README.ss7ops
%doc %{_docdir}/kamailio/modules/README.sst
%doc %{_docdir}/kamailio/modules/README.statistics
%doc %{_docdir}/kamailio/modules/README.stun
%doc %{_docdir}/kamailio/modules/README.sworker
%doc %{_docdir}/kamailio/modules/README.textops
%doc %{_docdir}/kamailio/modules/README.textopsx
%doc %{_docdir}/kamailio/modules/README.timer
%doc %{_docdir}/kamailio/modules/README.tm
%doc %{_docdir}/kamailio/modules/README.tmrec
%doc %{_docdir}/kamailio/modules/README.tmx
%doc %{_docdir}/kamailio/modules/README.topoh
%doc %{_docdir}/kamailio/modules/README.topos_htable
%doc %{_docdir}/kamailio/modules/README.uac
%doc %{_docdir}/kamailio/modules/README.uac_redirect
%doc %{_docdir}/kamailio/modules/README.uid_auth_db
%doc %{_docdir}/kamailio/modules/README.uid_avp_db
%doc %{_docdir}/kamailio/modules/README.uid_domain
%doc %{_docdir}/kamailio/modules/README.uid_gflags
%doc %{_docdir}/kamailio/modules/README.uid_uri_db
%doc %{_docdir}/kamailio/modules/README.uri_db
%doc %{_docdir}/kamailio/modules/README.userblocklist
%doc %{_docdir}/kamailio/modules/README.usrloc
%doc %{_docdir}/kamailio/modules/README.xhttp
%doc %{_docdir}/kamailio/modules/README.xhttp_prom
%doc %{_docdir}/kamailio/modules/README.xhttp_rpc
%doc %{_docdir}/kamailio/modules/README.xlog
%doc %{_docdir}/kamailio/modules/README.xprint
%doc %{_docdir}/kamailio/modules/README.jsonrpcs
%doc %{_docdir}/kamailio/modules/README.nosip
%doc %{_docdir}/kamailio/modules/README.tsilo
%doc %{_docdir}/kamailio/modules/README.call_obj
%doc %{_docdir}/kamailio/modules/README.evrexec
%doc %{_docdir}/kamailio/modules/README.keepalive
%doc %{_docdir}/kamailio/modules/README.log_custom
%doc %{_docdir}/kamailio/modules/README.statsc
%doc %{_docdir}/kamailio/modules/README.topos
%doc %{_docdir}/kamailio/modules/README.cfgt
%if "%{?_unitdir}" != ""
%doc %{_docdir}/kamailio/modules/README.log_systemd
%doc %{_docdir}/kamailio/modules/README.systemdops
%endif

%dir %attr(-,kamailio,kamailio) %{_sysconfdir}/kamailio
%config(noreplace) %{_sysconfdir}/kamailio/dictionary.kamailio
%config(noreplace) %{_sysconfdir}/kamailio/kamailio.cfg
%config(noreplace) %{_sysconfdir}/kamailio/kamctlrc
%config(noreplace) %{_sysconfdir}/kamailio/pi_framework.xml
%config(noreplace) %{_sysconfdir}/kamailio/tls.cfg
%dir %attr(-,kamailio,kamailio) %{_sharedstatedir}/kamailio
%if 0%{?suse_version}
%{_fillupdir}/sysconfig.kamailio
%else
%config %{_sysconfdir}/sysconfig/kamailio
%endif
%if "%{?_unitdir}" == ""
%config %{_sysconfdir}/rc.d/init.d/*
%dir %attr(-,kamailio,kamailio) %{_var}/run/kamailio
%else
%{_unitdir}/kamailio.service
%{_unitdir}/kamailio@.service
%{_tmpfilesdir}/kamailio.conf
%endif

%dir %{_libdir}/kamailio

%dir %{_libdir}/kamailio/modules
%{_libdir}/kamailio/modules/acc.so
%{_libdir}/kamailio/modules/acc_diameter.so
%{_libdir}/kamailio/modules/alias_db.so
%{_libdir}/kamailio/modules/app_jsdt.so
%{_libdir}/kamailio/modules/async.so
%{_libdir}/kamailio/modules/auth.so
%{_libdir}/kamailio/modules/auth_db.so
%{_libdir}/kamailio/modules/auth_diameter.so
%{_libdir}/kamailio/modules/avp.so
%{_libdir}/kamailio/modules/avpops.so
%{_libdir}/kamailio/modules/benchmark.so
%{_libdir}/kamailio/modules/blst.so
%{_libdir}/kamailio/modules/call_control.so
%{_libdir}/kamailio/modules/cfg_db.so
%{_libdir}/kamailio/modules/cfg_rpc.so
%{_libdir}/kamailio/modules/cfgutils.so
%{_libdir}/kamailio/modules/corex.so
%{_libdir}/kamailio/modules/counters.so
%{_libdir}/kamailio/modules/ctl.so
%{_libdir}/kamailio/modules/db_cluster.so
%{_libdir}/kamailio/modules/db_flatstore.so
%{_libdir}/kamailio/modules/db_text.so
%{_libdir}/kamailio/modules/db2_ops.so
%{_libdir}/kamailio/modules/debugger.so
%{_libdir}/kamailio/modules/dialog.so
%{_libdir}/kamailio/modules/dispatcher.so
%{_libdir}/kamailio/modules/diversion.so
%{_libdir}/kamailio/modules/dlgs.so
%{_libdir}/kamailio/modules/dmq.so
%{_libdir}/kamailio/modules/domain.so
%{_libdir}/kamailio/modules/domainpolicy.so
%{_libdir}/kamailio/modules/drouting.so
%{_libdir}/kamailio/modules/enum.so
%{_libdir}/kamailio/modules/exec.so
%{_libdir}/kamailio/modules/file_out.so
%{_libdir}/kamailio/modules/group.so
%{_libdir}/kamailio/modules/htable.so
%{_libdir}/kamailio/modules/imc.so
%{_libdir}/kamailio/modules/influxdbc.so
%{_libdir}/kamailio/modules/ipops.so
%{_libdir}/kamailio/modules/kemix.so
%{_libdir}/kamailio/modules/kex.so
%{_libdir}/kamailio/modules/lrkproxy.so
%{_libdir}/kamailio/modules/mangler.so
%{_libdir}/kamailio/modules/math.so
%{_libdir}/kamailio/modules/matrix.so
%{_libdir}/kamailio/modules/maxfwd.so
%{_libdir}/kamailio/modules/mediaproxy.so
%{_libdir}/kamailio/modules/misctest.so
%{_libdir}/kamailio/modules/mohqueue.so
%{_libdir}/kamailio/modules/mqueue.so
%{_libdir}/kamailio/modules/msilo.so
%{_libdir}/kamailio/modules/msrp.so
%{_libdir}/kamailio/modules/mtree.so
%{_libdir}/kamailio/modules/nat_traversal.so
%{_libdir}/kamailio/modules/nathelper.so
%{_libdir}/kamailio/modules/p_usrloc.so
%{_libdir}/kamailio/modules/path.so
%{_libdir}/kamailio/modules/pdb.so
%{_libdir}/kamailio/modules/pdt.so
%{_libdir}/kamailio/modules/permissions.so
%{_libdir}/kamailio/modules/pike.so
%{_libdir}/kamailio/modules/pipelimit.so
%{_libdir}/kamailio/modules/posops.so
%{_libdir}/kamailio/modules/prefix_route.so
%{_libdir}/kamailio/modules/pua_rpc.so
%{_libdir}/kamailio/modules/pv.so
%{_libdir}/kamailio/modules/pv_headers.so
%{_libdir}/kamailio/modules/pvtpl.so
%{_libdir}/kamailio/modules/qos.so
%{_libdir}/kamailio/modules/ratelimit.so
%{_libdir}/kamailio/modules/registrar.so
%{_libdir}/kamailio/modules/rr.so
%{_libdir}/kamailio/modules/rtimer.so
%{_libdir}/kamailio/modules/rtpproxy.so
%{_libdir}/kamailio/modules/rtpengine.so
%{_libdir}/kamailio/modules/sanity.so
%{_libdir}/kamailio/modules/sca.so
%{_libdir}/kamailio/modules/sdpops.so
%{_libdir}/kamailio/modules/seas.so
%{_libdir}/kamailio/modules/sipcapture.so
%{_libdir}/kamailio/modules/siprepo.so
%{_libdir}/kamailio/modules/sipt.so
%{_libdir}/kamailio/modules/siptrace.so
%{_libdir}/kamailio/modules/siputils.so
%{_libdir}/kamailio/modules/sl.so
%{_libdir}/kamailio/modules/sms.so
%{_libdir}/kamailio/modules/smsops.so
%{_libdir}/kamailio/modules/speeddial.so
%{_libdir}/kamailio/modules/sqlops.so
%{_libdir}/kamailio/modules/ss7ops.so
%{_libdir}/kamailio/modules/sst.so
%{_libdir}/kamailio/modules/statistics.so
%{_libdir}/kamailio/modules/stun.so
%{_libdir}/kamailio/modules/sworker.so
%{_libdir}/kamailio/modules/textops.so
%{_libdir}/kamailio/modules/textopsx.so
%{_libdir}/kamailio/modules/timer.so
%{_libdir}/kamailio/modules/tm.so
%{_libdir}/kamailio/modules/tmrec.so
%{_libdir}/kamailio/modules/tmx.so
%{_libdir}/kamailio/modules/topoh.so
%{_libdir}/kamailio/modules/uac.so
%{_libdir}/kamailio/modules/uac_redirect.so
%{_libdir}/kamailio/modules/uid_auth_db.so
%{_libdir}/kamailio/modules/uid_avp_db.so
%{_libdir}/kamailio/modules/uid_domain.so
%{_libdir}/kamailio/modules/uid_gflags.so
%{_libdir}/kamailio/modules/uid_uri_db.so
%{_libdir}/kamailio/modules/uri_db.so
%{_libdir}/kamailio/modules/userblocklist.so
%{_libdir}/kamailio/modules/usrloc.so
%{_libdir}/kamailio/modules/xhttp.so
%{_libdir}/kamailio/modules/xhttp_prom.so
%{_libdir}/kamailio/modules/xhttp_rpc.so
%{_libdir}/kamailio/modules/xlog.so
%{_libdir}/kamailio/modules/xprint.so
%{_libdir}/kamailio/modules/jsonrpcs.so
%{_libdir}/kamailio/modules/nosip.so
%{_libdir}/kamailio/modules/tsilo.so
%{_libdir}/kamailio/modules/call_obj.so
%{_libdir}/kamailio/modules/evrexec.so
%{_libdir}/kamailio/modules/keepalive.so
%{_libdir}/kamailio/modules/log_custom.so
%{_libdir}/kamailio/modules/statsc.so
%{_libdir}/kamailio/modules/topos.so
%{_libdir}/kamailio/modules/topos_htable.so
%{_libdir}/kamailio/modules/cfgt.so
%if "%{?_unitdir}" != ""
%{_libdir}/kamailio/modules/log_systemd.so
%{_libdir}/kamailio/modules/systemdops.so
%endif

%{_sbindir}/kamailio
%{_sbindir}/kamctl
%{_sbindir}/kamdbctl
%{_sbindir}/kamcmd

%dir %{_libdir}/kamailio/kamctl
%{_libdir}/kamailio/kamctl/kamctl.base
%{_libdir}/kamailio/kamctl/kamctl.ctlbase
%{_libdir}/kamailio/kamctl/kamctl.dbtext
%{_libdir}/kamailio/kamctl/kamctl.rpcfifo
%{_libdir}/kamailio/kamctl/kamctl.ser
%{_libdir}/kamailio/kamctl/kamctl.sqlbase
%{_libdir}/kamailio/kamctl/kamdbctl.base
%{_libdir}/kamailio/kamctl/kamdbctl.dbtext

%dir %{_libdir}/kamailio/kamctl/dbtextdb
%{_libdir}/kamailio/kamctl/dbtextdb/dbtextdb.py
%if 0%{?rhel} >= 8 || 0%{?fedora}
%dir %{_libdir}/kamailio/kamctl/dbtextdb/__pycache__
%{_libdir}/kamailio/kamctl/dbtextdb/__pycache__/*.pyc
%endif

%{_mandir}/man5/*
%{_mandir}/man8/*

%dir %{_datadir}/kamailio
%dir %{_datadir}/kamailio/dbtext
%dir %{_datadir}/kamailio/dbtext/kamailio
%{_datadir}/kamailio/dbtext/kamailio/*


%if %{with jansson}
%files      acc_json
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.acc_json
%{_libdir}/kamailio/modules/acc_json.so
%endif


%files      auth-ephemeral
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.auth_ephemeral
%{_libdir}/kamailio/modules/auth_ephemeral.so


%files      auth-xkeys
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.auth_xkeys
%{_libdir}/kamailio/modules/auth_xkeys.so


%files      bdb
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.db_berkeley
%{_sbindir}/kambdb_recover
%{_libdir}/kamailio/modules/db_berkeley.so
%{_libdir}/kamailio/kamctl/kamctl.db_berkeley
%{_libdir}/kamailio/kamctl/kamdbctl.db_berkeley
%dir %{_datadir}/kamailio/db_berkeley
%{_datadir}/kamailio/db_berkeley/*


%files      carrierroute
%defattr(-,root,root)
%{_docdir}/kamailio/modules/README.carrierroute
%{_libdir}/kamailio/modules/carrierroute.so


%if %{with cnxcc}
%files      cnxcc
%defattr(-,root,root)
%{_docdir}/kamailio/modules/README.cnxcc
%{_libdir}/kamailio/modules/cnxcc.so
%endif


%files      cpl
%defattr(-,root,root)
%{_docdir}/kamailio/modules/README.cplc
%{_libdir}/kamailio/modules/cplc.so


%files      crypto
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.crypto
%{_libdir}/kamailio/modules/crypto.so


%files      dialplan
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.dialplan
%{_libdir}/kamailio/modules/dialplan.so


%files      dmq_userloc
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.dmq_usrloc
%{_libdir}/kamailio/modules/dmq_usrloc.so


%if %{with dnssec}
%files      dnssec
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.dnssec
%{_libdir}/kamailio/modules/dnssec.so
%endif


%if %{with evapi}
%files      evapi
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.evapi
%{_libdir}/kamailio/modules/evapi.so
%endif


%files      geoip
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.geoip2
%{_libdir}/kamailio/modules/geoip2.so


%files      gzcompress
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.gzcompress
%{_libdir}/kamailio/modules/gzcompress.so


%if %{with http_async_client}
%files      http_async_client
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.http_async_client
%{_libdir}/kamailio/modules/http_async_client.so
%endif

%files      http_client
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.http_client
%{_libdir}/kamailio/modules/http_client.so

%if %{with ims}
%files      ims
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.cdp
%doc %{_docdir}/kamailio/modules/README.cdp_avp
%doc %{_docdir}/kamailio/modules/README.ims_auth
%doc %{_docdir}/kamailio/modules/README.ims_charging
%doc %{_docdir}/kamailio/modules/README.ims_dialog
%doc %{_docdir}/kamailio/modules/README.ims_diameter_server
%doc %{_docdir}/kamailio/modules/README.ims_icscf
%doc %{_docdir}/kamailio/modules/README.ims_ipsec_pcscf
%doc %{_docdir}/kamailio/modules/README.ims_isc
%doc %{_docdir}/kamailio/modules/README.ims_ocs
%doc %{_docdir}/kamailio/modules/README.ims_qos
%doc %{_docdir}/kamailio/modules/README.ims_qos_npn
%doc %{_docdir}/kamailio/modules/README.ims_registrar_pcscf
%doc %{_docdir}/kamailio/modules/README.ims_registrar_scscf
%doc %{_docdir}/kamailio/modules/README.ims_usrloc_pcscf
%doc %{_docdir}/kamailio/modules/README.ims_usrloc_scscf
%{_libdir}/kamailio/modules/cdp.so
%{_libdir}/kamailio/modules/cdp_avp.so
%{_libdir}/kamailio/modules/ims_auth.so
%{_libdir}/kamailio/modules/ims_charging.so
%{_libdir}/kamailio/modules/ims_dialog.so
%{_libdir}/kamailio/modules/ims_diameter_server.so
%{_libdir}/kamailio/modules/ims_icscf.so
%{_libdir}/kamailio/modules/ims_ipsec_pcscf.so
%{_libdir}/kamailio/modules/ims_isc.so
%{_libdir}/kamailio/modules/ims_ocs.so
%{_libdir}/kamailio/modules/ims_qos.so
%{_libdir}/kamailio/modules/ims_qos_npn.so
%{_libdir}/kamailio/modules/ims_registrar_pcscf.so
%{_libdir}/kamailio/modules/ims_registrar_scscf.so
%{_libdir}/kamailio/modules/ims_usrloc_pcscf.so
%{_libdir}/kamailio/modules/ims_usrloc_scscf.so
%endif


%if %{with jansson}
%files      jansson
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.jansson
%doc %{_docdir}/kamailio/modules/README.janssonrpcc
%{_libdir}/kamailio/modules/jansson.so
%{_libdir}/kamailio/modules/janssonrpcc.so
%endif


%if %{with json}
%files      json
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.json
%doc %{_docdir}/kamailio/modules/README.jsonrpcc
%{_libdir}/kamailio/modules/json.so
%{_libdir}/kamailio/modules/jsonrpcc.so
%endif


%files      jwt
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.jwt
%{_libdir}/kamailio/modules/jwt.so


%if %{with kazoo}
%files      kazoo
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.kazoo
%{_libdir}/kamailio/modules/kazoo.so
%endif

%files      lcr
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.lcr
%{_libdir}/kamailio/modules/lcr.so


%files      ldap
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.db2_ldap
%doc %{_docdir}/kamailio/modules/README.h350
%doc %{_docdir}/kamailio/modules/README.ldap
%{_libdir}/kamailio/modules/db2_ldap.so
%{_libdir}/kamailio/modules/h350.so
%{_libdir}/kamailio/modules/ldap.so

%files      lost
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.lost
%{_libdir}/kamailio/modules/lost.so


%if %{with lua}
%files      lua
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.app_lua
%{_libdir}/kamailio/modules/app_lua.so
%endif


%if %{with lwsc}
%files      lwsc
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.lwsc
%{_libdir}/kamailio/modules/lwsc.so
%endif

%if %{with memcached}
%files      memcached
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.memcached
%{_libdir}/kamailio/modules/memcached.so
%endif


%if %{with mongodb}
%files      mongodb
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.db_mongodb
%doc %{_docdir}/kamailio/modules/README.ndb_mongodb
%{_libdir}/kamailio/modules/db_mongodb.so
%{_libdir}/kamailio/modules/ndb_mongodb.so
%endif


%files      mysql
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.db_mysql
%{_libdir}/kamailio/modules/db_mysql.so
%{_libdir}/kamailio/kamctl/kamctl.mysql
%{_libdir}/kamailio/kamctl/kamdbctl.mysql
%dir %{_datadir}/kamailio/mysql
%{_datadir}/kamailio/mysql/*


%if %{with nats}
%files      nats
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.nats
%{_libdir}/kamailio/modules/nats.so
%endif


%files      outbound
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.outbound
%{_libdir}/kamailio/modules/outbound.so


%if %{with perl}
%files      perl
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.app_perl
%doc %{_docdir}/kamailio/modules/README.db_perlvdb
%{_libdir}/kamailio/modules/app_perl.so
%{_libdir}/kamailio/modules/db_perlvdb.so
%dir %{_libdir}/kamailio/perl
%{_libdir}/kamailio/perl/Kamailio.pm
%dir %{_libdir}/kamailio/perl/Kamailio
%{_libdir}/kamailio/perl/Kamailio/Constants.pm
%{_libdir}/kamailio/perl/Kamailio/Message.pm
%{_libdir}/kamailio/perl/Kamailio/VDB.pm
%dir %{_libdir}/kamailio/perl/Kamailio/LDAPUtils
%{_libdir}/kamailio/perl/Kamailio/LDAPUtils/LDAPConf.pm
%{_libdir}/kamailio/perl/Kamailio/LDAPUtils/LDAPConnection.pm
%dir %{_libdir}/kamailio/perl/Kamailio/Utils
%{_libdir}/kamailio/perl/Kamailio/Utils/Debug.pm
%{_libdir}/kamailio/perl/Kamailio/Utils/PhoneNumbers.pm
%dir %{_libdir}/kamailio/perl/Kamailio/VDB
%{_libdir}/kamailio/perl/Kamailio/VDB/Column.pm
%{_libdir}/kamailio/perl/Kamailio/VDB/Pair.pm
%{_libdir}/kamailio/perl/Kamailio/VDB/ReqCond.pm
%{_libdir}/kamailio/perl/Kamailio/VDB/Result.pm
%{_libdir}/kamailio/perl/Kamailio/VDB/VTab.pm
%{_libdir}/kamailio/perl/Kamailio/VDB/Value.pm
%dir %{_libdir}/kamailio/perl/Kamailio/VDB/Adapter
%{_libdir}/kamailio/perl/Kamailio/VDB/Adapter/AccountingSIPtrace.pm
%{_libdir}/kamailio/perl/Kamailio/VDB/Adapter/Alias.pm
%{_libdir}/kamailio/perl/Kamailio/VDB/Adapter/Auth.pm
%{_libdir}/kamailio/perl/Kamailio/VDB/Adapter/Describe.pm
%{_libdir}/kamailio/perl/Kamailio/VDB/Adapter/Speeddial.pm
%{_libdir}/kamailio/perl/Kamailio/VDB/Adapter/TableVersions.pm
%endif


%if %{with phonenum}
%files      phonenum
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.phonenum
%{_libdir}/kamailio/modules/phonenum.so
%endif


%files      postgresql
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.db_postgres
%{_libdir}/kamailio/modules/db_postgres.so
%{_libdir}/kamailio/kamctl/kamctl.pgsql
%{_libdir}/kamailio/kamctl/kamdbctl.pgsql
%dir %{_datadir}/kamailio/postgres
%{_datadir}/kamailio/postgres/*


%files      presence
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.presence
%doc %{_docdir}/kamailio/modules/README.presence_conference
%doc %{_docdir}/kamailio/modules/README.presence_dfks
%doc %{_docdir}/kamailio/modules/README.presence_dialoginfo
%doc %{_docdir}/kamailio/modules/README.presence_mwi
%doc %{_docdir}/kamailio/modules/README.presence_profile
%doc %{_docdir}/kamailio/modules/README.presence_reginfo
%doc %{_docdir}/kamailio/modules/README.presence_xml
%doc %{_docdir}/kamailio/modules/README.pua
%doc %{_docdir}/kamailio/modules/README.pua_bla
%doc %{_docdir}/kamailio/modules/README.pua_dialoginfo
%if %{with json}
%doc %{_docdir}/kamailio/modules/README.pua_json
%endif
%doc %{_docdir}/kamailio/modules/README.pua_reginfo
%doc %{_docdir}/kamailio/modules/README.pua_usrloc
%doc %{_docdir}/kamailio/modules/README.pua_xmpp
%doc %{_docdir}/kamailio/modules/README.rls
%doc %{_docdir}/kamailio/modules/README.xcap_client
%doc %{_docdir}/kamailio/modules/README.xcap_server
%{_libdir}/kamailio/modules/presence.so
%{_libdir}/kamailio/modules/presence_conference.so
%{_libdir}/kamailio/modules/presence_dfks.so
%{_libdir}/kamailio/modules/presence_dialoginfo.so
%{_libdir}/kamailio/modules/presence_mwi.so
%{_libdir}/kamailio/modules/presence_profile.so
%{_libdir}/kamailio/modules/presence_reginfo.so
%{_libdir}/kamailio/modules/presence_xml.so
%{_libdir}/kamailio/modules/pua.so
%{_libdir}/kamailio/modules/pua_bla.so
%{_libdir}/kamailio/modules/pua_dialoginfo.so
%if %{with json}
%{_libdir}/kamailio/modules/pua_json.so
%endif
%{_libdir}/kamailio/modules/pua_reginfo.so
%{_libdir}/kamailio/modules/pua_usrloc.so
%{_libdir}/kamailio/modules/pua_xmpp.so
%{_libdir}/kamailio/modules/rls.so
%{_libdir}/kamailio/modules/xcap_client.so
%{_libdir}/kamailio/modules/xcap_server.so


%files      python
%defattr(-,root,root)
%if %{with python2}
%doc %{_docdir}/kamailio/modules/README.app_python
%{_libdir}/kamailio/modules/app_python.so
%endif
%if %{with python3}
%doc %{_docdir}/kamailio/modules/README.app_python3
%doc %{_docdir}/kamailio/modules/README.app_python3s
%{_libdir}/kamailio/modules/app_python3.so
%{_libdir}/kamailio/modules/app_python3s.so
%endif


%if %{with rabbitmq}
%files      rabbitmq
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.rabbitmq
%{_libdir}/kamailio/modules/rabbitmq.so
%endif


%files      radius
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.acc_radius
%doc %{_docdir}/kamailio/modules/README.auth_radius
%doc %{_docdir}/kamailio/modules/README.misc_radius
%doc %{_docdir}/kamailio/modules/README.peering
%{_libdir}/kamailio/modules/acc_radius.so
%{_libdir}/kamailio/modules/auth_radius.so
%{_libdir}/kamailio/modules/misc_radius.so
%{_libdir}/kamailio/modules/peering.so


%if %{with redis}
%files      redis
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.db_redis
%doc %{_docdir}/kamailio/modules/README.ndb_redis
%doc %{_docdir}/kamailio/modules/README.topos_redis
%{_libdir}/kamailio/modules/db_redis.so
%{_libdir}/kamailio/modules/ndb_redis.so
%{_libdir}/kamailio/modules/topos_redis.so
%dir %{_datadir}/kamailio/db_redis
%{_datadir}/kamailio/db_redis/*
%endif


%files      regex
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.regex
%{_libdir}/kamailio/modules/regex.so


%files      rtjson
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.rtjson
%{_libdir}/kamailio/modules/rtjson.so


%if %{with ruby}
%files      ruby
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.app_ruby
%doc %{_docdir}/kamailio/modules/README.app_ruby_proc
%{_libdir}/kamailio/modules/app_ruby.so
%{_libdir}/kamailio/modules/app_ruby_proc.so
%endif


%if %{with sctp}
%files      sctp
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.sctp
%{_libdir}/kamailio/modules/sctp.so
%endif


%files      secfilter
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.secfilter
%{_libdir}/kamailio/modules/secfilter.so


%files      sipdump
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.sipdump
%{_libdir}/kamailio/modules/sipdump.so


%files      sipjson
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.sipjson
%{_libdir}/kamailio/modules/sipjson.so


%files      slack
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.slack
%{_libdir}/kamailio/modules/slack.so


%files      snmpstats
%defattr(-,root,root)
%{_docdir}/kamailio/modules/README.snmpstats
%{_libdir}/kamailio/modules/snmpstats.so
%{_datadir}/snmp/mibs/KAMAILIO-MIB
%{_datadir}/snmp/mibs/KAMAILIO-REG-MIB
%{_datadir}/snmp/mibs/KAMAILIO-SIP-COMMON-MIB
%{_datadir}/snmp/mibs/KAMAILIO-SIP-SERVER-MIB
%{_datadir}/snmp/mibs/KAMAILIO-TC


%files      statsd
%defattr(-,root,root)
%{_docdir}/kamailio/modules/README.statsd
%{_libdir}/kamailio/modules/statsd.so


%files      sqlite
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.db_sqlite
%{_libdir}/kamailio/modules/db_sqlite.so
%{_libdir}/kamailio/kamctl/kamctl.sqlite
%{_libdir}/kamailio/kamctl/kamdbctl.sqlite
%dir %{_datadir}/kamailio/db_sqlite
%{_datadir}/kamailio/db_sqlite/*


%files      tls
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.tls
%{_libdir}/kamailio/modules/tls.so


%if %{with wolfssl}
%files      tls_wolfssl
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.tls_wolfssl
%{_libdir}/kamailio/modules/tls_wolfssl.so
%endif


%files      tcpops
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.tcpops
%{_libdir}/kamailio/modules/tcpops.so


%files      unixodbc
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.db_unixodbc
%{_libdir}/kamailio/modules/db_unixodbc.so


%files      utils
%defattr(-,root,root)
%{_docdir}/kamailio/modules/README.utils
%{_libdir}/kamailio/modules/utils.so


%if %{with websocket}
%files      websocket
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.websocket
%{_libdir}/kamailio/modules/websocket.so
%endif


%files      xhttp-pi
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.xhttp_pi
%{_libdir}/kamailio/modules/xhttp_pi.so
%dir %{_datadir}/kamailio/xhttp_pi
%{_datadir}/kamailio/xhttp_pi/*


%files      xmlops
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.xmlops
%{_libdir}/kamailio/modules/xmlops.so


%if %{with xmlrpc}
%files      xmlrpc
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.xmlrpc
%{_libdir}/kamailio/modules/xmlrpc.so
%endif


%files      xmpp
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.xmpp
%{_libdir}/kamailio/modules/xmpp.so


%files          uuid
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.uuid
%{_libdir}/kamailio/modules/uuid.so


%changelog
* Tue Sep 13 2022 Gustavo Almeida <galmeida@broadvoice.com>
  - added readline-devel build dependency
* Sat Aug 31 2019 Sergey Safarov <s.safarov@gmail.com> 5.3.0-dev7
  - Packaged kemix, lost and xhttp_prom modules
* Sat Mar 30 2019 Sergey Safarov <s.safarov@gmail.com> 5.3.0-0
  - Added support of openSUSE:Leap:15.0, openSUSE:Leap:15.1 and Fedora 30 dists
* Thu Feb 21 2019 Sergey Safarov <s.safarov@gmail.com> 5.3.0-0
  - Added secfilter package
* Tue Dec 11 2018 Sergey Safarov <s.safarov@gmail.com> 5.2.0-1
  - Added Ruby package
* Sun Nov 04 2018 Sergey Safarov <s.safarov@gmail.com> 5.2.0-0
  - removed packaging for Fedora 25, 26 as End Of Life
* Sat Sep 02 2017 Sergey Safarov <s.safarov@gmail.com>
  - added packaging for Fedora 26 and openSUSE Leap 42.3
  - removed packaging for Fedora 24 and openSUSE Leap 42.1 as End Of Life
  - rewrited SPEC file to support Fedora, RHEL, CentOS, openSUSE distrs
* Mon Jul 31 2017 Mititelu Stefan <stefan.mititelu92@gmail.com>
  - added rabbitmq module
* Wed Apr 26 2017 Carsten Bock <carsten@ng-voice.co,>
  - added ims_diameter_server module
  - added topos_redis module
  - added call_obj module
  - added evrexec module
  - added keepalive module
  - added app_sqlang module
* Thu Mar 09 2017 Federico Cabiddu <federico.cabiddu@gmail.com>
  - added jansson package
* Sat Feb 04 2017 Federico Cabiddu <federico.cabiddu@gmail.com>
  - added http_async_client package
  - fix http_client package
* Fri Nov 04 2016 Marcel Weinberg <marcel@ng-voice.com>
  - Updated to Kamailio version 5.0 and CentOS / RHEL 7.2
  - added new modules available with Kamailio 5.x
    - cfgt
    - crypto
    - http_client
    - log_custom
    - smsops
    - statsc
    - topos
  - removed dialog_ng references and added ims_dialog to replace dialog_ng
  - removed java module which requires libgcj
    - libgcj is no longer supported by RHEL / CentOS (Version >= 7)
    - it's recommended to replace libgcj as dependency
  - added the ims_registrar_pcscf module
* Tue Dec 3 2013 Peter Dunkley <peter.dunkley@crocodilertc.net>
  - Updated version to 4.2.0
* Mon Oct 7 2013 Peter Dunkley <peter.dunkley@crocodilertc.net>
  - Consolidating changelog for 4.1.0 into a single entry...
  - Added new modules to main package:
    - cnxcc
    - gzcompress
    - mohqueue
    - rtpproxy-ng
    - sipt
    - stun (STUN functionality moved from compile time in core to own module)
  - Added new modules to other packages:
    - ims_charging module to ims package
  - Added new packages for new modules:
    - app_java
    - auth_ephemeral
    - sctp (SCTP functionality moved from compile time in core to own module)
  - Moved existing modules to different packages:
    - auth_identity to tls package (previously not built for CentOS)
    - cdp and cdp_avp to ims package
    - dialog_ng to main package
    - memcached to own package (previously not built for CentOS)
    - mi_xmlrpc to own package (previously not built for CentOS)
    - tls to own package
  - Added packages for (new and existing) modules that require EPEL:
    - carrierroute in own package
    - dnssec in own package
    - geoip in own package
    - json and jsonrpc-c in new json package
    - redis in own package
    - acc_radius, auth_radius, misc_radius, and peering in new radius package
  - Removed Fedora stuff as I am only maintaining this for CentOS now
  - Refactored .spec
  - Updated make commands to match updated module groups
  - Updated version to 4.1.0
* Mon Mar 11 2013 Peter Dunkley <peter.dunkley@crocodilertc.net>
  - Consolidating changelog for 4.0.0 into a single entry...
  - Added new modules to main package:
    - corex
    - sca
  - Added new packages for new modules:
    - cdp (cdp, cdp_avp)
    - ims (dialog_ng, ims_auth, ims_icscf, ims_isc, ims_qos,
      ims_registrar_pcscf, ims_registrar_scscf, ims_usrloc_pcscf,
      ims_usrloc_scscf)
    - outbound
    - websocket
    - xhttp_pi
  - Moved existing modules to different packages:
    - Various SER modules added to main package (avp, db2_ops, mangler, timer,
      uid_auth_db, uid_avp_db, uid_domain, uid_gflags, uid_uri_db, print,
      print_lib, xprint)
    - db2_ldap SER module added to ldap package
    - tls to main package (as OpenSSL was needed in core for STUN)
  - Moved modules from modules_k/ to modules/
  - Renamed perl modules
  - Added installation of auth.7.gz for Fedora now that manpages are built for
    Fedora
  - SCTP and STUN now included in this build
  - Refactored .spec
  - Updated ver to 4.0.0
* Mon Jun 18 2012 Peter Dunkley <peter.dunkley@crocodilertc.net>
  - Consolidating changelog for 3.3.0 into a single entry...
  - See revision control for details this far back
