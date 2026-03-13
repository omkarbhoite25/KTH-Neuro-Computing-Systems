# Build the C accelerator for the event camera accumulator
# Usage: make

CC = gcc
CFLAGS = -O3 -shared -fPIC -Wall -Wextra
TARGET = libaccumulator.so

all: $(TARGET)

$(TARGET): accumulator.c
	$(CC) $(CFLAGS) -o $@ $< -lm

clean:
	rm -f $(TARGET)

.PHONY: all clean
