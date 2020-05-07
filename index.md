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
The R4C dataset is built on top of [HotpotQA](https://hotpotqa.github.io/).

# Download

- [This repository](https://github.com/naoya-i/r4c) contains the R4C corpus and the official evaluation script.
- Question-answer pairs are in [HotpotQA](https://hotpotqa.github.io/) dataset.


# Leaderboard

## Full prediction setting

|Model|Entity|Relation|Full|Date|
|-|-|-|-|-|
| Human [1]           | 83.4/81.1/81.4 | 72.3/69.4/70.0 | 77.7/75.1/75.6 | May 2020 |


## Golden supporting facts setting

|Model|Entity|Relation|Full|Date|
|-|-|-|-|-|
| Human [1]           | 83.4/81.1/81.4 | 72.3/69.4/70.0 | 77.7/75.1/75.6 | May 2020 |
| Baseline (CORE) [1] | 66.4/60.1/62.1 | 51.0/46.0/47.5 | 59.4/53.6/55.4 | May 2020 |
| Baseline (IE) [1]   | 11.3/53.4/16.6 | 13.7/62.8/19.9 | 11.4/52.3/16.5 | May 2020 |


## Model references

1. Naoya Inoue, Pontus Stenetorp and Kentaro Inui. R4C: A Benchmark for Evaluating RC Systems to Get the Right Answer for the Right Reason. In <i>Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL2020)</i>, July 2020, to appear.  [Prediction](https://github.com/naoya-i/r4c/blob/master/prediction/)
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

## Papers

If you use our dataset in your paper, please cite the following paper:

1. Naoya Inoue, Pontus Stenetorp and Kentaro Inui. R4C: A Benchmark for Evaluating RC Systems to Get the Right Answer for the Right Reason. In <i>Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL2020)</i>, July 2020, to appear. [preprint](https://arxiv.org/abs/1910.04601)


## bib

```
@inproceedings{inoue-etal-2020-r4c,
    title = "R4C: A Benchmark for Evaluating RC Systems to Get the Right Answer for the Right Reason",
    author = "Inoue, Naoya  and
      Stenetorp, Pontus  and
      Inui, Kentaro",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    year = "2020",
    pages = "To appear"
}
```

## Latex code for R4C logo

```
\DeclareMathAlphabet\mathbfcal{OMS}{cmsy}{b}{n}
$\mathbfcal{R}^4\mathbfcal{C}$
```


# Author

[Naoya Inoue](https://naoya-i.github.io)


# Acknowledgements

This work was supported by the UCL-Tohoku University Strategic Partnership Fund, JSPS KAKENHI Grant Number 19K20332, JST CREST Grant Number JPMJCR1513 (including the AIP challenge program), the European Union's Horizon 2020 research and innovation programme under grant agreement No 875160, and the UK Defence Science and Technology Laboratory (Dstl) and Engineering and Physical Research Council (EPSRC) under grant EP/R018693/1 (a part of the collaboration between US DOD, UK MOD, and UK EPSRC under the Multidisciplinary University Research Initiative (MURI)).
