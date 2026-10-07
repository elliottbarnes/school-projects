// Page replacement coursework by Elliott Barnes (2020).
// Copyright © 2020 Elliott Barnes. All rights reserved.
// 2026 completion: bounded deterministic inputs and corrected LRU victim selection.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#define MAX_REFERENCES 40
#define MAX_FRAMES 10

static int number(const char *text, int low, int high) {
    if (!*text || strspn(text, "0123456789") != strlen(text)) return -1;
    errno = 0;
    char *end;
    long value = strtol(text, &end, 10);
    return errno || *end || value < low || value > high ? -1 : (int)value;
}
static int simulate(const int *references, int count, int capacity, int policy) {
    const char *names[] = {"FIFO", "LRU", "OPT"};
    int frames[MAX_FRAMES], last[MAX_FRAMES], used = 0, cursor = 0, faults = 0;
    for (int i = 0; i < capacity; i++) { frames[i] = -1; last[i] = -1; }
    for (int step = 0; step < count; step++) {
        int page = references[step], slot = -1;
        for (int i = 0; i < used; i++) if (frames[i] == page) slot = i;
        int hit = slot >= 0;
        if (!hit) {
            faults++;
            if (used < capacity) slot = used++;
            else if (policy == 0) { slot = cursor; cursor = (cursor + 1) % capacity; }
            else if (policy == 1) {
                slot = 0;
                for (int i = 1; i < capacity; i++) if (last[i] < last[slot]) slot = i;
            } else {
                int farthest = -1;
                slot = 0;
                for (int i = 0; i < capacity; i++) {
                    int next = count;
                    for (int j = step + 1; j < count; j++) if (references[j] == frames[i]) { next = j; break; }
                    if (next > farthest) { farthest = next; slot = i; }
                }
            }
            frames[slot] = page;
        }
        last[slot] = step;
        printf("%s step %d: %d %s |", names[policy], step + 1, page, hit ? "hit" : "fault");
        for (int i = 0; i < capacity; i++) printf(" %d", frames[i]);
        printf("\n");
    }
    printf("Total Number of Page Faults (%s): %d\n", names[policy], faults);
    return faults;
}
int main(int argc, char **argv) {
    int references[MAX_REFERENCES] = {7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1};
    int count = 20, capacity = 3;
    if (argc > 1) capacity = number(argv[1], 1, MAX_FRAMES);
    if (capacity < 0 || argc > MAX_REFERENCES + 2) goto invalid;
    if (argc > 2) {
        count = argc - 2;
        for (int i = 0; i < count; i++) {
            references[i] = number(argv[i + 2], 0, 9999);
            if (references[i] < 0) goto invalid;
        }
    }
    for (int policy = 0; policy < 3; policy++) simulate(references, count, capacity, policy);
    return 0;
invalid:
    fprintf(stderr, "Usage: q7 [frames 1..10 [1..40 pages, each 0..9999]]\n");
    return 1;
}
