mkdir /media/flashdrive/
 
sudo mount /dev/sda1 /media/flashdrive



dd if=/media/flashdrive/BackupFile bs=4M of=/dev/mmcblk0

umount /media/flashdrive/



