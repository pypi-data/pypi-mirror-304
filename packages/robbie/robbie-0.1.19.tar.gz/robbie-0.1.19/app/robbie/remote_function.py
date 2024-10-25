import sys
from functools import wraps
import argparse
import os
from positron_common.cli_args import args as cli_args
from positron_common.config import PositronJob, parse_job_config, merge_config
from positron_common.deployment.deploy import Deploy
from positron_common.deployment.stored_function import StoredFunction
from positron_common.user_config import user_config
from positron_common.cli.console import console
from positron_common.cli.logging_config import logger, set_log_level
from positron_common.enums import JobRunType

def remote(**parameters):

    # Parse command line arguments
    parser = argparse.ArgumentParser(description = "A decorator to handle deploying running your function in the cloud")
    parser.add_argument('--tail', action='store_true', help='Stream the stdout from Positron Cloud back to your cli', dest='stream_stdout', default=False)
    parser.add_argument('--loglevel', help='Set the logging level [CRITICAL,FATAL,ERROR, WARNING, INFO, DEBUG, NOTSET]', dest='loglevel')
    parser.add_argument('--create-only', action='store_true', help='Create the job but do not run it.', dest='create_only')
    parser.add_argument('--results-from-job-id', help='Fetch results and return from decorated function.', dest='results_from_job_id')
    positron_args, job_args = parser.parse_known_args()

    set_log_level(positron_args.loglevel)

    # Jupyter Support - Default out the cli_args to run remote always with no prompting
    if not cli_args.is_init:
        cli_args.init(
            local=False,
            deploy=True,
            stream_stdout=positron_args.stream_stdout,
            job_args=job_args,
            create_only=positron_args.create_only,
            results_from_job_id=positron_args.results_from_job_id,
            skip_prompts=True,
        )

    # enable  and tail function parameters but remove them before passing to PositronJob config    
    if "loglevel" in parameters:
        del parameters["loglevel"]
    if "tail" in parameters:
        cli_args.stream_stdout = parameters["tail"]
        del parameters["tail"]
    if "create_only" in parameters:
        cli_args.create_only = parameters["create_only"]
        del parameters["create_only"]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug("Running decorator")

            # Check this first to ensure we don't deploy
            if os.getenv('POSITRON_CLOUD_ENVIRONMENT', False):
                logger.debug("Running function locally")
                return func(*args, **kwargs)

            if cli_args.results_from_job_id:
                stored_function = StoredFunction(func, args, kwargs)
                stored_function.set_job_id(cli_args.results_from_job_id)
                secret_key = user_config.user_auth_token if user_config.user_auth_token else ""
                stored_function.load_and_validate_results(hmac_key=secret_key)
                return stored_function.result

            console.print("Robbie's deploying your function!", style="bold")
                # get decorator parameters
            job_config_decorator = PositronJob(**parameters)
            job_config = job_config_decorator
            job_config.job_type = JobRunType.REMOTE_FUNCTION_CALL

            # use job yaml as base if it exists
            job_config_yaml = parse_job_config()
            if job_config_yaml:
                job_config = merge_config(job_config_yaml, job_config_decorator)
                logger.debug("Processed configuration file")

            if job_config.commands:
                console.print("[red]Error: The 'commands' configuration in job_config.yaml is not supported in the remote decorator.\nPlease remove it or run with 'robbie run' to use 'commands'.[/red]")
                sys.exit(1)

            return Deploy.remote_function_deploy(func, args, kwargs, job_config)

        return wrapper
    return decorator