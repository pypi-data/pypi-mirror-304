<p align="center"><img width="70%" src="https://github.com/jimouris/curl/blob/main/Curl.png" alt="Curl logo" /></p>

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/jimouris/curl/blob/main/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/jimouris/curl/blob/main/CONTRIBUTING.md)
--------------------------------------------------------------------------------

Curl is a framework for Privacy Preserving Machine Learning (PPML) that builds on top of [CrypTen](https://github.com/facebookresearch/CrypTen) and [PyTorch](https://github.com/pytorch/pytorch).
CrypTen relies on expensive polynomial approximations for evaluating non linear functions such as logarithm, square root, etc.
In contrast, Curl uses lookup tables (LUTs) encoded with Discrete Wavelet Transforms (DWT) to approximate non-linearities that result in faster evaluation while achieving better approximations.

This way, in Curl we are able to evaluate Large Language Models (LLMs) such as GPT-2, GPT Neo, BERT (tiny, base, large).
Curl's goal and model is similar to CrypTen:

> Its goal is to make secure computing techniques accessible to Machine Learning practitioners.
> It currently implements [Secure Multiparty Computation](https://en.wikipedia.org/wiki/Secure_multi-party_computation)
> as its secure computing backend and offers three main benefits to ML researchers:
>
> 1. It is machine learning first. The framework presents the protocols via a `CrypTensor`
>    object that looks and feels exactly like a PyTorch `Tensor`. This allows the user to use
>    automatic differentiation and neural network modules akin to those in PyTorch.
>
> 2. CrypTen is library-based. It implements a tensor library just as PyTorch does.
>    This makes it easier for practitioners to debug, experiment on, and explore ML models.
>
> 3. The framework is built with real-world challenges in mind. CrypTen does not scale back or
>    oversimplify the implementation of the secure protocols.


## How to cite this work
Curl will appear in the proceedings of the Conference on Applied Machine Learning in Information Security (CAMLIS) 2024.
The preprint can be accessed [here](https://eprint.iacr.org/2024/1127); you can cite this work as follows:
Curl will appear in the proceedings of the Conference on Applied Machine Learning in Information Security (CAMLIS) 2024.
The preprint can be accessed [here](https://eprint.iacr.org/2024/1127); you can cite this work as follows:
```bibtex
@InProceedings{CAMLIS:SMUJRSV24,
  author =      "Manuel B. Santos and
                 Dimitris Mouris and
                 Mehmet Ugurbil and
                 Stanislaw Jarecki and
                 José Reis and
                 Shubho Sengupta and
                 Miguel de Vega",
  title =       "{Curl: Private LLMs through Wavelet-Encoded Look-Up Tables}",
  pages =       {1--31},
  booktitle =   {Proceedings of the Conference on Applied Machine Learning in Information Security},
  address =     {Arlington, Virginia, USA},
  month =       {October 24--25,},
  year =        2024,
}
```

The original CrypTen paper can be accessed [here](https://arxiv.org/pdf/2109.00984.pdf) (documented [here](https://crypten.readthedocs.io/en/latest/)); you can cite this work as follows:
```bibtex
@inproceedings{crypten2020,
  author={B. Knott and S. Venkataraman and A.Y. Hannun and S. Sengupta and M. Ibrahim and L.J.P. van der Maaten},
  title={CrypTen: Secure Multi-Party Computation Meets Machine Learning},
  booktitle={arXiv 2109.00984},
  year={2021},
}
```


## Installing AIVM

In order to install AIVM, you can use Poetry or Pip but Poetry is the recommended way.

To install with `pip` do:
```shell
cd aivm/
pip install .
```

or 

```shell
cd aivm
pip install poetry
pip install .
```

## Running the Project

For detailed instructions on running the project in various environments (Local, AWS, Docker Local, Docker Compose), check the [README](./aivm/README.md).

To quickly run the core components, use:

```shell
docker compose up --build coordinator node ttp client
```

## Examples

CrypTen has a series of tutorial built on Jupyter notebooks in the [tutorials directory](./tutorials/) as well as examples in the [examples directory](./examples/).

We extend these with our LLM applications in the [LLMs directory](./examples/llms/), which you can run as:
```shell
❯❯ python examples/llms/launcher.py --world_size 2 --tensor_size 1,10 --multiprocess --model GPT2
```

To see the full list of arguments and LLMs available run the script with the `--help` flag:
```shell
❯❯ python examples/llms/launcher.py --help
```

## Disclaimer
This is software for a research prototype and not production-ready code.
This repository builds upon [CrypTen](https://github.com/facebookresearch/CrypTen) and [PyTorch](https://github.com/pytorch/pytorch).
