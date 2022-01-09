#!/bin/bash

# defines the qa model
MODEL_DIR="https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L6-v2/resolve/main"
MODEL_NAME="paraphrase-MiniLM-L6-v2"

# downloads the qa model. To make this image more general one can use wget
# with the "-i requires.txt" argument to download the necessary files defined
# in "requires.txt".
mkdir ${MODEL_NAME} &&\
    wget --directory-prefix=${MODEL_NAME} ${MODEL_DIR}/vocab.txt &&\
    wget --directory-prefix=${MODEL_NAME} ${MODEL_DIR}/tokenizer_config.json &&\
    wget --directory-prefix=${MODEL_NAME} ${MODEL_DIR}/tokenizer.json &&\
    wget --directory-prefix=${MODEL_NAME} ${MODEL_DIR}/special_tokens_map.json &&\
    wget --directory-prefix=${MODEL_NAME} ${MODEL_DIR}/sentence_bert_config.json &&\
    wget --directory-prefix=${MODEL_NAME} ${MODEL_DIR}/pytorch_model.bin &&\
    wget --directory-prefix=${MODEL_NAME} ${MODEL_DIR}/modules.json &&\
    wget --directory-prefix=${MODEL_NAME} ${MODEL_DIR}/config_sentence_transformers.json &&\
    wget --directory-prefix=${MODEL_NAME} ${MODEL_DIR}/config.json