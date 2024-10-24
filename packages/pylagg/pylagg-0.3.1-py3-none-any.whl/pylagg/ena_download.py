from ftplib import FTP
import requests
import os
from typing import List, Optional

import rich.progress as prog
from rich.progress import Progress

PROGBAR_COLUMNS = (
    prog.SpinnerColumn(),
    prog.TextColumn("[progress.description]{task.description}"),
    prog.BarColumn(),
    prog.DownloadColumn(),
    prog.TaskProgressColumn(),
    prog.TimeElapsedColumn(),
)

def quit_connection(message: Optional[str], ftp: FTP):
    # quit() can throw an exception if ftp server responds with error
    try:
        ftp.quit()
        if message is not None:
            raise Exception(f"ERROR: {message}")
    except Exception as e:
        ftp.close()
        # This is more like a log message, just something to know that the ftp QUIT command failed.
        # This is not a critical error, so we can just close the connection with ftp.close().
        raise Exception("ERROR: ftp quit command failed, trying to close the connection with ftp.close()", e)


def get_accessions_from_config(config: dict) -> List[str]:
    '''
    Reads a dictionary of the config and returns a list of accession numbers from the 'download_args' section.
    '''    
    if 'download_args' not in config:
        raise Exception("ERROR: No 'download_args' section found in the config file.")

    arguments: dict = config['download_args']
    keys = list(arguments.keys())

    accessions = []
    
    for key in keys:
        if key == 'list_of_accessions':
            accessions_arg = arguments['list_of_accessions']

            if not isinstance(accessions_arg, list):
                raise Exception("ERROR: Value for key 'list_of_accessions' in config file must be a list of strings.")
        
            if not all(isinstance(item, str) for item in accessions_arg):       
                raise Exception("ERROR: Value for key 'list_of_accessions' in config file must be a list of strings.")
            
            for accession in accessions_arg:
                if accession[:3] == "PRJ":
                    accessions.extend(get_project_accessions(accession))
                else:
                    accessions.append(accession)

    if accessions == []:
        raise Exception("ERROR: No accessions found in the config file.")
    
    return accessions


def get_project_accessions(prj_accession: str):
    url = f"https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=study_accession={prj_accession}&fields=run_accession"

    response = requests.get(url)

    content = response.content.decode()
    lines = content.splitlines()[1:] # ignore the header line
    return [line.split("\t")[0] for line in lines] # get the first value in a line (the accession)


# TODO: can possibly get rid of the output_dir parameter, but its fine for now
def ena_download(accession: str, output_dir: str = None) -> List[str]: 

    # small argument validations for the sra_accession parameter
    if (not accession.isalnum()):
        raise Exception(f"ERROR: Invalid SRA accession number {accession}. Please provide a valid SRA accession number.")

    ftp = FTP('ftp.sra.ebi.ac.uk')
    ftp.login()

    prefix = accession[:6]
    suffix = accession[6:]

    directory = f'/vol1/fastq/{prefix}/'

    # handles different format of directory for accession numbers
    match len(suffix):
        case 3:
            directory += f'{accession}'
        case 4:
            directory += f"00{suffix[-1]}/{accession}"
        case 5:
            directory += f"0{suffix[-2:]}/{accession}"
        case _:
            raise Exception("Error creating download directory: Accession length is incorrect.")

    try:
        ftp.cwd(directory)
    except Exception:
        quit_connection(f"Failed to access the directory for the provided accession number of {accession}.\n"
                 "Please ensure that the accession number is correct and the corresponding\n"
                 "FASTQ files are available on ENA.", ftp)

    file_names = ftp.nlst()
    if (file_names == []):
        quit_connection(f"No files found for the given SRA accession number of {accession}.", ftp)
    
    if (output_dir is not None):
        if not os.path.exists(output_dir):
            quit_connection("Output directory given for ENA downloading results does not exist.", ftp)

    output_files = []

    with Progress(*PROGBAR_COLUMNS) as progress:
        for file_name in file_names:
            size = ftp.size(f"{file_name}")
            task = progress.add_task(f"Downloading {file_name}", total=size)
            
            # build local file path
            if (output_dir is not None):
                local_file_path = os.path.join(output_dir, file_name)
            else:
                local_file_path = file_name

            output_files.append(local_file_path)
            
            # skip download if the entire file already exists
            if os.path.isfile(local_file_path) and os.path.getsize(local_file_path) == size:
                progress.update(task, advance=size)
                continue

            # Use for later if we want to implement downloads with retries 

            #       if (download_with_retries(ftp, file_name, local_file_path, 3, 2)):
            #           print(f"Downloaded {file_name} successfully!")
            #       else:
            #           print(f"Failed to download {file_name}.")

            with open(local_file_path, 'wb') as f:

                def callback(data):
                    f.write(data)
                    progress.update(task, advance=len(data))

                ftp.retrbinary(f"RETR {file_name}", callback)

    quit_connection(None, ftp)
    return output_files