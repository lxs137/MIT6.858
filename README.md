# MIT6.858
Lab solution of http://css.csail.mit.edu/6.858/2014/

## Lab1
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

### part-2
* [exploit-2a](lab1/zook-server/exploit-2a.py)
* [exploit-2b](lab1/zook-server/exploit-2b.py) 
> this buffer overflow can cause process crash, but this process is a child process
> parent process will still alive, so `make check-crash` will not pass

### part-3
* [exploit-3](lab1/zook-server/exploit-3.py)
* [shellcode](lab1/zook-server/shellcode.S)

### part-4
* [exploit-4a](lab1/zook-server/exploit-4a.py)
* [exploit-4b](lab1/zook-server/exploit-4b.py) 
