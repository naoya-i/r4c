# Introduction

(Under construction)

This is the repository of R4C corpus introduced in the following paper:

- **Naoya Inoue**, Pontus Stenetorp and Kentaro Inui. R4C: A Benchmark for Evaluating RC Systems to Get the Right Answer for the Right Reason. In <i>Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL2020)</i>, July 2020, to appear.

See https://naoya-i.github.io/r4c/ for more about R4C corpus.


# What we have in the repository

This repository contains:

- R4C Corpus
- Official evaluation script
- Prediction of two baseline models (CORE, IE) and oracle


# R4C Corpus

The training set and the dev set are `corpus/train.json`, `corpus/dev_csf.json`, respectively.

## File format

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
  "5a8c7595554299585d9e36b6": [...],
  ...
}
```


# Official evaluation script

## Prepare your output

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
  }
}
```

You can find example prediction file in `prediction/bm_core.json` (baseline model CORE), `prediction/bm_ie.json` (baseline model IE) and `prediction/oracle.json` (human oracle).


## How to run

`python src/r4c_evaluate.py --prediction /path/to/your_output.json --label corpus/dev_csf.json`


## Output format

```
{"e": [0.8243644596919709, 0.8341406821599607, 0.8241752304610381], "r": [0.7168995180557596, 0.7183956173976581, 0.7094
029197329732], "er": [0.7685931868076684, 0.7757018447656213, 0.7666854346880572]}
```