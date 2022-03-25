#!/bin/sh
#-*-Mode:sh;coding:utf-8;tab-width:4;c-basic-offset:4;indent-tabs-mode:()-*-
# ex: set ft=sh fenc=utf-8 sts=4 ts=4 sw=4 et nomod:

trap "cloudi stop; exit 0" HUP TERM TSTP
trap "cloudi stop" INT

# Configure ssh allowing root and X11 access
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/#X11UseLocalhost yes/X11UseLocalhost no/' /etc/ssh/sshd_config
sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
mkdir -p /var/run/sshd
if [ ! -f "/etc/ssh/ssh_host_rsa_key" ]; then
  # generate fresh rsa key
  ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa
fi

# set permissions
mkdir -p ${HOME}/.cache
mkdir -p ${HOME}/.local
chown -Rh ${USER_ID_GID} ${HOME}/.cache
chown -Rh ${USER_ID_GID} ${HOME}/.local
# chown -Rh ${USER_ID_GID} /usr/local/bin/cloudi

#gosu ${USER_ID_GID} bash << EOF
cloudi console
#EOF
