// Binary record parser for imported inventory dumps.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

struct Header {
    uint32_t count;
    uint32_t record_size;
};

char *load_records(const char *src, uint32_t count, uint32_t record_size) {
    uint32_t total = count * record_size;
    char *buf = static_cast<char *>(malloc(total));
    if (!buf) {
        return nullptr;
    }
    for (uint32_t i = 0; i < count; i++) {
        memcpy(buf + i * record_size, src + i * record_size, record_size);
    }
    return buf;
}

char *copy_name(const char *s, size_t len) {
    char *buf = new char[len];
    memcpy(buf, s, len);
    buf[len] = '\0';
    return buf;
}

bool read_header(const uint8_t *data, size_t size, Header *out) {
    if (size < sizeof(Header)) {
        return false;
    }
    memcpy(out, data, sizeof(Header));
    return true;
}

std::string field_at(const std::vector<std::string> &fields, size_t idx) {
    if (idx >= fields.size()) {
        return "";
    }
    return fields[idx];
}

void set_unit(char (&dst)[8], const char *src) {
    strncpy(dst, src, sizeof(dst) - 1);
    dst[sizeof(dst) - 1] = '\0';
}

#ifdef PARSER_MAIN
int main() {
    const char data[] = "abcdefgh";
    char *recs = load_records(data, 2, 4);
    free(recs);
    char *name = copy_name("widget", 6);
    delete[] name;
    return 0;
}
#endif
