![Python](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-brightgreen?style=for-the-badge)
[![PyPI version](https://img.shields.io/pypi/v/xinfer.svg?style=for-the-badge&logo=pypi&logoColor=white&label=PyPI&color=blue)](https://pypi.org/project/xinfer/)
[![Downloads](https://img.shields.io/pypi/dm/xinfer.svg?style=for-the-badge&logo=pypi&logoColor=white&label=Downloads&color=purple)](https://pypi.org/project/xinfer/)
![License](https://img.shields.io/badge/License-Apache%202.0-green.svg?style=for-the-badge&logo=apache&logoColor=white)


<div align="center">
    <img src="https://raw.githubusercontent.com/dnth/x.infer/refs/heads/main/assets/xinfer.jpg" alt="x.infer" width="500"/>
    <br />
    <br />
    <a href="https://dnth.github.io/x.infer" target="_blank" rel="noopener noreferrer"><strong>Explore the docs »</strong></a>
    <br />
    <a href="#quickstart" target="_blank" rel="noopener noreferrer">Quickstart</a>
    ·
    <a href="https://github.com/dnth/x.infer/issues/new?assignees=&labels=Feature+Request&projects=&template=feature_request.md" target="_blank" rel="noopener noreferrer">Feature Request</a>
    ·
    <a href="https://github.com/dnth/x.infer/issues/new?assignees=&labels=bug&projects=&template=bug_report.md" target="_blank" rel="noopener noreferrer">Report Bug</a>
    ·
    <a href="https://github.com/dnth/x.infer/discussions" target="_blank" rel="noopener noreferrer">Discussions</a>
    ·
    <a href="https://dicksonneoh.com/" target="_blank" rel="noopener noreferrer">About</a>
</div>


## 🤔 Why x.infer?
If you'd like to run many models from different libraries without having to rewrite your inference code, x.infer is for you. It has a simple API and is easy to extend. Currently supports Transformers, Ultralytics, and TIMM.

Run any supported model using the following 4 lines of code:

```python
import xinfer

model = xinfer.create_model("vikhyatk/moondream2")
model.infer(image, prompt)         # Run single inference
model.infer_batch(images, prompts) # Run batch inference
model.launch_gradio()              # Launch Gradio interface
```

Have a custom model? Create a class that implements the `BaseModel` interface and register it with x.infer. See [Adding New Models](#adding-new-models) for more details.

## 🌟 Key Features
<div align="center">
  <img src="https://raw.githubusercontent.com/dnth/x.infer/refs/heads/main/assets/flowchart.gif" alt="x.infer" width="500"/>
</div>

- **Unified Interface:** Interact with different machine learning models through a single, consistent API.
- **Modular Design:** Integrate and swap out models without altering the core framework.
- **Ease of Use:** Simplifies model loading, input preprocessing, inference execution, and output postprocessing.
- **Extensibility:** Add support for new models and libraries with minimal code changes.

## 🚀 Quickstart

Here's a quick example demonstrating how to use x.infer with a Transformers model:

[![Open In Colab](https://img.shields.io/badge/Open%20In-Colab-blue?style=for-the-badge&logo=google-colab)](https://colab.research.google.com/github/dnth/x.infer/blob/main/nbs/quickstart.ipynb)
[![Open In Kaggle](https://img.shields.io/badge/Open%20In-Kaggle-blue?style=for-the-badge&logo=kaggle)](https://kaggle.com/kernels/welcome?src=https://github.com/dnth/x.infer/blob/main/nbs/quickstart.ipynb)

```python
import xinfer

model = xinfer.create_model("vikhyatk/moondream2")

image = "https://raw.githubusercontent.com/vikhyat/moondream/main/assets/demo-1.jpg"
prompt = "Describe this image. "

model.infer(image, prompt)

>>> An animated character with long hair and a serious expression is eating a large burger at a table, with other characters in the background.
```

Get a list of models:
```python
xinfer.list_models()
```

```
       Available Models                                      
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Implementation ┃ Model ID                                        ┃ Input --> Output     ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ timm           │ eva02_large_patch14_448.mim_m38m_ft_in22k_in1k  │ image --> categories │
│ timm           │ eva02_large_patch14_448.mim_m38m_ft_in1k        │ image --> categories │
│ timm           │ eva02_large_patch14_448.mim_in22k_ft_in22k_in1k │ image --> categories │
│ timm           │ eva02_large_patch14_448.mim_in22k_ft_in1k       │ image --> categories │
│ timm           │ eva02_base_patch14_448.mim_in22k_ft_in22k_in1k  │ image --> categories │
│ timm           │ eva02_base_patch14_448.mim_in22k_ft_in1k        │ image --> categories │
│ timm           │ eva02_small_patch14_336.mim_in22k_ft_in1k       │ image --> categories │
│ timm           │ eva02_tiny_patch14_336.mim_in22k_ft_in1k        │ image --> categories │
│ transformers   │ Salesforce/blip2-opt-6.7b-coco                  │ image-text --> text  │
│ transformers   │ Salesforce/blip2-flan-t5-xxl                    │ image-text --> text  │
│ transformers   │ Salesforce/blip2-opt-6.7b                       │ image-text --> text  │
│ transformers   │ Salesforce/blip2-opt-2.7b                       │ image-text --> text  │
│ transformers   │ fancyfeast/llama-joycaption-alpha-two-hf-llava  │ image-text --> text  │
│ transformers   │ vikhyatk/moondream2                             │ image-text --> text  │
│ transformers   │ sashakunitsyn/vlrm-blip2-opt-2.7b               │ image-text --> text  │
│ ultralytics    │ yolov8x                                         │ image --> boxes      │
│ ultralytics    │ yolov8m                                         │ image --> boxes      │
│ ultralytics    │ yolov8l                                         │ image --> boxes      │
│ ultralytics    │ yolov8s                                         │ image --> boxes      │
│ ultralytics    │ yolov8n                                         │ image --> boxes      │
│ ...            │ ...                                             │ ...                  │
│ ...            │ ...                                             │ ...                  │
└────────────────┴─────────────────────────────────────────────────┴──────────────────────┘
```

## 🖥️ Launch Gradio Interface

```python
model.launch_gradio()
```

![Gradio Interface](https://raw.githubusercontent.com/dnth/x.infer/refs/heads/main/assets/gradio.png)


## 📦 Installation
> [!IMPORTANT]
> You must have [PyTorch](https://pytorch.org/get-started/locally/) installed to use x.infer.

To install the barebones x.infer (without any optional dependencies), run:
```bash
pip install xinfer
```
x.infer can be used with multiple optional libraries. You'll just need to install one or more of the following:

```bash
pip install "xinfer[transformers]"
pip install "xinfer[ultralytics]"
pip install "xinfer[timm]"
```

To install all libraries, run:
```bash
pip install "xinfer[all]"
```

To install from a local directory, run:
```bash
git clone https://github.com/dnth/x.infer.git
cd x.infer
pip install -e .
```

## 🛠️ Usage


### Supported Models


Transformers:
<!DOCTYPE html>
<html lang="en">
<body>
    <table>
        <thead>
            <tr>
                <th>Model</th>
                <th>Usage</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><a href="https://huggingface.co/Salesforce/blip2-opt-2.7b">BLIP2 Series</a></td>
                <td><code>xinfer.create_model("Salesforce/blip2-opt-2.7b")</code></td>
            </tr>
            <tr>
                <td><a href="https://github.com/vikhyat/moondream">Moondream2</a></td>
                <td><code>xinfer.create_model("vikhyatk/moondream2")</code></td>
            </tr>
            <tr>
                <td><a href="https://huggingface.co/sashakunitsyn/vlrm-blip2-opt-2.7b">VLRM-BLIP2</a></td>
                <td><code>xinfer.create_model("sashakunitsyn/vlrm-blip2-opt-2.7b")</code></td>
            </tr>
            <tr>
                <td><a href="https://github.com/fpgaminer/joycaption">JoyCaption</a></td>
                <td><code>xinfer.create_model("fancyfeast/llama-joycaption-alpha-two-hf-llava")</code></td>
            </tr>
        </tbody>
    </table>
</body>
</html>

> [!NOTE]
> Wish to load an unsupported model?
> You can load any [Vision2Seq model](https://huggingface.co/docs/transformers/main/en/model_doc/auto#transformers.AutoModelForVision2Seq) 
> from Transformers by using the `Vision2SeqModel` class.

```python
from xinfer.transformers import Vision2SeqModel

model = Vision2SeqModel("facebook/chameleon-7b")
model = xinfer.create_model(model)
```



TIMM:
All models from [TIMM](https://github.com/huggingface/pytorch-image-models) fine-tuned for ImageNet 1k are supported.

> [!NOTE]
> Wish to load an unsupported model?
> You can load any model from TIMM by using the `TIMMModel` class.

```python
from xinfer.timm import TimmModel

model = TimmModel("resnet18")
model = xinfer.create_model(model)
```


Ultralytics:
<table>
    <thead>
        <tr>
            <th>Model</th>
            <th>Usage</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="https://github.com/ultralytics/ultralytics">YOLOv8 Series</a></td>
            <td><code>xinfer.create_model("yolov8n")</code></td>
        </tr>
        <tr>
            <td><a href="https://github.com/ultralytics/ultralytics">YOLOv10 Series</a></td>
            <td><code>xinfer.create_model("yolov10x")</code></td>
        </tr>
        <tr>
            <td><a href="https://github.com/ultralytics/ultralytics">YOLOv11 Series</a></td>
            <td><code>xinfer.create_model("yolov11s")</code></td>
        </tr>
    </tbody>
</table>

> [!NOTE]
> Wish to load an unsupported model?
> You can load any model from Ultralytics by using the `UltralyticsModel` class.

```python
from xinfer.ultralytics import UltralyticsModel

model = UltralyticsModel("yolov5n6u")
model = xinfer.create_model(model)
```

vLLM:

<table>
    <thead>
        <tr>
            <th>Model</th>
            <th>Usage</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="https://huggingface.co/allenai/Molmo-72B-0924">Molmo-72B</a></td>
            <td><code>xinfer.create_model("allenai/Molmo-72B-0924")</code></td>
        </tr>
        <tr>
            <td><a href="https://huggingface.co/allenai/Molmo-7B-D-0924">Molmo-7B-D</a></td>
            <td><code>xinfer.create_model("allenai/Molmo-7B-D-0924")</code></td>
        </tr>
        <tr>
            <td><a href="https://huggingface.co/allenai/Molmo-7B-O-0924">Molmo-7B-O</a></td>
            <td><code>xinfer.create_model("allenai/Molmo-7B-O-0924")</code></td>
        </tr>
    </tbody>
</table>


### 🔧 Adding New Models

+ **Step 1:** Create a new model class that implements the `BaseModel` interface.

+ **Step 2:** Implement the required abstract methods `load_model`, `infer`, and `infer_batch`.

+ **Step 3:** Decorate your class with the `register_model` decorator, specifying the model ID, implementation, and input/output.

For example:
```python
@xinfer.register_model("my-model", "custom", ModelInputOutput.IMAGE_TEXT_TO_TEXT)
class MyModel(BaseModel):
    def load_model(self):
        # Load your model here
        pass

    def infer(self, image, prompt):
        # Run single inference 
        pass

    def infer_batch(self, images, prompts):
        # Run batch inference here
        pass
```
