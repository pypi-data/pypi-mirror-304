# Optimum Pipelines

🤗 `optimum-pipelines` is a framework for maintaining and contributing inference pipelines for [Hugging Face hub models](https://huggingface.co/models).

The pipelines are objects implementing workflows corresponding to several tasks applied to hub models.

They provide a unified API for local or remote inference, with a dedicated [JSON schema](https://github.com/huggingface/huggingface.js/tree/main/packages/tasks/src/tasks) for each task.

## Building the package

```shell
$ make package
```

## Running the tests

First, install the package:

```shell
$ python -m pip install dist/optimum_pipelines-<version>.tar.gz
```

```shell
$ make test
```
