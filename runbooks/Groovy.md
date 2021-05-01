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

### Ethernet

Configure the Ethernet interface with systemd-network. Netplan does not support `ConfigureWithoutCarrier` for physical interfaces.

Create `/etc/systemd/network/01-eth0.link`.

    [Match]
    Driver=bcmgenet smsc95xx lan78xx
    OriginalName=eth0

    [Link]
    Name=eth0
    WakeOnLan=off

Create `/etc/systemd/network/01-eth0.network`.

    [Match]
    Driver=bcmgenet smsc95xx lan78xx
    Name=eth0

    [Link]
    RequiredForOnline=no

    [Network]
    DHCP=ipv4
    LinkLocalAddressing=ipv6
    Address=192.168.100.1/24
    ConfigureWithoutCarrier=true

    [DHCP]
    RouteMetric=100
    UseMTU=true

Apply the configuration.

    systemctl restart systemd-networkd

Test the SSH connection over Ethernet.

    ssh ubuntu@192.168.100.1

### WiFi

Configure the WiFi interface with Netplan. Create `/etc/netplan/01-network.yaml`.

    network:
      version: 2
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

Test the internet connection.

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

## Apt

### Suggested packages

By default installing a package does not automatically install the packages it suggests. However packages suggested by other installed packages are not automatically removed. This often prevents packages which are no longer required from being automatically removed.

Create `/etc/apt/apt.conf.d/99_nosuggests` with the following contents.

    APT::AutoRemove::SuggestsImportant "false";

### History

Edit `/etc/logrotate.d/apt` and set rotate to 60 to keep `history.log` for 5 years.

## Timezone

    sudo dpkg-reconfigure tzdata

## Software

    sudo apt remove --purge nano
