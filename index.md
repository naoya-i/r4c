---
layout: home
---

<p align="center">
<img src="./imgs/logo.png" width="100px"/> <br />
</p>

# About R4C

Recent studies have revealed that reading comprehension (RC) systems learn to exploit annotation artifacts and other biases in current datasets.
This prevents the community from reliably measuring the progress of RC systems.
To address this issue, we introduce R4C, a new task for evaluating RC systems' internal reasoning.
R4C requires giving not only answers but also derivations: explanations that justify predicted answers.

<p align="center">
<img src="./imgs/fig1.png" width="60%"/> <br />
</p>

This website publicly releases the R4C dataset, the first, quality-assured dataset consisting of 4.6k questions, each of which is annotated with 3 reference derivations (i.e. 13.8k derivations).


# Download

[This repository](https://github.com/naoya-i/r4c) contains the R4C corpus and its official evaluation script.


# Leaderboard

## Full prediction setting

|Model|Entity|Relation|Full|Resource|
|-|-|-|-|-|
| Human [1]           | 83.3/81.5/81.6 | 72.2/69.2/69.8 | 77.6/75.0/75.5 | [Prediction](https://github.com/naoya-i/r4c/blob/master/prediction/oracle.json) |


## Golden supporting facts setting

|Model|Entity|Relation|Full|Resource|
|-|-|-|-|-|
| Human [1]           | 83.3/81.5/81.6 | 72.2/69.2/69.8 | 77.6/75.0/75.5 | [Prediction](https://github.com/naoya-i/r4c/blob/master/prediction/oracle.json) |
| Baseline (CORE) [1] | 66.1/59.8/61.8 | 50.9/45.9/47.4 | 59.1/53.4/55.1 | [Prediction](https://github.com/naoya-i/r4c/blob/master/prediction/bm_core.json) |
| Baseline (IE) [1]   | 11.1/52.8/16.3 | 13.7/62.7/19.9 | 11.2/51.9/16.3 | [Prediction](https://github.com/naoya-i/r4c/blob/master/prediction/bm_ie.json) |


## Model references

1. Naoya Inoue, Pontus Stenetorp and Kentaro Inui. R4C: A Benchmark for Evaluating RC Systems to Get the Right Answer for the Right Reason. In <i>Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL2020)</i>, July 2020, to appear.
1. *Your work here!*

To list your work, please contact us the following information:

1. Your prediction file following [R4C prediction file format](https://github.com/naoya-i/r4c#prediction-file-format)
2. Output of [the official evaluation script](https://github.com/naoya-i/r4c#official-evaluation-script)
3. Whether it is in golden supporting facts setting or not
4. Public repository of your model
5. Reference to your publication

Finally, please make sure that you are reporting the results on the dev set of R4C corpus ;)

We look forward to your results!


# Citation

## Latex code for R4C logo

```
\DeclareMathAlphabet\mathbfcal{OMS}{cmsy}{b}{n}
$\mathbfcal{R}^4\mathbfcal{C}$
```

## Papers
1. Naoya Inoue, Pontus Stenetorp and Kentaro Inui. R4C: A Benchmark for Evaluating RC Systems to Get the Right Answer for the Right Reason. In <i>Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL2020)</i>, July 2020, to appear.


## Author
[Naoya Inoue](https://naoya-i.github.io)