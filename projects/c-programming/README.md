# C Programming and Operating Systems Exercises

Small programs by Elliott Barnes covering integer processing, process identifiers, POSIX threads, synchronization, pipes, address translation, and page-replacement algorithms.

Source and Makefiles are grouped by their original assignment number. Assignment prompts, written answer sheets, and compiled binaries are excluded.

## Building

The exercises are independent programs rather than one application. Some use POSIX threads, semaphores, or Unix headers and therefore target a Unix-like environment. Use a directory's Makefile where present, or compile an individual source with an appropriate C compiler; threaded programs may require `-pthread`.

Modern Clang syntax checks passed for 8 of the 11 C files. Historical exercises `Assignment2/q4.c`, `Assignment6/Q1.c`, and `Assignment6/Q2.c` retain compile errors or incompatible declarations and are included as incomplete archival work. See each source file for its entry point and assumptions.

## Completed memory examples

[Memory Lab](https://elliottbarnes.github.io/school-projects/) provides browser counterparts to Assignments 7 and 8. Both native programs now accept validated command-line inputs:

```sh
cc -std=c11 -Wall -Wextra -Werror Assignment7/addresses.c -o /tmp/addresses
/tmp/addresses 4294967295
cc -std=c11 -Wall -Wextra -Werror Assignment8/q7.c -o /tmp/pages
/tmp/pages 3 7 0 1 2 0 3 0 4 2 3 0 3 2
```

Address translation accepts unsigned decimal 32-bit addresses and uses 4096-byte pages. Page replacement accepts 1–10 frames and 1–40 page references (each 0–9999); with no arguments it runs a fixed 20-reference example with three frames. FIFO, LRU, and OPT print each frame trace and final fault count. Ties choose the first frame. OPT requires future references and serves as a comparison bound, not an online policy.

The 2026 completion replaces unsafe `atoi`/unchecked frame counts and fixes LRU's previously uninitialized victim index. These two exercises are actively checked; the incomplete archival exercises listed above are unchanged.
