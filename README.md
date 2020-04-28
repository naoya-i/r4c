
<p align="center">
<img src="https://naoya-i.github.io/r4c/imgs/logo.png" width="100px">
</p>

# Introduction

This is the repository of the following paper:

- Naoya Inoue, Pontus Stenetorp and Kentaro Inui. R4C: A Benchmark for Evaluating RC Systems to Get the Right Answer for the Right Reason. In <i>Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL2020)</i>, July 2020, to appear.

See https://naoya-i.github.io/r4c/ for further information.


# Overview

This repository contains the following datasets and script:

- R4C Corpus (`corpus/train.json`, `corpus/dev_csf.json`)
- Prediction of two baseline models (CORE, IE) and oracle (`prediction/bm_core.json`, `prediction/bm_ie.json`, `prediction/oracle.json`)
- Official evaluation script (`src/r4c_evaluate.py`)
- Baseline models (TBA by July)
- Crowdsourcing interface (TBA by July)

# R4C corpus

The corpus is divided into the training set (`corpus/train.json`) and the dev set (`corpus/dev_csf.json`).


## R4C file format

The files are in standard JSON format.
The entire file is a big dictionary, where the key is an instance ID of [HotpotQA](https://hotpotqa.github.io) and the corresponding value is a list of derivations given by three different annotators.

```
{
  HOTPOTQA_INSTANCE_ID: [
    ANNOTATOR_1_DERIVATION,
    ANNOTATOR_2_DERIVATION,
    ANNOTATOR_3_DERIVATION
  ]
}
```

Each derivation (`ANNOTATOR_*_DERIVATION`) is represented as a list of derivation steps.
Each derivation step consists of a supporting fact (an article title and a sentence ID in HotpotQA) and a relational fact (a list of three strings---head, relation, tail).

```
[
  [
    ARTICLE_TITLE,
    SENTENCE_ID,
    [
      HEAD_ENTITY,
      RELATION,
      TAIL_ENTITY
    ]
  ],
  [
    ...
  ],
  ...
]
```

The following JSON fragment is an actual example from the corpus:

```
{
  "5a8b57f25542995d1e6f1371": [
    [
      [
        "Scott Derrickson",
        0,
        [
          "Scott Derrickson",
          "is",
          "an American director"
        ]
      ],
      [
        "Ed Wood",
        0,
        [
          "Ed Wood",
          "was",
          "an American filmmaker"
        ]
      ]
    ],
    [
      [
        "Scott Derrickson",
        0,
        [
          "Scott Derrickson",
          "is",
          "an American director"
        ]
      ],
      [
        "Ed Wood",
        0,
        [
          "Ed Wood",
          "is",
          "an American filmmaker"
        ]
      ]
    ],
    [
      [
        "Scott Derrickson",
        0,
        [
          "Scott Derrickson",
          "is",
          "an American director"
        ]
      ],
      [
        "Ed Wood",
        0,
        [
          "Ed Wood",
          "is",
          "an American filmmaker"
        ]
      ]
    ]
  ],
  "5a8c7595554299585d9e36b6": ...
```


# Official evaluation script

As described in Section 2.2 in the paper, the evaluation metric of R4C involves an optimization problem.
To make the evaluation easier and fair for everyone, we provide an official evaluation script written in Python.


## Dependency

Please install the following Python packages (you can install them via `pip install pulp editdistance tqdm`):

- `pulp`
- `editdistance`
- `tqdm`


## Prediction file format

The prediction file should basically follow [HotpotQA prediction file format](https://github.com/hotpotqa/hotpot#prediction-file-format) (a JSON dictionary).
On top of `answer` key (answers) and `sp` key (supporting facts), add `re` key for derivations.
The value of `re` should be a dictionary, where the key is a HotpotQA instance ID and the value is a derivation, similar to `answer` and `sp`.
Each derivation should follow the same format as [here](#r4c-file-format).
An example is given below.

```
{
  "answer": {
    "5a8b57f25542995d1e6f1371": "yes",
    ...
  },
  "sp": {
    "5a8b57f25542995d1e6f1371": [
      [
        "Scott Derrickson",
        0
      ],
      [
        "Ed Wood",
        0
      ]
    ],
    ...
  },
  "re": {
    "5a8b57f25542995d1e6f1371": [
      [
        "Scott Derrickson",
        0,
        [
          "Scott Derrickson",
          "is",
          "an American director"
        ]
      ],
      [
        "Ed Wood",
        0,
        [
          "Ed Wood",
          "was",
          "an American filmmaker"
        ]
      ]
    ],
    ...
  }
}
```

You can also find more example prediction files in `prediction` folder.


## How to run

To evaluate your prediction (say `/path/to/your_prediction.json`), simply run the following command:

`python src/r4c_evaluate.py --prediction /path/to/your_prediction.json --label corpus/dev_csf.json`

You can also use the HotpotQA official evaluation script to evaluate the performance of answer prediction and supporting facts prediction:

`python /path/to/hotpot_evaluate_v1.py /path/to/your_prediction.json /path/to/hotpot_dev_distractor_v1.json`


## Output format

The script outputs a JSON dictionary consisting of three entries:

- `"e"`: a list. Each element represents *entity-level* precision, recall, and f1.
- `"r"`: a list. Each element represents *relation-level* precision, recall, and f1.
- `"er"`: a list. Each element represents *full* precision, recall, and f1.

An example is given below.

```
{
  "e": [0.8243644596919709, 0.8341406821599607, 0.8241752304610381],
  "r": [0.7168995180557596, 0.7183956173976581, 0.7094029197329732],
  "er": [0.7685931868076684, 0.7757018447656213, 0.7666854346880572]
}
```

See Section 2.2 in the paper for further details.
