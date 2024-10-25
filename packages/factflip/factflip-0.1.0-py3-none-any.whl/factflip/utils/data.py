import logging
import os
import urllib
import zipfile
from pathlib import Path
from typing import List

import requests
from rdflib import Graph
from rich.progress import track

from factflip import DEFAULT_TEMPLATES_PATH


def load_rdf(rdf: Path, format="ttl") -> Graph:
    g = Graph()
    g.parse(rdf, format=format)

    return g


def load_imkg(imkg_full_dir: str) -> Graph:
    g = Graph()
    for subdir, _, files in os.walk(imkg_full_dir):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if ext in [".nt", ".ttl"]:
                print(os.path.join(subdir, file))
                g.parse(os.path.join(subdir, file), format=ext[1::])

    return g


def download_and_parse_imkg(
    imkg_url: str = "https://zenodo.org/records/7457166/files/imkg.1.0.data.zip?download=1",
) -> Graph:
    log = logging.getLogger()
    tmpf, _ = urllib.request.urlretrieve(imkg_url)
    with zipfile.ZipFile(tmpf) as zf:
        g = Graph()
        log.info("Parsing: full/imgflip.nt.")
        g.parse(zf.read("full/imgflip.nt"), format="nt")

        for file in zf.namelist():
            if file.startswith("full/"):
                ext = os.path.splitext(file)[-1].lower()
                if ext in [".nt", ".ttl"]:
                    if file != "full/imgflip.nt":
                        log.info(f"Parsing: {file}.")
                        g.parse(zf.read(file), format=ext[1::])

    urllib.request.urlcleanup()
    return g


def download_imgflip_templates_images(
    imgflip_template: List[int] = None,
    output_dir: Path = DEFAULT_TEMPLATES_PATH,
    force_download: bool = False,
):
    if imgflip_template is None:
        imgflip_template = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"  # noqa E501
    }
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for tmpl in track(imgflip_template, description="Downloading image templates..."):
        tmpl_name = tmpl.split("/")[-1]
        imgf = os.path.join(output_dir, f"{tmpl_name}.jpg")
        url = f"https://imgflip.com/s/meme/{tmpl_name}.jpg"

        if not os.path.isfile(imgf) or force_download:
            response = requests.get(url, stream=True, headers=headers)
            with open(imgf, "bw") as file:
                file.write(response.content)
