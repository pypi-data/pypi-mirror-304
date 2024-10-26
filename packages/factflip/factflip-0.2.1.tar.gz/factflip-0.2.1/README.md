# 🖼️ FactFlip

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> FactFlip is an image macro meme generator designed for creating fact-checking memes based on misinforming claims and their corrections.

## ℹ️ Installation and Usage

Factflip can be installed using pip:

```
pip install factflip
```

### 📒 Requirements

Counsel requires an [Ollama](https://ollama.com/) installation for running the LLMs used for generating the memes. An [Imgflip](https://imgflip.com/api) username and password is required for generating the meme image.

### 🖥️ Command Line Interface (CLI)

Factflip has a simple CLI interface that be accessed using the ``` factflip ``` command.
Before starting, run ```factflip download``` for downloading the precomputed embeddings database. Alternatively, you can build the database from scrathc using  the ```factflip build``` command. Building the database manually can take a few hours.

```
 Usage: factflip [OPTIONS] COMMAND [ARGS]...

 🖼️  Factflip - A claim-based meme generator powered by IMKG and LLMs.

╭─ Options ────────────────────────────────────────────────────────────────────────────────╮
│ --version  -v        Show the installed factflip version.                                │
│ --help               Show this message and exit.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────╮
│ build      Build the meme embedding                                                      │
│ download   Download precomputed Factflip embeddings.                                     │
│ generate   Generate the text of a meme.                                                  │
│ render     Render a meme instance using the imgflip API.                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
```

## 🎓 Publication

> Filipe Altoe, Gregoire Burel, Sergio Miguel Gonçalves Pinto, Harith Alani and H. Sofia Pinto. *"Towards AI-mediated Meme Generation for Misinformation Corrective Explanation"*. EMAI-XAI24, CAI 2024. IOS Press, 2024.

## 📐 Architecture

FactFlip, like [MemeCraft](https://arxiv.org/abs/2403.14652), uses a large language model to understand and generate memes. However, FactFlip focuses on creating specific memes to debunk misinformation, using humour and well-matched meme formats to make the corrections clear and engaging.

![FactFlip Architecture](.//images/factflip_architecture.png)

## 🤖 Prompts

The following prompts are currently used by FactFlip.

### Meme Concept Extraction (Step A)

The following prompt is used for extracting the main concept based on the meme template usage description.

```json
[
   {
      "role": "system",
      "content": "You are a fact-checker and meme expert who provides short and accurate answers."
   },
   {
      "role": "user",
      "content": "Just answer in one or two words without punctuation, what is the main rhetorical device used in the following meme description?"
   },
   {
      "role": "user",
      "content":"<IMAGE_TEMPALTE_USAGE>"
   }
]
```

### Meme Image Captioning (Step B)

The image description is extracted using the following prompt.

```json
[
   {
      "role": "system",
      "content": "You are a fact-checker and meme expert who perfectly describes images concisely."
   },
   {
      "role": "user",
      "content": "Provide a short description for the image. Consider that the image is an image used for  <CONCEPT> and humour.",
      "images":"<IMAGE>"
   }
]
```

### Meme Claims Generation(Step C)

The claim behind a given meme content is extracted with this prompt.

```json
[
   {
      "role": "system",
      "content": "You are a fact-checker and meme expert who provides short and accurate answers."
   },
   {
      "role": "user",
      "content": "Give a claim explaining the meaning of the following meme text. The text of the meme contains <CONCEPT> and humour."
   },
   {
      "role": "user",
      "content": "The image used by the meme is <IMAGE_TITLE>. <IMAGE_TEMPLATE_DESCRIPTION> <IMAGE_TEMPALTE_USAGE>"
   },
   {
      "role": "user",
      "content": "The text of the meme is: <CAPTION>"
   },
   {
      "role": "assistant",
      "content": "The one sentence claim explaining the meme is: \""
   }
]
```

The misinforming claim is extracted as follows.

```json
[
   {
      "role": "system",
      "content": "You are a fact-checker and meme expert who provides short and accurate answers."
   },
   {
      "role": "user",
      "content": "Give a claim that contradicts the following meme explanation."
   },
   {
      "role": "user",
      "content":"<CLAIM_CORRECTION>"
   },
   {
      "role": "assistant",
      "content": "The one sentence contradictory claim is: \""
   }
]
```

### Meme Caption Generation (Step 3)

The following prompt is used for generating the meme caption. The actual prompt uses 4 examples.

```json
[
   {
      "role": "system",
      "content": "You are a fact-checker and meme expert who provides short and accurate answers."
   },
   {
      "role": "user",
      "content":"Instruction: Generate a caption to turn the image into a meme. The meme must contain <EXAMPLE_CONCEPT> and humour and be formulated as a response to an erroneous claim based on the provided claim review."
   },
   {
      "role": "user",
      "content": "Input image: The image is <EXAMPLE_IMAGE_TITLE>. <EXAMPLE_IMAGE_TEMPLATE_DESCRIPTION> <EXAMPLE_IMAGE_TEMPALTE_USAGE>"
   },
   {
      "role": "user",
      "content": "Input erroneous claim: <EXAMPLE_CLAIM>"
   },
   {
      "role": "user",
      "content": "Input claim review:<EXAMPLE_CLAIM_CORRECTION>"
   },
   {
      "role": "assistant",
      "content": "Output meme caption: <EXAMPLE_MEME_CAPTION>"
   },
   {
      "role": "user",
      "content": "Instruction: Generate a caption to turn the image into a meme. The meme must contain <CONCEPT> and humour and be formulated as a response to an erroneous claim based on the provided claim review."
   },
   {
      "role": "user",
      "content": "Input image: The image is <IMAGE_TITLE>. <IMAGE_TEMPLATE_DESCRIPTION> <IMAGE_TEMPALTE_USAGE>"
   },
   {
      "role": "user",
      "content": "Input erroneous claim: <CLAIM>"
   },
   {
      "role": "user",
      "content": "Input claim review: <CLAIM_CORRECTION>"
   }
]
```

The resulting meme caption is split using the following prompt:

```json
"Just answer: Split the sentence in two: <MEME_CAPTION>"
```
