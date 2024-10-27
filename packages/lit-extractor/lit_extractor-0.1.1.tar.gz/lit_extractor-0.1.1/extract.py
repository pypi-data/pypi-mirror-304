import click
from tqdm import tqdm
import fanficfare
import os
import sys
import time
import subprocess


def extract_urls_from_file(filename):
    data_from_file = filename.readlines()
    data_from_file = [url.strip() for url in data_from_file]
    return data_from_file


def fff_url_extractor(url):
    try:
        print(f"Processing {url}")
        result = subprocess.run(['fanficfare', '-l', url], capture_output=True, text=True, check=True)
        metadata = result.stdout
        return metadata
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {url}: {e}")
        return ""


def download_url_from_file(file):
    try:
        print(f"Downloading from {file}")
        result = subprocess.Popen(['fanficfare', '-o', "is_adult=true", '-i', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with tqdm(total=100, desc="Downloading", ncols=100) as progress_bar:
            while result.poll() is None:  # While subprocess is running
                time.sleep(0.5)  # Small delay to slow down the loop
                progress_bar.update(1)  # Simulate progress with small increments
                if progress_bar.n >= progress_bar.total:
                    progress_bar.n = 0  # Reset bar if it reaches max (optional)
        # Update bar to full on completion
            progress_bar.n = 100
            progress_bar.refresh()

    # Get the subprocess output
        stdout, stderr = result.communicate()
        if result.returncode == 0:
            print("Download completed successfully.")
        else:
            print("Download failed.")
            print(stderr.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        print(f"Error downloading from{file}: {e}")
        return ""


def prettify_url(url):
    url_list = url.strip().split('\n')
    return url_list


def save_to_file(file_name=None, file_data=None):
    name = file_name if file_name else "extracted_list.txt"
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, name)
    try:
        with open(file_path, 'a') as f:
            if file_data is not None:
                for line in file_data:
                    f.write(f"{line}\n")
            print(f"Data has been saved to {file_path}")
    except IOError as e:
        print(f"Error writing to {file_path}: {e}")
        return

    return file_path


@click.group()
def extract():
    pass


@extract.command()
@click.argument('file', type=click.File('r'))
@click.option("--o", default=None, help="Output file name where the extracted list is to be stored")
@click.option("--d", default=False, help="flag to download all the books in the url")
def url(file, o, d):
    original_url_list = extract_urls_from_file(file)
    extracted_url = []
    for item in original_url_list:
        result = fff_url_extractor(item)
        processed_result = prettify_url(result)
        extracted_url.extend(processed_result)

    print(f"All the urls in the file {file.name} has been processed")
    filename = save_to_file(o, extracted_url)
    if d:
        download_url_from_file(filename)


@extract.command()
@click.argument('file', type=click.Path())
def download(file):
    download_url_from_file(file)


if __name__ == '__main__':
    url()
