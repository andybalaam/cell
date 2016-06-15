
from tests.util.pipe import Pipe
from threading import Thread

from pycell.repl import repl

from tests.util.system_test import system_test
from tests.util.all_examples import all_sessions


def _validate_line(exp_line, strin, strout, strerr):
    expprompt = exp_line[:3]
    if expprompt in (">>>", "..."):
        prompt = strout.read(4)
        if prompt != exp_line[:4]:
            raise Exception(
                "Prompt was '%s' but we expected '%s'." % (
                    prompt, exp_line[:4])
            )
        strin.write(exp_line[4:])
    else:
        output = strout.readline()
        if output != exp_line:
            raise Exception("Output was '%s' but we expected '%s'" % (
                output, exp_line)
            )


def _validate_session(f):
    with Pipe() as strin, Pipe() as strout:
        replthread = Thread(target=repl, args=(strin, strout, strout))
        replthread.start()
        for exp_line in f:
            _validate_line(exp_line, strin, strout, strout)

    replthread.join()


@system_test
def All_example_repl_sessions_are_correct():
    for example in all_sessions():
        with open(example, encoding="ascii") as f:
            _validate_session(f)
