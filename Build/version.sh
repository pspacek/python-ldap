#! /bin/sh
# $Id: version.sh,v 1.1 2000/08/14 03:19:12 leonard Exp $

#
# Extract the current version number from configure.in
#

CONFIGURE_IN=`dirname $0`/../configure.in
sed -n -e 's/^AC_DEFINE(LDAPMODULE_VERSION, \(.*\)).*/\1/p' \
		< $CONFIGURE_IN

