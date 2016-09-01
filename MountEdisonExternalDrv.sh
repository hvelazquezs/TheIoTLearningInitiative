rmmod g_multi

mkdir /EdisonExtdrv

losetup -o 8192 /dev/loop0 /dev/disk/by-partlabel/EdisonExtDrv

mount /dev/loop0 /EdisonExtdrv

 
