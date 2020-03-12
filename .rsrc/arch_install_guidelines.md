[a guide](https://www.youtube.com/watch?v=i5IQMZVT8Bo)

> timedatectl set-ntp true

```
ping -q -c 1 google.com
if [[ $? -ne 0 ]]; then
	echo 'need to set up wifi'
	wifi-menu
	echo "now run sudo netctl start <service>"
fi
```

* cfdisk /dev/sdx
* gpt scheme
* partitions
	* 1 600M EFI
	* 2 20G Linux Filesystem
	* 3 12G Linux swap
	* 4 the rest Linux Filesystem

* format

```
mkfs.fat -F32 /dev/sda1
mkfs.ext4 /dev/sda2
mkswap /dev/sda3
swapon /dev/sda3
mkfs.ext4 /dev/sda4
```

* mount

```
mount /dev/sda2 /mnt
mkdir /mnt/boot
mkdir /mnt/boot/efi
mount /dev/sda1 /mnt/boot/efi
mkdir /mnt/home
mount /dev/sda4 /mnt/home
```

* all important packages

```
pacman -Syy
pacstrap /mnt base base-devel linux linux-firmware efibootmgr vim git dhcpcd dhclient networkmanager man-db man-pages sudo openssh grub netctl dialog python3 python-pip xonsh i3-gaps xorg-xinit xorg-server picom lxappearance pcmanfm code unclutter konsole firefox
```

* system config

```
genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot /mnt
ln -sf /usr/share/zoneinfo/America/Detroit /etc/localtime
hwclock --systohc
echo "LANG=en_US>UTF-8" > /etc/local.conf
locale-gen
echo lilylake > /etc/hostname
```

> vim /etc/hosts
* and paste the following

```
127.0.0.1	localhost
::1			localhost
127.0.0.1	hostname.localdomain	hostname
```

* more system setup

```
systemctl enable NetworkManager
passwd
grub-install --target=x86_64-efi --efi-directory=/boot/efi
grub-mkconfig -o /boot/grub/grub.cfg
exit
umount -R /mnt
```

* reboot
* login as root with password

* create a user

```
useradd -m 'username'
passwd 'username'
```

> vim /etc/sudoers
* and add/uncomment the following

```
%wheel ALL=(ALL) NOPASSWD: ALL
```

> usermod -aG wheel 'username'

* verify this worked

> groups 'username'

* [get internet](https://www.youtube.com/watch?v=MAi9DurTRQc)

> nmcli device wifi connect 'SSID' password 'password'

pip install pygments
```
__init__.py for pytest but fucks up source_executables
```
