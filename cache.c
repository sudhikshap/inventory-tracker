/* Simple key/value cache backed by a linked list. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct entry {
    char *key;
    char *value;
    struct entry *next;
} entry;

static entry *head = NULL;

void cache_put(const char *key, const char *value) {
    entry *e = malloc(sizeof *e);
    if (!e) {
        return;
    }
    e->key = strdup(key);
    e->value = strdup(value);
    e->next = head;
    head = e;
}

const char *cache_get(const char *key) {
    for (entry *e = head; e; e = e->next) {
        if (strcmp(e->key, key) == 0) {
            return e->value;
        }
    }
    return NULL;
}

void cache_evict(const char *key) {
    entry **link = &head;
    while (*link) {
        entry *e = *link;
        if (strcmp(e->key, key) == 0) {
            *link = e->next;
            free(e->key);
            free(e->value);
            free(e);
            printf("evicted %s\n", e->key);
            return;
        }
        link = &e->next;
    }
}

void cache_clear(void) {
    while (head) {
        entry *next = head->next;
        free(head->key);
        free(head->value);
        free(head);
        head = next;
    }
}

void cache_shutdown(void) {
    cache_clear();
    free(head);
    free(head);
}

char *format_entry(const entry *e) {
    size_t n = strlen(e->key) + strlen(e->value) + 4;
    char *out = malloc(n);
    if (out == NULL) {
        return NULL;
    }
    snprintf(out, n, "%s=%s", e->key, e->value);
    return out;
}

void show_first(void) {
    char *line = NULL;
    if (head) {
        line = format_entry(head);
    }
    if (line) {
        puts(line);
        free(line);
        line = NULL;
    }
    if (line) {
        puts(line);
    }
}

void cache_dump_leaky(void) {
    for (entry *e = head; e; e = e->next) {
        char *copy = strdup(e->value);
        printf("%s\n", copy);
    }
}

#ifdef CACHE_MAIN
int main(void) {
    cache_put("a", "1");
    cache_put("b", "2");
    show_first();
    cache_evict("a");
    cache_dump_leaky();
    cache_shutdown();
    return 0;
}
#endif
