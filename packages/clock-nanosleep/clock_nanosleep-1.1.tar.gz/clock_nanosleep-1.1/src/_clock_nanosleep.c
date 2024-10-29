#include "Python.h"

#include <time.h>

#if !defined(CLOCK_MONOTONIC) || !defined(TIMER_ABSTIME)
    #error "clock_nanosleep() function is not available"
#endif

#define SEC_TO_NS (1000*1000*1000)

inline static int
_a_LE_b(const struct timespec *a, const struct timespec *b)
{
    if (a->tv_sec < b->tv_sec ||
        (a->tv_sec  == b->tv_sec &&
         a->tv_nsec <= b->tv_nsec)) {
        return 1;
    }
    return 0;
}

inline static int
_get_monotonic(struct timespec *ts)
{
    if (clock_gettime(CLOCK_MONOTONIC, ts) == 0) {
        return 0;
    } else {
        PyErr_SetFromErrno(PyExc_OSError);
        return -1;
    }
}

static PyObject *
_sleep(PyObject *module, PyObject *obj)
{
    struct timespec monotonic, deadline;

    /* get monotonic */
    if (_get_monotonic(&monotonic)) {
        return NULL;
    }

    /* get seconds from arg, and calculate deadline. */
    if (PyFloat_Check(obj)) {
        int64_t nsec;
        double d = PyFloat_AsDouble(obj);

        if (isnan(d) || d < 0.0 || d >= (double)(INT64_MAX / SEC_TO_NS)) {
            goto secs_out_of_range;
        }
        nsec = (int64_t)(d * SEC_TO_NS);
        if (nsec == 0) {
            Py_RETURN_NONE;
        }

        /* calculate deadline */
        deadline.tv_sec  = monotonic.tv_sec  + (nsec / SEC_TO_NS);
        deadline.tv_nsec = monotonic.tv_nsec + (nsec % SEC_TO_NS);
        if (deadline.tv_nsec >= SEC_TO_NS) {
            deadline.tv_sec  += 1;
            deadline.tv_nsec -= SEC_TO_NS;
        }
    } else {
        int64_t sec = PyLong_AsLongLong(obj);
        if (sec < 0) {
            if (sec == -1 && PyErr_Occurred()) {
                PyErr_SetString(PyExc_ValueError,
                                "Can't covert secs to int64_t");
                return NULL;
            }
            goto secs_out_of_range;
        }
        if (sec == 0) {
            Py_RETURN_NONE;
        }

        /* calculate deadline */
        deadline.tv_sec  = monotonic.tv_sec + sec;
        deadline.tv_nsec = monotonic.tv_nsec;
    }

    /* check overflow */
    if (_a_LE_b(&deadline, &monotonic)) {
        /* deadline <= monotonic. in fact can't be equal. */
        goto secs_out_of_range;
    }

    /* sleep */
    while (1) {
        int ret;

        Py_BEGIN_ALLOW_THREADS
        ret = clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME,
                              &deadline, NULL);
        Py_END_ALLOW_THREADS

        /* success */
        if (ret == 0) {
            Py_RETURN_NONE;
        }

        if (ret != EINTR) {
            errno = ret;
            PyErr_SetFromErrno(PyExc_OSError);
            return NULL;
        }

        /* sleep was interrupted by SIGINT */
        if (PyErr_CheckSignals()) {
            return NULL;
        }

        /* check timeout */
        if (_get_monotonic(&monotonic)) {
            return NULL;
        }
        if (_a_LE_b(&deadline, &monotonic)) {
            /* deadline <= monotonic */
            Py_RETURN_NONE;
        }
    }

secs_out_of_range:
    PyErr_SetString(PyExc_ValueError,
                    "Secs is negative/overflow/out_of_range.");
    return NULL;
}

static PyMethodDef _clock_nanosleep_methods[] = {
    {"sleep", (PyCFunction)_sleep, METH_O, NULL},
    {0}
};

static PyModuleDef _clock_nanosleep_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "_clock_nanosleep",
    .m_size = 0,
    .m_methods = _clock_nanosleep_methods,
};

PyMODINIT_FUNC
PyInit__clock_nanosleep(void)
{
    return PyModule_Create(&_clock_nanosleep_module);
}
