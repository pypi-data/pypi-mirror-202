"""
Contains tests for LinearRegression, BinaryLogisticRegression as well as TwiceDifferentiable modules and
its associated gradient and matrix vector product calculations. Note that there is no test for the neural network
module.
"""

import itertools
from typing import List, Tuple

import numpy as np
import pytest

from pydvl.utils import (
    linear_regression_analytical_derivative_d2_theta,
    linear_regression_analytical_derivative_d_theta,
    linear_regression_analytical_derivative_d_x_d_theta,
)

try:
    import torch.nn.functional as F

    from pydvl.influence.frameworks import TorchTwiceDifferentiable
    from pydvl.influence.model_wrappers import TorchLinearRegression
except ImportError:
    pass


class ModelTestSettings:
    DATA_OUTPUT_NOISE: float = 0.01
    ACCEPTABLE_ABS_TOL_MODEL: float = (
        0.04  # TODO: Reduce bound if tests are running with fixed seeds.
    )
    ACCEPTABLE_ABS_TOL_DERIVATIVE: float = 1e-5

    TEST_CONDITION_NUMBERS: List[int] = [5]
    TEST_SET_SIZE: List[int] = [20]
    TRAINING_SET_SIZE: List[int] = [500]
    PROBLEM_DIMENSIONS: List[Tuple[int, int]] = [
        (2, 2),
        (5, 10),
        (10, 5),
        (10, 10),
    ]


test_cases_linear_regression_fit = list(
    itertools.product(
        ModelTestSettings.TRAINING_SET_SIZE,
        ModelTestSettings.TEST_SET_SIZE,
        ModelTestSettings.PROBLEM_DIMENSIONS,
        ModelTestSettings.TEST_CONDITION_NUMBERS,
    )
)

test_cases_logistic_regression_fit = list(
    itertools.product(
        ModelTestSettings.TRAINING_SET_SIZE,
        ModelTestSettings.TEST_SET_SIZE,
        [(1, 3), (1, 7), (1, 20)],
        ModelTestSettings.TEST_CONDITION_NUMBERS,
    )
)

test_cases_linear_regression_derivatives = list(
    itertools.product(
        ModelTestSettings.TRAINING_SET_SIZE,
        ModelTestSettings.PROBLEM_DIMENSIONS,
        ModelTestSettings.TEST_CONDITION_NUMBERS,
    )
)


def lmb_fit_test_case_to_str(packed_i_test_case):
    i, test_case = packed_i_test_case
    return f"Problem #{i} of dimension {test_case[2]} with train size {test_case[0]}, test size {test_case[1]} and condition number {test_case[3]}"


def lmb_correctness_test_case_to_str(packed_i_test_case):
    i, test_case = packed_i_test_case
    return f"Problem #{i} of dimension {test_case[1]} with train size {test_case[0]} and condition number {test_case[2]}"


fit_test_case_ids = list(
    map(
        lmb_fit_test_case_to_str,
        zip(
            range(len(test_cases_linear_regression_fit)),
            test_cases_linear_regression_fit,
        ),
    )
)
correctness_test_case_ids = list(
    map(
        lmb_correctness_test_case_to_str,
        zip(
            range(len(test_cases_linear_regression_derivatives)),
            test_cases_linear_regression_derivatives,
        ),
    )
)


@pytest.mark.torch
@pytest.mark.parametrize(
    "train_set_size,problem_dimension,condition_number",
    test_cases_linear_regression_derivatives,
    ids=correctness_test_case_ids,
)
def test_linear_regression_model_grad(
    train_set_size: int,
    condition_number: float,
    linear_model: Tuple[np.ndarray, np.ndarray],
):
    # some settings
    A, b = linear_model
    output_dimension, input_dimension = tuple(A.shape)

    # generate datasets
    data_model = lambda x: np.random.normal(
        x @ A.T + b, ModelTestSettings.DATA_OUTPUT_NOISE
    )
    train_x = np.random.uniform(size=[train_set_size, input_dimension])
    train_y = data_model(train_x)

    model = TorchLinearRegression(input_dimension, output_dimension, init=linear_model)
    loss = F.mse_loss
    mvp_model = TorchTwiceDifferentiable(model=model, loss=loss)

    train_grads_analytical = 2 * linear_regression_analytical_derivative_d_theta(
        (A, b), train_x, train_y
    )
    train_grads_autograd = mvp_model.split_grad(train_x, train_y)
    train_grads_max_diff = np.max(np.abs(train_grads_analytical - train_grads_autograd))
    assert (
        train_grads_max_diff < ModelTestSettings.ACCEPTABLE_ABS_TOL_DERIVATIVE
    ), "training set produces wrong gradients."


@pytest.mark.torch
@pytest.mark.parametrize(
    "train_set_size,problem_dimension,condition_number",
    test_cases_linear_regression_derivatives,
    ids=correctness_test_case_ids,
)
def test_linear_regression_model_hessian(
    train_set_size: int,
    condition_number: float,
    linear_model: Tuple[np.ndarray, np.ndarray],
):
    # some settings
    A, b = linear_model
    output_dimension, input_dimension = tuple(A.shape)

    # generate datasets
    data_model = lambda x: np.random.normal(
        x @ A.T + b, ModelTestSettings.DATA_OUTPUT_NOISE
    )
    train_x = np.random.uniform(size=[train_set_size, input_dimension])
    train_y = data_model(train_x)
    model = TorchLinearRegression(input_dimension, output_dimension, init=linear_model)
    loss = F.mse_loss
    mvp_model = TorchTwiceDifferentiable(model=model, loss=loss)

    test_hessian_analytical = 2 * linear_regression_analytical_derivative_d2_theta(
        (A, b), train_x, train_y
    )
    grad_xy, _ = mvp_model.grad(train_x, train_y)
    estimated_hessian = mvp_model.mvp(
        grad_xy, np.eye((input_dimension + 1) * output_dimension)
    )
    test_hessian_max_diff = np.max(np.abs(test_hessian_analytical - estimated_hessian))
    assert (
        test_hessian_max_diff < ModelTestSettings.ACCEPTABLE_ABS_TOL_DERIVATIVE
    ), "Hessian was wrong."


@pytest.mark.torch
@pytest.mark.parametrize(
    "train_set_size,problem_dimension,condition_number",
    test_cases_linear_regression_derivatives,
    ids=correctness_test_case_ids,
)
def test_linear_regression_model_d_x_d_theta(
    train_set_size: int,
    condition_number: float,
    linear_model: Tuple[np.ndarray, np.ndarray],
):
    # some settings
    A, b = linear_model
    output_dimension, input_dimension = tuple(A.shape)

    # generate datasets
    data_model = lambda x: np.random.normal(
        x @ A.T + b, ModelTestSettings.DATA_OUTPUT_NOISE
    )
    train_x = np.random.uniform(size=[train_set_size, input_dimension])
    train_y = data_model(train_x)
    model = TorchLinearRegression(input_dimension, output_dimension, init=(A, b))
    loss = F.mse_loss
    mvp_model = TorchTwiceDifferentiable(model=model, loss=loss)

    test_derivative = 2 * linear_regression_analytical_derivative_d_x_d_theta(
        (A, b),
        train_x,
        train_y,
    )
    model_mvp = []
    for i in range(len(train_x)):
        grad_xy, tensor_x = mvp_model.grad(train_x[i], train_y[i])
        model_mvp.append(
            mvp_model.mvp(
                grad_xy,
                np.eye((input_dimension + 1) * output_dimension),
                backprop_on=tensor_x,
            )
        )
    estimated_derivative = np.stack(model_mvp, axis=0)
    test_hessian_max_diff = np.max(np.abs(test_derivative - estimated_derivative))
    assert (
        test_hessian_max_diff < ModelTestSettings.ACCEPTABLE_ABS_TOL_DERIVATIVE
    ), "Hessian was wrong."
