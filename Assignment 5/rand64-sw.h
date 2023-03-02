#ifndef RAND64SW_H_INCLUDED
#define RAND64SW_H_INCLUDED
#include <stdio.h>

void
software_rand64_init (void);

unsigned long long
software_rand64 (void);

void
reassignFile(char *file);

void
software_rand64_fini (void);

#endif
