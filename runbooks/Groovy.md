# Ubuntu Server 20.10 (Groovy)

## Boot drive

Download Ubuntu Server 20.10 64 bits for Raspberry Pi 4. 20.04 LTS does not support USB boot.

Install Rasbperry Pi Imager. Create the boot drive.

## Network bootstrap

Connect a computer and the Raspberry Pi over Ethernet.

Configure the computer's Ethernet interface to use the static IP address 192.168.100.2/24.

Boot the Raspberry Pi from the drive. Change the password (default credentials: ubuntu/ubuntu).

Prevent cloudinit from managing the network. Create `/etc/cloud/cloud.cfg.d/99-disable-network-config.cfg`.

    network: {config: disabled}

Configure netplan. Create `/etc/netplan/01-network.yaml`.

    network:
      version: 2
      ethernets:
        eth0:
          dhcp4: false
          addresses: [192.168.100.1/24]
      wifis:
        wlan0:
          dhcp4: true
          optional: true
          access-points:
            "ssid":
              password: "password"

Apply the configuration.

    sudo netplan generate
    sudo netplan apply

Test internet connection.

Test SSH connection over Ethernet.

    ssh ubuntu@192.168.100.1

## Fix network-online.target

By default `network-online.target` does not wait for interfaces to be up.

Create `/usr/local/sbin/wait-localnet.sh`. Change the permissions to 0755.

    #!/usr/bin/env bash
    set -euo pipefail
    while [ "$(ip addr | grep eth0 | grep 192\.168\.100\.1 | wc -l)" = "0" ]; do sleep 1; done

Create `/etc/systemd/system/wait-localnet.service`.

    [Unit]
    After=network.target
    Before=network-online.target

    [Service]
    Type=oneshot
    RemainAfterExit=yes
    TimeoutStartSec=1min
    ExecStart=/usr/local/sbin/wait-localnet.sh

    [Install]
    WantedBy=network-online.target

Enable the service.

    sudo systemctl daemon-reload
    sudo systemctl enable wait-localnet

## SSH server

Install the computer's public key to the Raspberry Pi.

    ssh-copy-id -i ~/.ssh/id_ed25519.pub ubuntu@192.168.100.1

Add the following line to `/etc/ssh/sshd_config`.

    ListenAddress 192.168.100.1

Update the following line in `/etc/ssh/sshd_config`.

    PasswordAuthentication no

Restart the SSH server.

    sudo systemctl restart ssh

Edit `/etc/systemd/system/sshd.service`. Update the dependencies.

    # After=network.target auditd.service
    After=network-online.target auditd.service
    Wants=network-online.target

## Network configuration

Change the hostname in `/etc/hostname` to rpi. Reboot.

Add an entry for rpi in `/etc/hosts`.

    192.168.100.1 rpi

Disable resolved.

    sudo systemctl stop systemd-resolved
    sudo systemctl disable systemd-resolved

Delete the symbolic link `/etc/resolv.conf`. Create `/etc/resolv.conf` as a regular file.

    nameserver 1.1.1.1

Install dnsmasq.

    sudo apt install dnsmasq

Create `/etc/dnsmasq.d/localnet.conf`.

    interface=eth0
    dhcp-range=192.168.100.100,192.168.100.200,255.255.255.0,12h
    port=53
    domain=localnet
    local=/localnet/
    expand-hosts
    domain-needed
    bogus-priv
    server=1.1.1.1

Restart dnsmasq

    sudo systemctl restart dnsmasq

Update `/etc/resolv.conf`.

    nameserver 127.0.0.1

Configure the computer's Ethernet interface to use DHCP. Reconnect to the Ethernet network.

Test the DNS server.

    ssh ubuntu@rpi.localnet

## Timezone

    sudo dpkg-reconfigure tzdata

## Software

    sudo apt remove --purge nano
