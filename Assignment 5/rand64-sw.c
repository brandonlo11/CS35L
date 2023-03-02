#include "rand64-sw.h"
#include <stdlib.h>

/* Software implementation.  */

FILE *urandstream;
char *fileStream;

/* Initialize the software rand64 implementation.  */
void
software_rand64_init (void)
{
  if (!fileStream)
    fileStream = "/dev/random";
  urandstream = fopen (fileStream, "r");
  if (! urandstream)
    abort ();
}

/* Return a random value, using software operations.  */
unsigned long long
software_rand64 (void)
{
  unsigned long long int x;
  if (fread (&x, sizeof x, 1, urandstream) != 1)
    abort ();
  return x;
}

/* Changes urandstream if reading from a file */
void
reassignFile(char *file)
{
  fileStream = file;
}

/* Finalize the software rand64 implementation.  */
void
software_rand64_fini (void)
{
  fclose (urandstream);
}
