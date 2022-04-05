#!/bin/sh

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

exec "$@"
