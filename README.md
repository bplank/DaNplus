# DaN+ (DaNplus): Danish Nested Named Entities and Lexical Normalization

This repository contains the code to reproduce the results of Plank, Nørgaard Jensen, van der Goot, 2020 (COLING) on Nested NER and Lexical Normalization for Danish: [DaN+](https://www.aclweb.org/anthology/2020.coling-main.583/). In this repository you'll find:

* `configs`: configuration files for MaChAmp
* `data`: the data used in our paper
* `predictions`: the predictions for all experiments
* `scripts`: the code to reproduce all experiments. Look at scripts/runAll.sh on all commands necessary to rerun. Scripts/genAll.sh can be used to generate all tables/graphs used in the paper

Additionally, these scripts will download the following folders:

* `monoise`: MoNoise is a state-of-the-art lexical normalization model (van der Goot, 2019)
* `mtp`: Contains MaChAmp, a bert-based sequence labeler (van der Goot et al., 2020)

# References

If you use the code, data, guidelines from DaN+, please include the following two citations:

```
@inproceedings{plank-etal-2020-dan,
    title = "{D}a{N}+: {D}anish Nested Named Entities and Lexical Normalization",
    author = "Plank, Barbara  and
      Jensen, Kristian N{\o}rgaard  and
      van der Goot, Rob",
    booktitle = "Proceedings of the 28th International Conference on Computational Linguistics",
    month = dec,
    year = "2020",
    address = "Barcelona, Spain (Online)",
    publisher = "International Committee on Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.coling-main.583",
    pages = "6649--6662"
}

```
```
@misc{goot2020massive,
    title={Massive Choice, Ample Tasks (MaChAmp): A Toolkit for Multi-task Learning in NLP},
    author={Rob van der Goot and Ahmet Üstün and Alan Ramponi and Barbara Plank},
    year={2020},
    eprint={2005.14672},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```




