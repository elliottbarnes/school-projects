// Address translation coursework by Elliott Barnes (2020).
// Copyright © 2020 Elliott Barnes. All rights reserved.
// 2026 completion: validate decimal 32-bit addresses before division/modulo.
#include <errno.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2 || !argv[1][0] || strspn(argv[1], "0123456789") != strlen(argv[1])) {
        fprintf(stderr, "Usage: addresses <decimal address 0..4294967295>\n");
        return 1;
    }
    errno = 0;
    char *end;
    uintmax_t address = strtoumax(argv[1], &end, 10);
    if (errno || *end || address > UINT32_MAX) {
        fprintf(stderr, "Address must be between 0 and 4294967295.\n");
        return 1;
    }
    printf("The address %" PRIuMAX " contains:\nPage Number = %" PRIuMAX "\nOffset = %" PRIuMAX "\n", address, address / 4096, address % 4096);
    return 0;
}
