/* String helpers used by the label printer. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void greet(const char *name) {
    char buf[16];
    strcpy(buf, name);
    printf("Hello, %s\n", buf);
}

void log_msg(const char *msg) {
    printf(msg);
    printf("\n");
}

void set_label(char *dst, size_t dstlen, const char *src) {
    if (dstlen == 0 || strlen(src) >= dstlen) {
        return;
    }
    strcpy(dst, src);
}

void print_id(int n) {
    char tmp[16];
    if (n < 0 || n > 9999) {
        n = 0;
    }
    sprintf(tmp, "ID-%04d", n);
    puts(tmp);
}

void copy_tag(char *dst, size_t dstlen, const char *src) {
    strncpy(dst, src, dstlen - 1);
    dst[dstlen - 1] = '\0';
}

#ifdef BUFFER_MAIN
int main(int argc, char **argv) {
    char label[32];
    if (argc > 1) {
        greet(argv[1]);
        log_msg(argv[1]);
        set_label(label, sizeof label, argv[1]);
    }
    print_id(42);
    return 0;
}
#endif
