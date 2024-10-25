import os
import re
from pathlib import Path
from typing import Sequence

import chromadb
import pandas as pd
from rdflib import Graph
from rich.progress import track

from factflip import DEFAULT_EMBEDDINGS_PATH, DEFAULT_TEMPLATES_PATH
from factflip.llms import Llm, get_default_llm


def describe_imkg_memes(
    imkg_memes_df: pd.DataFrame,
    imgflip_templates_dir: Path = DEFAULT_TEMPLATES_PATH,
    llm: Llm = None,
) -> pd.DataFrame:
    data = []
    if not llm:
        llm = get_default_llm()

    tmpl_df = imkg_memes_df.groupby(["kym_template", "imgflip_template", "usage"]).first().reset_index()
    for _, row in track(
        tmpl_df.iterrows(),
        total=len(tmpl_df),
        description="Generating memes descriptions...",
    ):
        tmpl = row["imgflip_template"].split("/")[-1]
        tmpl_file = os.path.join(imgflip_templates_dir, f"{tmpl}.jpg")

        concept = llm.chat(
            messages=[
                {
                    "role": "system",
                    "content": "You are a fact-checker and meme expert that provides short and acurate answers.",
                },
                {
                    "role": "user",
                    "content": "Just answer in one or two words without punctuation, what is the main rethorical device used in the following meme description?",  # noqa E501
                },
                {"role": "user", "content": row["usage"]},
            ],
        ).lower()

        desc = llm.chat(
            messages=[
                {
                    "role": "system",
                    "content": "You are a fact-checker and meme expert who perfectly describes images concisely.",
                },
                {
                    "role": "user",
                    "content": f"Provide a short description for the image. Consider that the image is an image used for {concept} and humor.",  # noqa E501
                    "images": [tmpl_file],
                },
            ],
        )

        data.append(
            {
                "imgflip_template": row["imgflip_template"],
                "usage_concept": concept,
                "template_image_description": desc,
            }
        )

    return pd.DataFrame(data)


def query_imkg_memes(graph: Graph) -> pd.DataFrame:
    query = """
    SELECT DISTINCT ?kym_src ?imgf_src  ?imgf_template_src ?about ?alt_text ?views ?upvotes ?id
    WHERE
    {
        ?kym_src <https://meme4.science/title> ?title;
                <https://meme4.science/about> ?about .
        ?imgf_src <https://imgflip.com/template_title> ?title; <https://imgflip.com/template> ?imgf_template_src .
        ?imgf_src <https://imgflip.com/view_count>  ?views; <https://imgflip.com/upvote_count> ?upvotes; <https://imgflip.com/alt_text> ?alt_text; <https://imgflip.com/templateId> ?id
    }
    """  # noqa E501

    data = []
    qres = graph.query(query)
    for row in track(qres, description="Querying IMKG memes..."):
        if match := re.search(
            r"^ *([^|]+) *\| *([^|]+) *\| *image tagged in *([^|]+) *\|[^|]*$",
            row.alt_text.strip(),
            re.IGNORECASE,
        ):
            instance_text = match.group(2).strip()

        data.append(
            {
                "kym_template": row.kym_src.toPython().strip(),
                "imgflip_template": row.imgf_template_src.toPython().strip(),
                "imgflip_template_id": row.id.toPython().strip(),
                "imgflip_instance": row.imgf_src.toPython().strip(),
                "usage": row.about.toPython().strip(),
                "text": instance_text,
                "upvotes": (0 if row.upvotes.toPython() == "NA" else int(row.upvotes.toPython().replace(",", ""))),
                "views": (0 if row.views.toPython() == "NA" else int(row.views.toPython().replace(",", ""))),
            }
        )

    return pd.DataFrame(data)


def generate_imkg_claims(
    imkg_memes_df: pd.DataFrame,
    imkg_memes_descriptions_df: pd.DataFrame,
    llm: Llm = None,
    group_size: int = 50,
    group_sort: Sequence[str] = ["views", "upvotes"],
) -> pd.DataFrame:
    generated_claims = []

    merged_df = pd.merge(imkg_memes_df, imkg_memes_descriptions_df, on="imgflip_template").reset_index()

    memes_df = (
        merged_df.sort_values(group_sort, ascending=False)
        .groupby(["kym_template", "imgflip_template"])
        .head(group_size)
    )

    for _, row in track(
        memes_df.iterrows(),
        total=len(memes_df),
        description="Generating IMKG claims...",
    ):
        tmpl = row["imgflip_template"].split("/")[-1]
        title = tmpl.replace("-", " ").strip()

        correction_claim = (
            llm.chat(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a fact-checker and meme expert that provides short and acurate answers.",
                    },
                    {
                        "role": "user",
                        "content": f"Give a claim explaining the meaning of the following meme text. The text of the meme contains {row['usage_concept']} and humour.",  # noqa E501
                    },
                    {
                        "role": "user",
                        "content": f"The image used by the meme is \"{title}\". {row['usage']} {row['template_image_description']}",  # noqa E501
                    },
                    {
                        "role": "user",
                        "content": f"The text of the meme is: {row['text']}",
                    },
                    {
                        "role": "assistant",
                        "content": 'The one sentence claim explaning the meme is: "',
                    },
                ],
            )
            .split('"')[0]
            .strip()
        )

        claim = (
            llm.chat(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a fact-checker and meme expert that provides short and acurate answers.",
                    },
                    {
                        "role": "user",
                        "content": "Give a claim that contradict the following meme explanation.",
                    },
                    {"role": "user", "content": correction_claim},
                    {
                        "role": "assistant",
                        "content": 'The one sentence contradictory claim is: "',
                    },
                ],
            )
            .split('"')[0]
            .strip()
        )

        vec1 = llm.embed(prompt=row["text"])
        vec2 = llm.embed(prompt=claim)
        vec3 = llm.embed(prompt=correction_claim)

        generated_claims.append(
            {
                "kym_template": row["kym_template"],
                "imgflip_template": row["imgflip_template"],
                "imgflip_template_id": row["imgflip_template_id"],
                "imgflip_instance": row["imgflip_instance"],
                "imgflip_instance_text": row["text"],
                "imgflip_instance_claim": claim,
                "imgflip_instance_correction_claim": correction_claim,
                "imgflip_instance_text_vec": vec1,
                "imgflip_instance_claim_vec": vec2,
                "imgflip_instance_correction_claim_vec": vec3,
            }
        )

    return pd.DataFrame(generated_claims)


def merge_claims_data(
    imkg_memes_df: pd.DataFrame,
    imkg_memes_descriptions_df: pd.DataFrame,
    imkg_claims_df: pd.DataFrame,
) -> pd.DataFrame:
    merged_claims_df = pd.merge(
        imkg_memes_df,
        imkg_memes_descriptions_df,
        on="imgflip_template",
    )
    merged_claims_df = pd.merge(
        merged_claims_df,
        imkg_claims_df,
        on=["imgflip_instance", "kym_template", "imgflip_template", "imgflip_template_id"],
    )

    merged_claims_df = merged_claims_df[
        [
            "kym_template",
            "imgflip_template",
            "imgflip_template_id",
            "imgflip_instance",
            "usage",
            "text",
            "upvotes",
            "views",
            "usage_concept",
            "template_image_description",
            "imgflip_instance_claim",
            "imgflip_instance_correction_claim",
        ]
    ]
    return merged_claims_df.rename(
        columns={
            "usage": "kym_template_usage",
            "text": "imgflip_instance_text",
            "upvotes": "imgflip_instance_upvotes",
            "views": "imgflip_instance_views",
            "usage_concept": "kym_template_usage_concept",
            "template_image_description": "imgflip_template_image_description",
            "claim": "imgflip_instance_claim",
            "claim_correction": "imgflip_instance_correction_claim",
        }
    )


def build_embeddings_database(
    merged_claims_df: pd.DataFrame,
    path: Path = DEFAULT_EMBEDDINGS_PATH,
    delete_collection: bool = False,
) -> chromadb.Collection:
    client = chromadb.PersistentClient(path=str(path))

    if delete_collection:
        client.delete_collection("claims")
    collection = client.get_or_create_collection("claims")

    collection.add(
        documents=merged_claims_df.imgflip_instance_claim.to_list(),
        metadatas=merged_claims_df[
            [
                "kym_template",
                "imgflip_template_id",
                "imgflip_template",
                "imgflip_instance",
                "imgflip_instance_text",
                "imgflip_instance_claim",
            ]
        ].to_dict("records"),
        ids=merged_claims_df.imgflip_instance.to_list(),
    )

    return collection
