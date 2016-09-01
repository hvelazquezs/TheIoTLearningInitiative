mkdir /media/flashdrive/
 
sudo mount /dev/sda1 /media/flashdrive



dd if=/dev/mmcblk0 of=/media/flashdrive/BackupFile bs=4M

umount /media/flashdrive/



