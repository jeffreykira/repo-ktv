service.zfs
-----------

A simple Script for checking ZFS Status in Kodi Mediaplayer.


If Kodi is not running as root, the user must have the priveleges to run "zpool status".

On Arch Linux you can use this commands:

>    echo 'ACTION=="add", KERNEL=="zfs", MODE="0660", GROUP="zfs"' >> /etc/udev/rules.d/91-zfs-permissions.rules
>    groupadd zfs
>    gpasswd -a kodi zfs

