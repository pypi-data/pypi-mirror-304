<small>EN | [简体中文](https://github.com/cui-shaobo/causal-strength/blob/main/README_zh.md) </small>
# causal-strength  ![Causal Strength](https://img.shields.io/badge/causal--strength-%E2%9A%96%EF%B8%8F%20measurement%20of%20causality-blue) : Measure the Strength Between Cause and Effect

<a href="https://aclanthology.org/2024.findings-acl.384/">
    <img src="https://img.shields.io/badge/2024.findings-acl.384-blue.svg?style=flat-square" alt="ACL Anthology" />
</a>
<a href="https://pypi.org/project/causal-strength/">
    <img src="https://img.shields.io/pypi/v/causal-strength?style=flat-square" alt="PyPI version" />
</a>



**causal-strength** is a Python package for evaluating the causal strength between statements using various metrics such as CESAR (Causal Embedding aSsociation
with Attention Rating). This package leverages pre-trained models available on [Hugging Face Transformers](https://huggingface.co/) for efficient and scalable computations.

## Table of Contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [📜 Citation *](#-citation-)
- [🌟 Features *](#-features-)
- [🚀 Installation *](#-installation-)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [🛠️ Usage  *](#-usage--)
  - [Quick Start](#quick-start)
  - [Evaluating Causal Strength](#evaluating-causal-strength)
  - [Generating Causal Heatmaps](#generating-causal-heatmaps)
- [📚 References *](#-references-)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## 📜 Citation ![Citation](https://img.shields.io/badge/Citation-Required-green) 

If you find this package helpful, please star this repository [causal-strength](https://github.com/cui-shaobo/causal-strength) and the related repository: [defeasibility-in-causality](https://github.com/cui-shaobo/defeasibility-in-causality). For academic purposes, please cite our paper:

```bibtex
@inproceedings{cui-etal-2024-exploring,
    title = "Exploring Defeasibility in Causal Reasoning",
    author = "Cui, Shaobo  and
      Milikic, Lazar  and
      Feng, Yiyang  and
      Ismayilzada, Mete  and
      Paul, Debjit  and
      Bosselut, Antoine  and
      Faltings, Boi",
    booktitle = "Findings of the Association for Computational Linguistics ACL 2024",
    month = aug,
    year = "2024",
    address = "Bangkok, Thailand and virtual meeting",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.findings-acl.384",
    doi = "10.18653/v1/2024.findings-acl.384",
    pages = "6433--6452",
}
```


## 🌟 Features ![Key Features](https://img.shields.io/badge/Key_Features-Highlights-orange) 

- **Causal Strength Evaluation**: Compute the causal strength between two statements using models like CESAR.
- **Visualization Tools**: Generate heatmaps to visualize attention and similarity scores between tokens.
- **Extensibility**: Easily add new metrics and models for evaluation.
- **Hugging Face Integration**: Load models directly from the Hugging Face Model Hub.

## 🚀 Installation ![Installation](https://img.shields.io/badge/Installation-Guide-blue)

### Prerequisites

- Python 3.7 or higher
- [PyTorch](https://pytorch.org/) (for GPU support, ensure CUDA is properly configured)

### Steps

1. **Install it directly from PyPI**
    ```bash
    pip install causal-strength
    ```

2. **Install it from source code**

   ```bash
   git clone https://github.com/cui-shaobo/causal-strength.git
   cd causal-strength
   pip install .
   ```


## 🛠️ Usage  ![Usage](https://img.shields.io/badge/Usage-Instructions-green)

### Quick Start
Here's a quick example to evaluate the causal strength between two statements:

```python
from causalstrength import evaluate

# Test CESAR Model
s1_cesar = "Tom is very hungry now."
s2_cesar = "He goes to McDonald for some food."

print("Testing CESAR model:")
cesar_score = evaluate(s1_cesar, s2_cesar, model_name='CESAR', model_path='shaobocui/cesar-bert-large')
print(f"CESAR Causal strength between \"{s1_cesar}\" and \"{s2_cesar}\": {cesar_score:.4f}")
```

This will output the following without errors:
```plaintext
Testing CESAR model:
CESAR Causal strength between "Tom is very hungry now." and "He goes to McDonald for some food.": 0.4482
```


### Evaluating Causal Strength

The `evaluate` function computes the causal strength between two statements.

1. For the CESAR model. 

    ```python
    from causalstrength import evaluate
    
    # Test CESAR Model
    s1_cesar = "Tom is very hungry now."
    s2_cesar = "He goes to McDonald for some food."
    
    print("Testing CESAR model:")
    cesar_score = evaluate(s1_cesar, s2_cesar, model_name='CESAR', model_path='shaobocui/cesar-bert-large')
    print(f"CESAR Causal strength between \"{s1_cesar}\" and \"{s2_cesar}\": {cesar_score:.4f}")
    ```
   This will now output the following without errors:
    ```plaintext
    Testing CESAR model:
    CESAR Causal strength between "Tom is very hungry now." and "He goes to McDonald for some food.": 0.4482
    ```
2. For the CEQ model
   ```python
    from causalstrength import evaluate

    # Test CEQ Model
    s1_ceq = "Tom is very hungry now."
    s2_ceq = "He goes to McDonald for some food."
    
    print("\nTesting CEQ model:")
    ceq_score = evaluate(s1_ceq, s2_ceq, model_name='CEQ')
    print(f"CEQ Causal strength between \"{s1_ceq}\" and \"{s2_ceq}\": {ceq_score:.4f}")
    ```
   This will now output the following without errors:
    ```plaintext
    Testing CEQ model:
    CEQ Causal strength between "Tom is very hungry now." and "He goes to McDonald for some food.": 0.0168
    ```

**Parameters:**

- `s1` (str): The cause statement.
- `s2` (str): The effect statement.
- `model_name` (str): The name of the model to use (`'CESAR'`, `'CEQ'`, etc.).
- `model_path` (str): Hugging Face model identifier or local path to the model.

### Generating Causal Heatmaps

Visualize the attention and similarity scores between tokens using heatmaps.

```python
from causalstrength.visualization.causal_heatmap import plot_causal_heatmap

# Statements to visualize
s1 = "Tom is very hungry now."
s2 = "He goes to McDonald for some food."

# Generate heatmap
plot_causal_heatmap(
    s1,
    s2,
    model_name='shaobocui/cesar-bert-large',
    save_path='causal_heatmap.png'
)
```
This will now output the following without errors:
```plaintext
Testing CESAR model:
Warning: The sliced score_map dimensions do not match the number of tokens.
The causal heatmap is saved to ./figures/causal_heatmap.png
```

The causal heatmap is as follows: 
![Example Image](https://github.com/cui-shaobo/public-images/raw/main/causal-strength/heatmap.png)




[//]: # (## Acknowledgments)

[//]: # (+ HuggingFace Transformers - For providing the model hub and transformer implementations)

[//]: # (+ PyTorch - For providing the deep learning framework)


## 📚 References ![References](https://img.shields.io/badge/References-Scholarly-green)
1. Cui, Shaobo, et al. "Exploring Defeasibility in Causal Reasoning." Findings of the Association for Computational Linguistics ACL 2024. 2024. 
2. Du, Li, et al. "e-CARE: a New Dataset for Exploring Explainable Causal Reasoning." Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). 2022.