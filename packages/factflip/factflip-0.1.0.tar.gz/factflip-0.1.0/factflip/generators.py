import logging
from collections import Counter
from typing import Dict, List

import chromadb

from factflip.llms import Llm, get_default_llm
from factflip.utils import dequote
from factflip.validators import DefaultMemeValidator, MemeValidator


class FactFlipMemeGenerator(object):
    def __init__(
        self,
        embeddings: chromadb.Collection,
        llm: Llm = None,
    ) -> None:
        self.embeddings = embeddings

        if not llm:
            self.llm = get_default_llm()
        else:
            self.llm = llm

    @staticmethod
    def _generate_messages(claim: str, review: str, examples) -> List[dict]:
        messages = [
            {
                "role": "system",
                "content": "You are a fact-checker and meme expert that provides short and acurate answers.",
            }
        ]

        for e in examples:
            title = e["imgflip_template"].split("/")[-1].replace("-", " ").strip()

            messages.append(
                {
                    "role": "user",
                    "content": f"Instruction: Generate a caption to turn the image into a meme. The meme must contains {e['kym_template_usage_concept']} and humour and be formulated as response to a erronous claim based on the provided claim review.",  # noqa E501
                }
            )
            messages.append(
                {
                    "role": "user",
                    "content": f"Input image: The image is \"{title}\". {e['imgflip_template_image_description']} {e['kym_template_usage']}",  # noqa E501
                }
            )
            messages.append(
                {
                    "role": "user",
                    "content": f"Input erronous claim: {e['imgflip_instance_claim']}",
                }
            )
            messages.append(
                {
                    "role": "user",
                    "content": f"Input claim review: {e['imgflip_instance_claim_correction']}",
                }
            )
            messages.append(
                {
                    "role": "assistant",
                    "content": f"Output meme caption: {e['imgflip_instance_text']}",
                }
            )

        messages.append(
            {
                "role": "user",
                "content": f"Instruction: Generate a caption to turn the image into a meme. The meme must contains {examples[0]['kym_template_usage_concept']} and humour and be formulated as response to a erronous claim based on the provided claim review.",  # noqa E501
            }
        )
        messages.append(
            {
                "role": "user",
                "content": f"Input image: The image is \"{title}\". {examples[0]['imgflip_template_image_description']} {examples[0]['kym_template_usage']}",  # noqa E501
            }
        )
        messages.append({"role": "user", "content": f"Input erronous claim: {claim}"})
        messages.append({"role": "user", "content": f"Input claim review: {review}"})

        return messages

    def generate_meme_text(self, claim: str, review: str, validator: MemeValidator = None) -> Dict[str, str]:
        log = logging.getLogger()
        if not validator:
            validator = DefaultMemeValidator(1)

        # 1) Find meme candidates and get the most comon template:
        candidates = self.embeddings.query(query_texts=[claim], n_results=10)
        meme_template = Counter([x["imgflip_template"] for x in candidates["metadatas"][0]]).most_common(1)[0][0]

        # 2) Find examples for the meme template:
        examples = self.embeddings.query(
            query_texts=["This is a question or text"],
            n_results=4,  # Best number found by memecraft.
            where={"imgflip_template": meme_template},
        )
        meme_template_id = examples["metadatas"][0][0]["imgflip_template_id"]

        # 3) Generate the prompt usig the examples
        messages = self.__class__._generate_messages(claim=claim, review=review, examples=examples["metadatas"][0])

        # 4) Generate the the meme:
        for i in range(max(1, validator.max_retries)):
            response = self.llm.chat(messages)

            # 5) Split the sentence in two:
            split_response = self.llm.generate(
                prompt=f"Just answer: Split the sentence in two: {response}",
            ).splitlines()[-2:]

            split_response = [dequote(x) for x in split_response]  # Remove quotes if present.

            if validator.validate_caption(split_response):
                log.info(split_response)
                break
            else:
                log.info(f"{i}/{max(1, validator.max_retries)} The meme was not valid: {split_response}")

        return {
            "template_url": meme_template,
            "template_id": meme_template_id,
            "meme_caption": split_response,
            "meme_claim": claim,
            "meme_claim_review": review,
        }
