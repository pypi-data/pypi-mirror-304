# When adding support for a new task, just add it to the list below
# Note: please make sure that input and output specifications for the task are
# available at https://github.com/huggingface/huggingface.js/tree/main/packages/tasks/src/tasks
# Tasks without specification:
# - audio-to-audio
# - image-feature-extraction
# - image-text-to-text
# - image-to-3d
# - keypoint-detection
# - mask-generation
# - reinforcement-learning
# - tabular-classification
# - tabular-regression
# - text-to-3d
# - text-to-video
# - unconditional-image-generation
# - video-text-to-text
# Tasks that do not have a signature following the inputs,parameters paradigm
# - chat-completion
# - feature-extraction
# Tasks that raised errors while generating (for various reasons)
# - depth-estimation
# - image-to-text
# - text-to-speech
# - video-classification
#
TASKS := \
audio-classification \
automatic-speech-recognition \
document-question-answering \
fill-mask \
image-classification \
image-segmentation \
image-to-image \
object-detection \
question-answering \
sentence-similarity \
summarization \
table-question-answering \
text-classification \
text-generation \
text-to-audio \
text-to-image \
text2text-generation \
token-classification \
translation \
visual-question-answering \
zero-shot-classification \
zero-shot-image-classification \
zero-shot-object-detection
