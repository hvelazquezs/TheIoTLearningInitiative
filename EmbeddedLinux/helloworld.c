#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>

static int module_init_function(void)
{
    printk(KERN_INFO "Module? Hello Hector Velazquez!\n");
    return 0;
}

static void module_exit_function(void)
{
    printk(KERN_INFO "Module? Bye Hector Velazquez!\n");
}

MODULE_LICENSE("GPL");
MODULE_AUTHOR("hvelazquezs");
MODULE_DESCRIPTION("My First Linux Kernel Module");

module_init(module_init_function);
module_exit(module_exit_function);

