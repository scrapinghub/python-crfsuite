#include <iostream>
#include "Python.h"
#include "trainer_wrapper.hpp"

namespace CRFSuiteWrapper
{


void Trainer::set_handler(PyObject *obj, messagefunc handler)
{
    if (this->m_obj != NULL){
        Py_XDECREF(this->m_obj);
    }
    this->m_obj = obj;
    Py_XINCREF(this->m_obj);

    this->handler = handler;
}


Trainer::~Trainer()
{
    if (this->m_obj != NULL){
        Py_XDECREF(this->m_obj);
    }
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
