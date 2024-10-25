import os
import shutil
import requests
import tarfile
import typer
from typing_extensions import Annotated
from typing import Optional
from tqdm.autonotebook import tqdm
from positron_common.job_api.list_jobs import list_jobs
from positron_common.job_api.get_job import get_job
from positron_common.aws.s3_presigned_handler import S3PresignedHandler
from positron_common.cli.console import console
from positron_common.exceptions import RobbieException
from positron_common.cli.console import console, ROBBIE_BLUE, SPINNER
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich.tree import Tree
from positron_common.cli.console import console
from positron_common.cli.logging_config import logger


def download(
    filename: Annotated[Optional[str], typer.Argument(help='Download a results <file> to your local machine. Specify "all" for the complete list.')] = None,
) -> None:
    """
        Download command for Robbie CLI ("robbie download) allows users to download result.tar.gz from a job.
        
        Prompts the user to choose a job to download results from.
    """
    if not download_argument_is_valid(filename):
        console.print('[red]Error: Please specify a valid file name or "all" to download all files.')
        return
    
    jobs = Jobs.load()
    jobs_choice = prompt('Choose a job to download: <tab for menu>: ', completer=WordCompleter(jobs.menu_items()))
    if jobs_choice == "" or jobs_choice == None:
        console.print("No job selected. Try again.")
    if not jobs_choice in jobs.menu_items():
        valid_job_selected = True
        console.print("Invalid job selected. Try again.")
    else:
        download_chosen_results(jobs.id_from_menu_item(jobs_choice), filename)
    
def download_argument_is_valid(filename: str) -> bool:
    """Check if the download argument is valid."""
    if filename == None:
        return False
    if filename == "all":
        return True
    if filename == "":
        return False
    return True

def download_chosen_results(job_id: str, filename: str):
    """The user can download a single file or all files from the job."""
    if filename == "all":
        download_tar_results_file(job_id)
    elif filename == None or filename == "":
        raise RobbieException(f"Nothing to download job {job_id}")
    else:
        download_individual_results_file(job_id, filename)

def download_tar_results_file(job_id: str):
    """
    Download the result.tar.gz file from the job and stores it in the CWD

    Raises:
        RobbieException: If we can't generate a presigned URL or downloading fails
    """
    job = get_job(job_id)

    if(job["resultsPresignedBucketInfo"] == None):
        raise RobbieException(f"No resultsPresignedBucketInfo for job {job_id}")

    print("resultsPresignedBucketInfo", job["resultsPresignedBucketInfo"])

    logger.debug(f'Downloading results for: {job["name"]}')

    response = requests.get(job["resultsPresignedBucketInfo"],stream=True) 
    if response.status_code != 200:
        logger.debug(f'Failed to download URL, http code: {response.status_code} \n {response.text}')
        raise RobbieException('Sorry, run has no results to download.') 
    else:
        # Sizes in bytes.
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024

        console.print(f'Download results for: {job["name"]}')
        with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            with open("./result.tar.gz", "wb") as file:
                logger.debug(f'Successfull opened ./result.tar.gz')
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)

        if total_size != 0 and progress_bar.n != total_size:
            raise RobbieException(f'failed to download file')
    
        if os.path.exists("./job-execution") and os.path.isdir("./job-execution"):
            console.print("[green]✔[/green] Removed old job-execution directory.")
            shutil.rmtree("./job-execution")

        _decompress(tar_file="./result.tar.gz", path=".")
        # get rid of it
        os.remove("./result.tar.gz") 
        console.print("[green]✔[/green] Results now available.")


def download_individual_results_file(job_id: str, file_name: str):
    """
    Download a single file from the job and stores it in the CWD

    Raises:
        RobbieException: If we can't generate a presigned URL or downloading fails
    """
    
    file_url = S3PresignedHandler._get_download_presigned_url(job_id, f"result/{file_name}")
    if(file_url == None):
        raise RobbieException(f"No such file: {file_name} for job {job_id}")

    print("file_url", file_url)
    logger.debug(f"Downloading file: {file_name} for job {job_id}")

    # _get_download_presigned_url returns a dict with a 'url' key
    response = requests.get(file_url['url'], stream=True) 
    if response.status_code != 200:
        logger.debug(f'Failed to download URL, http code: {response.status_code} \n {response.text}')
        raise RobbieException('Sorry, run has no results to download.') 
    else:
        # Sizes in bytes.
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024

        console.print(f"Downloading file: {file_name} for job {job_id}")
        with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            with open(f"./{file_name}", "wb") as file:
                logger.debug(f'Successfull opened ./{file_name}')
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)

        if total_size != 0 and progress_bar.n != total_size:
            raise RobbieException(f'failed to download file')
    
        console.print("[green]✔[/green] File downloaded successfully.")

def _decompress(tar_file, path):
    """
    Extracts `tar_file` and puts the `members` to `path`.
    If members is None, all members on `tar_file` will be extracted.
    """
    tree = Tree("Remote files copied to Local Machine")

    tar = tarfile.open(tar_file, mode="r:gz")
    for member in tar.getmembers():
        logger.debug(f'Extracting {member.name}')
        tar.extract(member, path=path)
        tree.add(f"[yellow]{member.name}, size: {member.size} bytes[/yellow]")
    console.print(tree)
    tar.close()

# Naming
JOB_ID="id"
JOB_NAME="name"
JOB_MENU="menu"

# singleton builds a list of tuples from the DB results
class Jobs: 
    is_init: bool = False
    my_jobs: dict

    def __init__(self, jobs_arg: dict):
        if self.is_init:
            raise ValueError('Jobs.load() already initialized')
        else:
            self.init = True
            self.my_jobs= jobs_arg

    @staticmethod
    def load():
        jobs = list_jobs()
        if len(jobs) == 0:
            return None
        # Loop through and add a custom "menu" item to each dict (but only if the job actually ran)
        for key, val in jobs.items(): 
            if val["durationMs"] != None:
                val[JOB_MENU] = f'{val[JOB_NAME]} (uuid: {val[JOB_ID]} )'
        return Jobs(jobs)
        
    # Prompt toolkit needs a list of strings to display in the menu 
    def menu_items(self) -> list: 
        ret_list: list = []
        for key, val in self.my_jobs.items():
            # just show names
            if val["durationMs"] != None:
                ret_list.append(val[JOB_MENU])
        return ret_list
    
    def id_from_menu_item(self, menu_item: str) -> str:
        for key, val in self.my_jobs.items():
            if val["durationMs"] != None and val[JOB_MENU] == menu_item:
                return val[JOB_ID]
        return None