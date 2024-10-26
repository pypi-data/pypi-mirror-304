import os
from pathlib import Path

import chromadb
import pandas as pd
import requests
from imgflip import AsyncMeme, Imgflip, SyncMeme
from rich.progress import track

from factflip.generators import FactFlipMemeGenerator
from factflip.llms import OllamaLlm
from factflip.utils import dequote
from factflip.validators import FactFlipMemeValidator


def create_memes_from_summaries(embeddings: chromadb.Collection, fc_df: pd.DataFrame, drop_na=False) -> pd.DataFrame:
    model = "llava:13b-v1.6"
    generator = FactFlipMemeGenerator(embeddings=embeddings, llm=OllamaLlm(model))

    if drop_na:
        memes = fc_df[fc_df.verdict.notna()].progress_apply(
            lambda row: generator.generate_meme_text(
                claim=row.claim, review=row.verdict, validator=FactFlipMemeValidator(10)
            ),
            axis=1,
        )
    else:
        memes = fc_df.progress_apply(
            lambda row: generator.generate_meme_text(
                claim=row.claim, review=row.verdict, validator=FactFlipMemeValidator(10)
            ),
            axis=1,
        )
    return pd.DataFrame(memes.to_list())


def create_imgflip_meme(meme: dict, imgflip_username: str, imgflip_password: str) -> SyncMeme | AsyncMeme:
    imgflip = Imgflip(username=imgflip_username, password=imgflip_password, session=requests.Session())

    if len(meme["meme_caption"]) > 1:
        imgflipmeme = imgflip.make_meme(
            template=meme["template_id"],
            top_text=meme["meme_caption"][0],
            bottom_text=meme["meme_caption"][1],
        )
    else:
        imgflipmeme = imgflip.make_meme(template=meme["template_id"], top_text=meme["meme_caption"][0])
    return imgflipmeme


def create_imgflip_memes(generated_memes_df: pd.DataFrame, output_dir: Path):
    images = []
    for _, row in track(generated_memes_df.iterrows(), description="Creating Imgflip memes..."):
        img_meme = create_imgflip_meme(
            {
                "template_id": row.template_id,
                "meme_caption": [dequote(x) for x in row.meme_caption],
            }
        )
        img_filename = img_meme.url.split("/")[-1]
        img_meme.save(os.path.join(output_dir, img_filename))

        images.append(
            {
                "meme_imgage_page_url": img_meme.page_url,
                "meme_imgage_url": img_meme.url,
                "meme_image_filename": img_filename,
            }
        )

    return pd.DataFrame(images)
