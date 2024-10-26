import warnings

from .initializers import (
    ones,
    zeros,
    gramschmidt,
    identity,
    randn,
    rand_unitary
)
from .embeddings import (
    Embedding,
    trigonometric,
    fourier,
    linear_complement_map,
    gaussian_rbf,
    jax_arrays,
    add_ones,
    embed
)

from .metrics import (
    neg_log_likelihood,
    transformed_squared_norm,
    no_reg,
    reg_log_norm,
    reg_log_norm_relu,
    reg_norm_quad,
    error_logquad,
    error_quad,
    softmax,
    MSE,
    loss_wrapper_optax,
    combined_loss
)

from .strategy import (
    Strategy,
    Sweeps,
    Global
)

from .util import (
    gramschmidt_row,
    gramschmidt_col,
    return_digits,
    zigzag_order,
    integer_to_one_hot
)