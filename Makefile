CFLAGS ?= -Wall -Wextra -g -O0
CXXFLAGS ?= -Wall -Wextra -g -O0 -std=c++17

all: buffer cache parser

buffer: buffer.c
	$(CC) $(CFLAGS) -DBUFFER_MAIN -o $@ $<

cache: cache.c
	$(CC) $(CFLAGS) -DCACHE_MAIN -o $@ $<

parser: parser.cpp
	$(CXX) $(CXXFLAGS) -DPARSER_MAIN -o $@ $<

clean:
	rm -f buffer cache parser inventory.db

.PHONY: all clean
