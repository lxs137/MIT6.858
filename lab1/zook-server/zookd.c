/* dispatch daemon */

#include "http.h"
#include <err.h>
#include <regex.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_SERVICES 256
static int nsvcs;
static int svcfds[MAX_SERVICES];      // 0x804c120
static regex_t svcurls[MAX_SERVICES]; // 0x804c520

static void process_client(int);

int main(int argc, char **argv)
{
    int fd, sockfd = -1, i;

    if (argc != 2)
        errx(1, "Wrong arguments");
    fd = atoi(argv[1]);

    signal(SIGPIPE, SIG_IGN);
    signal(SIGCHLD, SIG_IGN);

    /* receive the number of services and the server socket from zookld */
    if ((recvfd(fd, &nsvcs, sizeof(nsvcs), &sockfd) <= 0) || sockfd < 0)
        err(1, "recvfd sockfd");
    --nsvcs;
    warnx("Start with %d service(s)", nsvcs);

    /* receive url patterns of all services */
    for (i = 0; i != nsvcs; ++i)
    {
        char url[1024], regexp[1024];
        if (recvfd(fd, url, sizeof(url), &svcfds[i]) <= 0)
            err(1, "recvfd svc %d", i + 1);
	/* parens are necessary here so that regexes like a|b get
	   parsed properly and not as (^a)|(b$) */
        snprintf(regexp, sizeof(regexp), "^(%s)$", url);
        if (regcomp(&svcurls[i], regexp, REG_EXTENDED | REG_NOSUB))
            errx(1, "Bad url for service %d: %s", i + 1, url);
        warnx("Dispatch %s for service %d", regexp, i + 1);
    }

    close(fd);

    for (;;)
    {
        int cltfd = accept(sockfd, NULL, NULL);
        if (cltfd < 0)
            err(1, "accept");
        process_client(cltfd);
    }
}

static void process_client(int fd)
{
    // 0x804e520
    static char env[8192];  /* static variables are not on the stack */
    // 0x8050520
    static size_t env_len;
    char reqpath[2048]; // $ebp-2064
    const char *errmsg; // $ebp-16
    int i; // $ebp-12
           // $ebp-8 and $ebp -4 is callee-saved reg (%EDI, %ESI)

    /* get the request line */
    if ((errmsg = http_request_line(fd, reqpath, env, &env_len)))
        return http_err(fd, 500, "http_request_line: %s", errmsg);

    for (i = 0; i < nsvcs; ++i)
    {
        if (!regexec(&svcurls[i], reqpath, 0, 0, 0))
        {
            warnx("Forward %s to service %d", reqpath, i + 1);
            break;
        }
    }

    if (i == nsvcs)
        return http_err(fd, 500, "Error dispatching request: %s", reqpath);

    if (sendfd(svcfds[i], env, env_len, fd) <= 0)
        return http_err(fd, 500, "Error forwarding request: %s", reqpath);

    close(fd);
}
