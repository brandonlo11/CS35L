#include "options.h"

  int x;
  long long nbytes;
  bool valid = false;
  char *inputArg;
  char *outputArg;
  bool useRdrand = true;
  bool useMrand = false;
  bool useFile = false;
  bool useStdio = true;

void
options (int argc, char **argv){
    while ((x = getopt(argc, argv, ":i:o:")) != -1) {
        switch(x) {
        case 'i':
	    if (optarg[0]=='/') {
	      useFile = true;
	      useRdrand = false;
	    }
	    else if (strcmp("mrand48_r", optarg) == 0) {
              useRdrand = false;
              useMrand = true;
            }
	    else if (strcmp("rdrand", optarg) != 0) {
               return;
	    }
	    inputArg = optarg;
	    break;
        case 'o':
	    if (isdigit(*optarg)) {
               useStdio = false;
            }
	    else if (strcmp("stdio", optarg) != 0) {
                return;
            }
            outputArg = optarg;
            break;
        case ':':
            return;
        case '?':
	    return;
        }
    }
  if (optind == (argc - 1)){
	  char *endptr;
	  errno = 0;
	  nbytes = strtoll(argv[optind], &endptr, 10);
	  if (errno)
		  perror (argv[optind]);
	  valid = !*endptr && 0 <= nbytes;
  }
}
