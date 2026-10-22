#ifndef TAGGER_WRAPPER_H
#define TAGGER_WRAPPER_H 1

#include <stdio.h>
#include <errno.h>
#include <stdexcept>
#include "crfsuite_api.hpp"
#ifdef _WIN32
#include <io.h>
#else
#include <unistd.h>
#endif


namespace CRFSuiteWrapper
{

/**
* A wrapper around CRFSuite::Tagger that allows to call 'dump' method
* from Python.
*/
class Tagger : public CRFSuite::Tagger
{
public:
    void dump(int fileno)
    {
        if (model == NULL) {
            throw std::runtime_error("Tagger is closed");
        }

        // Python owns fileno; closing it here would race with descriptor reuse
        // in other threads before Python's finally block closes it again.
        int fd = dup(fileno);
        if (fd == -1) {
            throw std::runtime_error("Can't duplicate file descriptor");
        }
        FILE* file = fdopen(fd, "w");
        if (!file){
            ::close(fd);
            throw std::runtime_error("Can't open file");
        }

        model->dump(model, file);

        if (fclose(file)){
            throw std::runtime_error("Can't close file");
        };
    }
};

}
#endif
