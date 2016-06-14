
from tests.util.pipe import Pipe
from threading import Thread

from pycell.repl import repl

from tests.util.system_test import system_test
from tests.util.all_examples import all_sessions

def _validate_session(f):
    strin = Pipe()
    strout = Pipe()
    strerr = Pipe()
    replthread = Thread(target=repl, args=(strin, strout, strerr))
    replthread.start()
    for exp_line in f:
        expprompt = exp_line[:4]
        if expprompt in (">>> ", "... "):
            prompt = strout.read(4)
            if prompt != exp_line[:4]:
                raise Exception(
                    "Prompt was '%s' but we expected '%s'." % (
                prompt, exp_line[:4]))
            strin.write(exp_line[4:])
        else:
            output = strout.readline()
            if output != exp_line:
                raise Exception("Output was '%s' but we expected '%s'" % (
                output, exp_line))

    strerr.close()
    strout.close()
    strin.close()
    replthread.join()


@system_test
def All_example_repl_sessions_are_correct():
    from pycell.chars_in_file import chars_in_file
    for example in all_sessions():
        with open(example, encoding="ascii") as f:
            _validate_session(f)
