# MIT6.858
Lab solution of http://css.csail.mit.edu/6.858/2014/

## Lab1
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
