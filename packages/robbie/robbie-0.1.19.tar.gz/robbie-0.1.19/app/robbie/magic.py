import os
import threading
import select
import dill
import subprocess
import shutil
from IPython.core.magic import (Magics, magics_class, cell_magic)

LOCAL_PICKLE = 'cell.pkl'
REMOTE_PICKLE = 'cell_result.pkl'
REQUIREMENTS_FILE = 'cell_requirements.txt'
PYTHON_CELL_OUTPUT = 'cell_output.py'
JOB_RESULTS = 'job-execution'

# Registers this class name as a magic definition with ipython.
# Run with %%robbie
@magics_class
class robbie_magic(Magics):
    @cell_magic
    def robbie(self, _, cell):
        # Ensure dill is installed and save the current session to a pickle file
        dill.dump_session(LOCAL_PICKLE)

        # get deps and ensure we'll install them.
        pip_freeze = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # in testing we're usually using a test version of robbie so we need to remove it from the requirements since
        # it fail install on the remote machine.
        requirements_str = remove_line(pip_freeze.stdout, 'robbie')
        with open(REQUIREMENTS_FILE, 'w') as f:
            f.write(requirements_str)

        # create a file that wraps the cell and loads the pickle file
        python_cell_output = open(PYTHON_CELL_OUTPUT, "w")
        python_cell_output.write("import dill\n")
        python_cell_output.write(f"dill.load_session('{LOCAL_PICKLE}')\n")
        python_cell_output.write(cell)
        python_cell_output.write(f"dill.dump_session('{REMOTE_PICKLE}')\n")
        python_cell_output.flush()
        python_cell_output.close()

        # Create a job on the fly and run the cell file in robbie
        p = subprocess.Popen(
          f'robbie run --download --tail --y "pip install -r {REQUIREMENTS_FILE} && python {PYTHON_CELL_OUTPUT} && rm -rf venv"',
          text=True,
          shell=True,
          stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # wait for the job to finish and print the output
        log_stop_event = threading.Event()
        stdout_thread = threading.Thread(target=logging_thread, args=(p.stdout, "stdout", log_stop_event)); stdout_thread.start()
        stderr_thread = threading.Thread(target=logging_thread, args=(p.stderr, "stderr", log_stop_event)); stderr_thread.start()
        p.wait()
        log_stop_event.set()
        stdout_thread.join()
        stderr_thread.join()

        # Job results should come back as a pkl file. We load the results back into the ipython environment
        try:
          dill.load_session(f'./{JOB_RESULTS}/{REMOTE_PICKLE}')
        except Exception as e:
          pass

        # Clean up env
        rm(PYTHON_CELL_OUTPUT)
        rm(LOCAL_PICKLE)
        rm(REMOTE_PICKLE)
        rm(REQUIREMENTS_FILE)
        rmdir(JOB_RESULTS)


def remove_line(multiline_str, match) -> str:
    lines = multiline_str.splitlines()  # Split into lines
    filtered_lines = [line for line in lines if match not in line]  # Filter lines
    return "\n".join(filtered_lines)  # Join the remaining lines

def rmdir(dirname):
    try:
        shutil.rmtree(dirname)
    except FileNotFoundError:
        pass

def rm(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
 
def logging_thread(pipe, stream_name: str, stop_event: threading.Event):
    try:
        with pipe:
            while not stop_event.is_set():
                # Calling pipe.readline() will hang the process until a new line is available
                # however, if no new lines are available, we want to check if the thread should stop
                ready, _, _ = select.select([pipe], [], [], 0.1)
                if ready:
                    # TODO: Can I iterate over the pipe and process everything that's ready?
                    line = pipe.readline()
                    if not line:
                        break
                    if line.strip():
                        if stream_name == "stdout":
                            print(line.rstrip())
                        else:
                            print("ERROR: " + line.rstrip())
                else:
                    stop_event.wait(1)

            # Read one last time.
            ready, _, _ = select.select([pipe], [], [], 0.1)
            if ready:
                for line in pipe:
                    if line.strip():
                        if stream_name == "stdout":
                            print(line.rstrip())
                        else:
                            print("ERROR: " + line.rstrip())
            # TODO: Do we need to check one more time for outstanding data in the pipe?
            # logger.debug(f'Logging thread for: {stream_name} stopped')
    except Exception as e:
        print(f'Logging thread for: {stream_name} stopped with exception: {e}')


# Loads the magic class into the runtime ipython environment.
# Load with %load_ext robbie.magic
def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # You can register the class itself without instantiating it.  IPython will
    # call the default constructor on it.
    ipython.register_magics(robbie_magic)
