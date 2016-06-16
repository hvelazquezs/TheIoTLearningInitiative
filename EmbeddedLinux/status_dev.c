/*
 * "status" minimal kernel module - /dev version
 *
 * Hector Velazquez <hvelazquezs@hotmail.com>
 *
 */

#include <linux/fs.h>
#include <linux/init.h>
#include <linux/miscdevice.h>
#include <linux/module.h>

#include <asm/uaccess.h>

//#include <linux/random.h>
#include <linux/string.h>
#include <linux/math64.h>

/*Generate a random number routine*/
static unsigned long next=1;
/*RAND?MAX assumed to be 32767*/
int RandNumb(void) {
	next = next * 1103515245+12345;
	return((unsigned)(next/65536)%32768);

}
/*
 * status_read is the function called when a process calls read() on
 * /dev/status.  It writes "status" to the buffer passed in the
 * read() call.
 */

static ssize_t status_read(struct file * file, char * buf, 
			  size_t count, loff_t *ppos)
{
	
	char *status_str = "...in progress \n"; 
	int len = strlen(status_str);
	unsigned int seed, i;
	const char digiMap[] = "0123456789abcdef";
	seed = RandNumb();
	if (seed == 0) {
		status_str="0 \n";
	}
	for (i=30; seed && i; --seed) {
		status_str= digiMap[i] + status_str;
	}

	
	/* Don't include the null byte. */
	/*
	 * We only support reading the whole string at once.
	 */
	if (count < len)
		return -EINVAL;
	/*
	 * If file position is non-zero, then assume the string has
	 * been read and indicate there is no more data to be read.
	 */
	if (*ppos != 0)
		return 0;
	/*
	 * Besides copying the string to the user provided buffer,
	 * this function also checks that the user has permission to
	 * write to the buffer, that it is mapped, etc.
	 */
	
	if (copy_to_user(buf, status_str, len))
		return -EINVAL;
	/*
	 * Tell the user how much data we wrote.
	 */
	*ppos = len;

	return len;
}

/*
 * The only file operation we care about is read.
 */

static const struct file_operations status_fops = {
	.owner		= THIS_MODULE,
	.read		= status_read,
};

static struct miscdevice status_dev = {
	/*
	 * We don't care what minor number we end up with, so tell the
	 * kernel to just pick one.
	 */
	MISC_DYNAMIC_MINOR,
	/*
	 * Name ourselves /dev/status.
	 */
	"status",
	/*
	 * What functions to call when a program performs file
	 * operations on the device.
	 */
	&status_fops
};

static int __init
status_init(void)
{
	int ret;

	/*
	 * Create the "status" device in the /sys/class/misc directory.
	 * Udev will automatically create the /dev/status device using
	 * the default rules.
	 */
	ret = misc_register(&status_dev);
	if (ret)
		printk(KERN_ERR
		       "Unable to register \"status\" misc device\n");

	return ret;
}

module_init(status_init);

static void __exit
status_exit(void)
{
	misc_deregister(&status_dev);
}

module_exit(status_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Hector Velazquez <hvelazquezs@hotmail.com>");
MODULE_DESCRIPTION("\"status\" minimal module");
MODULE_VERSION("dev");
