# MIT6.858
Lab solution of http://css.csail.mit.edu/6.858/2014/, no lab4, lab5 (Browser security) is from [2019 version](https://css.csail.mit.edu/6.858/2019/labs/lab4.html)

## [Lab1](https://css.csail.mit.edu/6.858/2014/labs/lab1.html)
### Bugs
* zookd.c: process_client
```C
static void process_client(int fd)
...
    static char env[8192];  /* static variables are not on the stack */
    static size_t env_len;
    char reqpath[2048]; // $ebp-2064
    const char *errmsg; // $ebp-16
    int i; // $ebp-12
           // $ebp-8 and $ebp -4 is callee-saved reg (%EDI, %ESI)
```
* http.c: http_request_headers
```C
const char *http_request_headers(int fd)
...
    // i: $ebp-12
    // sp: $ebp-16
    // colon: $ebp-20
    // value: $ebp-532
    static char buf[8192];      /* static variables are not on the stack */
    int i;
    char value[512];
    char envvar[512];
```

### part-1
* [bugs.txt](lab1/zook-server/bugs.txt)

### part-2 (cause crash)
* [exploit-2a](lab1/zook-server/exploit-2a.py)
* [exploit-2b](lab1/zook-server/exploit-2b.py) 
> this buffer overflow can cause process crash, but this process is a child process
> parent process will still alive, so `make check-crash` will not pass

### part-3 (cause file deletion with exstack)
* [exploit-3](lab1/zook-server/exploit-3.py)
* [shellcode](lab1/zook-server/shellcode.S)

### part-4 (caue file deletion with nxstack)
* [exploit-4a](lab1/zook-server/exploit-4a.py)
* [exploit-4b](lab1/zook-server/exploit-4b.py)

### part-extra (chaining function calls with return-to-libc)
* [exploit-extra](lab1/zook-server/exploit-extra.py) ([guide](https://www.exploit-db.com/docs/english/28553-linux-classic-return-to-libc-&-return-to-libc-chaining-tutorial.pdf))
> sys\_unlink("/home/httpd/grades.txt") -> pop/ret -> touch("grades.txt") (http.c:18) -> sys\_exit()
