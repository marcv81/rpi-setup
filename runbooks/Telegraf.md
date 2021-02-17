# Telegraf

## Installation

Download and install Telegraf.

    wget https://dl.influxdata.com/telegraf/releases/telegraf-1.17.2_linux_armhf.tar.gz
    tar xvf telegraf-1.17.2_linux_armhf.tar.gz
    sudo cp telegraf-1.17.2/usr/bin/telegraf /usr/bin/
    sudo cp telegraf-1.17.2/usr/lib/telegraf/scripts/telegraf.service /etc/systemd/system/

Create the telegraf user.

    sudo groupadd -r telegraf
    sudo useradd -r -M telegraf -g telegraf
    sudo usermod -L telegraf

## Quiet logs

Add the following line to `/etc/pam.d/sudo`, just before `@include common-session-noninteractive`.

    session [success=1 default=ignore] pam_succeed_if.so quiet uid = 0 ruser = telegraf

Add the following line to `/etc/sudoers.d/telegraf`.

    Defaults:telegraf !syslog

## Dependencies

### SMART

Install smartctl, but disable smartd.

    sudo apt install smartmontools
    sudo systemctl stop smartd
    sudo systemctl disable smartd

Allow the telegraf user to run smartctl in `/etc/sudoers.d/telegraf`.

    telegraf ALL=(root) NOPASSWD: /usr/sbin/smartctl

### CPU stats

Install `cpu_stats.py` from https://github.com/marcv81/cpu-stats to `/usr/local/bin`.

## Configuration

Use `/etc/telegraf/telegraf.conf` from the files directory.

Start and enable the service.

    sudo systemctl daemon-reload
    sudo systemctl start telegraf
    sudo systemctl enable telegraf
