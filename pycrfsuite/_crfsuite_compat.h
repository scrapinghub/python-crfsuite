#ifndef PYCRFSUITE_COMPAT_H
#define PYCRFSUITE_COMPAT_H

#ifndef __cplusplus
#include <stdlib.h>
int pycrfsuite_rand(void);
#define rand pycrfsuite_rand
#endif

#endif
