"""Yoyodyne models."""

import argparse

from .. import defaults
from .base import BaseEncoderDecoder
from .hard_attention import HardAttentionLSTM
from .lstm import AttentiveLSTMEncoderDecoder, LSTMEncoderDecoder
from .pointer_generator import (
    PointerGeneratorLSTMEncoderDecoder,
    PointerGeneratorTransformerEncoderDecoder,
)
from .transducer import TransducerEncoderDecoder
from .transformer import TransformerEncoderDecoder

_model_fac = {
    "attentive_lstm": AttentiveLSTMEncoderDecoder,
    "hard_attention_lstm": HardAttentionLSTM,
    "lstm": LSTMEncoderDecoder,
    "pointer_generator_lstm": PointerGeneratorLSTMEncoderDecoder,
    "pointer_generator_transformer": PointerGeneratorTransformerEncoderDecoder,  # noqa: 501
    "transducer": TransducerEncoderDecoder,
    "transformer": TransformerEncoderDecoder,
}


def get_model_cls(arch: str) -> BaseEncoderDecoder:
    """Model factory.

    Args:
        arch (str).
        has_features (bool).

    Raises:
        NotImplementedError: Architecture not found.

    Returns:
        BaseEncoderDecoder.
    """
    try:
        return _model_fac[arch]
    except KeyError:
        raise NotImplementedError(f"Architecture {arch} not found")


def get_model_cls_from_argparse_args(
    args: argparse.Namespace,
) -> BaseEncoderDecoder:
    """Creates a model from CLI arguments.

    Args:
        args (argparse.Namespace).

    Returns:
        BaseEncoderDecoder.
    """
    return get_model_cls(args.arch)


def add_argparse_args(parser: argparse.ArgumentParser) -> None:
    """Adds model options to an argument parser.

    We only add the ones needed to look up the model class itself, with
    more specific arguments specified in train.py.

    Args:
        parser (argparse.ArgumentParser).
    """
    parser.add_argument(
        "--arch",
        choices=_model_fac.keys(),
        default="attentive_lstm",
        help="Model architecture. Default: %(default)s.",
    )
    parser.add_argument(
        "--tie_embeddings",
        action="store_true",
        default=defaults.TIE_EMBEDDINGS,
        help="Shares embeddings for the source and target vocabularies. "
        "Always enable this with pointer-generator and transducer "
        "architectures. Default: enabled.",
    )
    parser.add_argument(
        "--no_tie_embeddings",
        action="store_false",
        dest="tie_embeddings",
    )
