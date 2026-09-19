# C Programming and Operating Systems Exercises

Small programs by Elliott Barnes covering integer processing, process identifiers, POSIX threads, synchronization, pipes, address translation, and page-replacement algorithms.

Source and Makefiles are grouped by their original assignment number. Assignment prompts, written answer sheets, and compiled binaries are excluded.

## Building

The exercises are independent programs rather than one application. Some use POSIX threads, semaphores, or Unix headers and therefore target a Unix-like environment. Use a directory's Makefile where present, or compile an individual source with an appropriate C compiler; threaded programs may require `-pthread`.

Modern Clang syntax checks passed for 8 of the 11 C files. Historical exercises `Assignment2/q4.c`, `Assignment6/Q1.c`, and `Assignment6/Q2.c` retain compile errors or incompatible declarations and are included as incomplete archival work. See each source file for its entry point and assumptions.
