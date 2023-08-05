from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

import torch
from torch import nn
from torch.utils.data import DataLoader
from tqdm import tqdm


def recalculate_batch_norms(
        model: nn.Module,
        dataloader: DataLoader[Any],
        input_indices: int | Sequence[int],
        device: torch.device | str | None,
        verbose: bool,
        *forward_args: Any,
        **forward_kwargs: Any
) -> None:
    """
    Recalculate the BatchNorm statistics of a model.

    Use this after permuting the model, but only if the model contains
    a BatchNorm.

    Args:
        model:
            The model.
        dataloader:
            The DataLoader to use for recalculating the statistics.
            Should ideally be the training DataLoader.
        input_indices:
            Many DataLoaders return several inputs and labels.
            These can sometimes be used in unexpected ways.
            To make sure that the correct outputs of the dataloader are used
            as inputs to the model's forward pass, you can specify the indices
            at which the inputs are located, in the order that they should be
            passed to the model.
        device:
            The device on which to run the model.
        verbose:
            Whether to print progress.
        *forward_args:
            Any additional positional arguments to pass to the model's forward  pass.
        **forward_kwargs:
            Any additional keyword arguments to pass to the model's forward pass.
    """
    if verbose:
        print("Recalculating BatchNorm statistics...")
    types = [type(m) for m in model.modules()]
    if (
            nn.BatchNorm1d not in types
            and nn.BatchNorm2d not in types
            and nn.BatchNorm3d not in types
    ):
        if verbose:
            print("No BatchNorm layers found in model.")
        return

    training = model.training
    model.train()

    # Reset the running mean and variance
    for module in model.modules():
        if (
                not isinstance(module, (nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d))
                or not hasattr(module, "running_mean")
                or not hasattr(module, "running_var")
                or module.running_mean is None
                or module.running_var is None
        ):
            continue

        model.running_mean = torch.zeros_like(module.running_mean)
        model.running_var = torch.zeros_like(module.running_var)

    # Recalculate the running mean and variance
    for batch in tqdm(dataloader, disable=not verbose):
        if isinstance(batch, Sequence):
            inputs, _ = get_inputs_labels(batch, input_indices, 0, device)
        else:
            inputs = [batch]
        model(*inputs, *forward_args, **forward_kwargs)

    if not training:
        model.eval()


def get_inputs_labels(
        batch: Any,
        input_indices: int | Sequence[int] = 0,
        label_indices: int | Sequence[int] = 1,
        device: torch.device | str | int | None = None
) -> tuple[list[Any], list[Any]]:
    """
    Get the inputs and outputs from a batch.

    Args:
        batch:
            The batch.
        input_indices:
            Many DataLoaders return several inputs and labels per batch.
            These can sometimes be used in unexpected ways.
            To make sure that the correct outputs of the dataloader are used
            as inputs to the model's forward pass, you can specify the indices
            at which the inputs are located, in the order that they should be
            passed to the model.
        label_indices:
            Like `input_indices`, but for the labels.
        device:
            The device on which to run the model.

    Returns:
        The inputs and labels.
    """
    if isinstance(input_indices, int):
        input_indices = [input_indices]
    if isinstance(label_indices, int):
        label_indices = [label_indices]

    inputs = (
        [batch[i].to(device) for i in input_indices]
        if device is not None
        else [batch[i] for i in input_indices]
    )
    labels = (
        [batch[i].to(device) for i in label_indices]
        if device is not None
        else [batch[i] for i in label_indices]
    )
    return inputs, labels


def contains_parameter(
        parameters: Sequence[nn.Parameter] | Iterator[nn.Parameter],
        parameter: nn.Parameter
) -> bool:
    """
    Check if a sequence of parameters contains a parameter.

    This cannot be done via the normal `in` operator, because
    `nn.Parameter`'s `__eq__` does not work for parameters of different shapes.

    Args:
        parameters:
            The sequence of parameters.
        parameter:
            The parameter.

    Returns:
        Whether the sequence contains the parameter.
    """
    return any(param is parameter for param in parameters)
