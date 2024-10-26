import os
import shutil
from pathlib import Path
from typing import Optional

import chromadb
import pandas as pd
import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.pretty import pprint
from typing_extensions import Annotated

import factflip
from factflip import DEFAULT_EMBEDDINGS_PATH, DEFAULT_ROOT_PATH
from factflip.generators import FactFlipMemeGenerator
from factflip.llms import OllamaLlm
from factflip.utils.build import (
    build_embeddings_database,
    describe_imkg_memes,
    generate_imkg_claims,
    merge_claims_data,
    query_imkg_memes,
)
from factflip.utils.data import (
    download_and_parse_imkg,
    download_factflip_embeddings,
    download_imgflip_templates_images,
    load_rdf,
)
from factflip.utils.memes import create_imgflip_meme
from factflip.validators import FactFlipMemeValidator

load_dotenv()
app = typer.Typer(no_args_is_help=True, add_completion=False)


def _version_callback(value: bool):
    if value:
        print(factflip.version)
        raise typer.Exit()


@app.callback()
def callback(
    version: Annotated[
        Optional[bool],
        typer.Option("--version", "-v", help="Show the installed factflip version.", callback=_version_callback),
    ] = None,
):
    """🖼️  Factflip - A claim-based meme generator powered by IMKG and LLMs."""


@app.command(help="Build the meme embedding database.")
def build(
    imkg_dir: Annotated[
        Path,
        typer.Option(
            ...,
            "--imkg-dir",
            "-imkg",
            envvar="IMKG_DIR",
            help="The path where IMGK is stored.",
        ),
    ] = DEFAULT_ROOT_PATH,
    embeddings_db: Annotated[
        Path,
        typer.Option(
            ...,
            "--embeddings-db",
            "-db",
            envvar="FACTFLIP_EMBEDDINGS",
            help="The path of the FactFlip database that contains the embeddings.",
        ),
    ] = DEFAULT_EMBEDDINGS_PATH,
    download_imkg: Annotated[
        bool,
        typer.Option(
            "--download-imkg",
            "-d",
            help="Download IMKG release (this will not use the already downloaded and parsed IMKG data).",
        ),
    ] = False,
):
    Path(imkg_dir).mkdir(parents=True, exist_ok=True)
    templates_dir = os.path.join(imkg_dir, "templates")
    imkgf = os.path.join(imkg_dir, "imkg_full.ttl")
    imkg_memes_f = os.path.join(imkg_dir, "imkg_memes.csv")
    imkg_memes_descriptions_f = os.path.join(imkg_dir, "imkg_memes_descriptions.csv")
    imkg_claims_f = os.path.join(imkg_dir, "imkg_claims.csv")
    merged_claims_f = os.path.join(imkg_dir, "merged_imkg_claims.csv")

    console = Console()
    with console.status("Building embedding data (this will take a very long time)...") as status:
        # 1) Download and parse IMKG into one Graph.
        g = None
        if download_imkg or not os.path.isfile(imkgf):
            status.update("Downloading and parsing IMKG (this will take a very long time)...")
            g = download_and_parse_imkg()

            status.update("Saving parsed IMKG knowledge graph (this will take a very long time)...")
            g.serialize(destination=imkgf)

            status.update(f"IMKG knowledge graph saved: {imkgf}.")

        # 2) Download IMKG images.
        if os.path.isfile(imkg_memes_f):
            imkg_memes_df = pd.read_csv(imkg_memes_f)
        else:
            if not download_imkg and not g:
                status.update(f"Loading IMKG: {imkgf}.")
                g = load_rdf(imkgf)
                status.update("IMKG loaded.")

            status.update("Querying template images...")
            imkg_memes_df = query_imkg_memes(g)
            imkg_memes_df.to_csv(imkg_memes_f, index=False)

            status.update(f"Template query data saved: {imkg_memes_f}")

            status.update("Downloading template images from ImgFlip...")
            download_imgflip_templates_images(
                imkg_memes_df.imgflip_template.unique(),
                output_dir=templates_dir,
            )
            status.update("Template images saved.")

        # 3) Create images meme descriptions:
        if os.path.isfile(imkg_memes_descriptions_f):
            imkg_memes_descriptions_df = pd.read_csv(imkg_memes_descriptions_f)
        else:
            status.update("Generating memes descriptions...")
            imkg_memes_descriptions_df = describe_imkg_memes(
                imkg_memes_df,
                imgflip_templates_dir=templates_dir,
            )
            imkg_memes_descriptions_df.to_csv(imkg_memes_descriptions_f, index=False)
            status.update(f"Memes description data saved: {imkg_memes_descriptions_f}")

        # 4) Generate claims for existing memes:
        if os.path.isfile(imkg_claims_f):
            imkg_claims_df = pd.read_csv(imkg_claims_f)
        else:
            status.update("Generating claims...")
            imkg_claims_df = generate_imkg_claims(
                imkg_memes_df=imkg_memes_df, imkg_memes_descriptions_df=imkg_memes_descriptions_df, llm=OllamaLlm()
            )
            imkg_claims_df.to_csv(imkg_claims_f, index=False)
            status.update(f"Claims data saved: {imkg_claims_f}")

        # 5) Create embeddings database:
        status.update("Bulding embeddings database...")
        merged_claims_df = merge_claims_data(imkg_memes_df, imkg_memes_descriptions_df, imkg_claims_df)

        merged_claims_df.to_csv(merged_claims_f, index=False)
        status.update(f"Merged claims data saved: {merged_claims_f}")

        build_embeddings_database(merged_claims_df, embeddings_db, delete_collection=False)
        status.update("Embeddings database created.")


@app.command(help="Download precomputed Factflip embeddings.")
def download(
    embeddings_db: Annotated[
        Path,
        typer.Option(
            ...,
            "--embeddings-db",
            "-db",
            envvar="FACTFLIP_EMBEDDINGS",
            help="The path of the FactFlip database that contains the embeddings.",
        ),
    ] = DEFAULT_EMBEDDINGS_PATH,
    force_download: Annotated[
        bool,
        typer.Option("--force-download", "-f", help="Force download if the database is already present."),
    ] = False,
):
    console = Console()
    with console.status("Downloading embedding data...") as status:
        if not os.path.isdir(embeddings_db) or force_download:
            zipfile = download_factflip_embeddings(embeddings_version=factflip.version)

            status.update("Extracting embedding data...")
            if os.path.isdir(embeddings_db):
                shutil.rmtree(embeddings_db)

            Path(embeddings_db).mkdir(parents=True, exist_ok=True)
            zipfile.extractall(embeddings_db)
            status.update("Embedding data installed.")
        else:
            status.update("Embedding data already installed.")


@app.command(help="Render a meme instance using the imgflip API.")
def render(
    imgflip_template_id: Annotated[
        int,
        typer.Option(
            ...,
            "--imgflip-template-id",
            "-i",
            help="The ImgFlip template ID used for generating the final image.",
        ),
    ],
    caption_1: Annotated[
        str,
        typer.Argument(help="The first caption that is used for rendering the meme image."),
    ],
    caption_2: Annotated[
        str,
        typer.Argument(help="The optional second caption that is used for rendering the meme image."),
    ] = None,
    download_render: Annotated[
        bool,
        typer.Option("--download-render", "-d", help="Download rendered meme using ImgFlip API."),
    ] = False,
    imgflip_username: Annotated[
        str,
        typer.Option(
            ...,
            "--imgflip-username",
            "-u",
            envvar="IMGFLIP_USERNAME",
            help="The ImgFlip API username used for generating the final image.",
        ),
    ] = None,
    imgflip_password: Annotated[
        str,
        typer.Option(
            ...,
            "--imgflip-password",
            "-p",
            envvar="IMGFLIP_PASSWORD",
            help="The ImgFlip API password used for generating the final image.",
        ),
    ] = None,
):
    generated = {
        "template_id": imgflip_template_id,
        "meme_caption": [caption_1, caption_2] if caption_2 else [caption_1],
    }

    console = Console()
    with console.status("Rendering meme...") as status:
        if imgflip_username and imgflip_password:
            status.update("Generating meme image using FactFlip API...")
            imgflipmeme = create_imgflip_meme(
                meme=generated,
                imgflip_username=imgflip_username,
                imgflip_password=imgflip_password,
            )

            img_filename = imgflipmeme.url.split("/")[-1]
            generated["meme_imgage_page_url"] = imgflipmeme.page_url
            generated["meme_imgage_url"] = imgflipmeme.url
            generated["meme_image_filename"] = img_filename

            console.log("Meme image generated.")

            if download_render:
                status.update("Downloading meme image.")
                imgflipmeme.save(img_filename)
                status.update(f"Meme image saved: {img_filename}")

    pprint(generated, expand_all=True)


@app.command(help="Generate the text of a meme.")
def generate(
    claim: Annotated[
        str,
        typer.Argument(help="The claim (misinformation) that is used for generating the meme."),
    ],
    review: Annotated[
        str,
        typer.Argument(help="The claim review (claim correction) that is used for generating the meme."),
    ],
    embeddings_db: Annotated[
        Path,
        typer.Option(
            ...,
            "--embeddings-db",
            "-db",
            envvar="FACTFLIP_EMBEDDINGS",
            help="The path of the FactFlip database that contains the embeddings.",
        ),
    ] = DEFAULT_EMBEDDINGS_PATH,
    render: Annotated[
        bool,
        typer.Option("--render", "-r", help="Render the generated meme using ImgFlip API."),
    ] = False,
    download_render: Annotated[
        bool,
        typer.Option("--download-render", "-d", help="Download rendered meme using ImgFlip API."),
    ] = False,
    imgflip_username: Annotated[
        str,
        typer.Option(
            ...,
            "--imgflip-username",
            "-u",
            envvar="IMGFLIP_USERNAME",
            help="The ImgFlip API username used for generating the final image.",
        ),
    ] = None,
    imgflip_password: Annotated[
        str,
        typer.Option(
            ...,
            "--imgflip-password",
            "-p",
            envvar="IMGFLIP_PASSWORD",
            help="The ImgFlip API password used for generating the final image.",
        ),
    ] = None,
):
    console = Console()
    with console.status("Generating meme...") as status:
        status.update("Loading embeddings...")
        client = chromadb.PersistentClient(path=embeddings_db.absolute().as_posix())
        collection = client.get_or_create_collection("claims")
        console.log("Embeddings database loaded.")

        status.update("Loading language model...")
        generator = FactFlipMemeGenerator(embeddings=collection)
        console.log("Language model loaded.")

        status.update("Generating meme content...")
        generated = generator.generate_meme_text(claim, review, validator=FactFlipMemeValidator(max_retries=5))
        console.log("Meme content generated.")

        if (render or download_render) and imgflip_username and imgflip_password:
            status.update("Generating meme image using FactFlip API...")
            imgflipmeme = create_imgflip_meme(
                meme=generated,
                imgflip_username=imgflip_username,
                imgflip_password=imgflip_password,
            )

            img_filename = imgflipmeme.url.split("/")[-1]
            generated["meme_imgage_page_url"] = imgflipmeme.page_url
            generated["meme_imgage_url"] = imgflipmeme.url
            generated["meme_image_filename"] = img_filename

            console.log("Meme image generated.")

            if download_render:
                status.update("Downloading meme image.")
                imgflipmeme.save(img_filename)
                status.update(f"Meme image saved: {img_filename}")

    pprint(generated, expand_all=True)


if __name__ == "__main__":
    app()
