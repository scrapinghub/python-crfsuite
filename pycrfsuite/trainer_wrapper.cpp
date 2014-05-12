#include <iostream>
#include "Python.h"
#include "trainer_wrapper.hpp"

namespace CRFSuiteWrapper
{


void Trainer::set_handler(PyObject *obj, messagefunc handler)
{
    // don't hold a reference to obj here because it prevents
    // destructor from being called
    this->m_obj = obj;
    this->handler = handler;
}


void Trainer::message(const std::string& msg)
{
    if (this->m_obj == NULL) {
        std::cerr << "** Trainer invalid state: obj [" << this->m_obj << "]\n";
        return;
    }
    handler(this->m_obj, msg);
}

void Trainer::_init_hack()
{
    Trainer::init();
}


}
