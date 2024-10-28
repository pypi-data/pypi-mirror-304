import click
from click import prompt

from helper.helper import *

@click.group()
def extract():
    pass


@extract.command()
@click.argument('file', type=click.File('r'))
@click.option("-o","--output", default='extracted_list',show_default=True, help="Output file name where the extracted list is to be stored")
@click.option("-d", "--download", is_flag=True,default=False,show_default=True, help="flag to download all the books in the url")
def url(file, output, download):
    original_url_list = extract_urls_from_file(file)
    extracted_url = []
    for item in original_url_list:
        result = fff_url_extractor(item)
        processed_result = prettify_url(result)
        extracted_url.extend(processed_result)

    console.print(f"All the urls in the file [cyan]{file.name}[/] has been processed", style="bold green")
    filename = save_to_file(output, extracted_url)
    if download:
        download_url_from_file(filename)


@extract.command()
@click.argument('file', type=click.Path())
def download(file):
    download_url_from_file(file)


if __name__ == '__main__':
    url()
