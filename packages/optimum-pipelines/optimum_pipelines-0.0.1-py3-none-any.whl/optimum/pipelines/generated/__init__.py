# Copyright 2024 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from .audio_classification.pipeline import *
from .automatic_speech_recognition.pipeline import *
from .document_question_answering.pipeline import *
from .fill_mask.pipeline import *
from .image_classification.pipeline import *
from .image_segmentation.pipeline import *
from .image_to_image.pipeline import *
from .object_detection.pipeline import *
from .question_answering.pipeline import *
from .sentence_similarity.pipeline import *
from .summarization.pipeline import *
from .table_question_answering.pipeline import *
from .text2text_generation.pipeline import *
from .text_classification.pipeline import *
from .text_generation.pipeline import *
from .text_to_audio.pipeline import *
from .text_to_image.pipeline import *
from .token_classification.pipeline import *
from .translation.pipeline import *
from .visual_question_answering.pipeline import *
from .zero_shot_classification.pipeline import *
from .zero_shot_image_classification.pipeline import *
from .zero_shot_object_detection.pipeline import *


tasks = [
    "audio-classification",
    "automatic-speech-recognition",
    "document-question-answering",
    "fill-mask",
    "image-classification",
    "image-segmentation",
    "image-to-image",
    "object-detection",
    "question-answering",
    "sentence-similarity",
    "summarization",
    "table-question-answering",
    "text-classification",
    "text-generation",
    "text-to-audio",
    "text-to-image",
    "text2text-generation",
    "token-classification",
    "translation",
    "visual-question-answering",
    "zero-shot-classification",
    "zero-shot-image-classification",
    "zero-shot-object-detection",
]
