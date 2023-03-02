#ifndef OPTIONS_H_INCLUDED
#define OPTIONS_H_INCLUDED
#include <stdbool.h>
#include <getopt.h>
#include <errno.h>
#include <string.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

  extern int e;
  extern long long nbytes;
  extern bool valid;
  extern char *inputArg;
  extern char *outputArg;
  extern bool useRdrand;
  extern bool useMrand;
  extern bool useFile;
  extern bool useStdio;

void
options (int argc, char **argv);

#endif
