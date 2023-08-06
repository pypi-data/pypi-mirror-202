# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""A Quantum Neural Network for jax"""

from .neural_network import NeuralNetwork
import jax
import jax.numpy as jnp
import numpy as np


class QNNJax(NeuralNetwork):

    def __init__(
        self,
        circuit,
        num_inputs,
        num_weights,
        output_shape,
    ) -> None:

        super().__init__(
            num_inputs=num_inputs,
            num_weights=num_weights,
            sparse=False,
            output_shape=output_shape,
            input_gradients=True,
        )

        self.circuit = circuit

    def _forward(
        self,
        inputs,
        weights,
    ):

        inputs = jnp.array(inputs)
        weights = jnp.array(weights)

        output_data = jax.vmap(self.circuit, (0, None))(
            inputs, weights)

        return np.array(output_data)

    def _backward(
        self,
        inputs,
        weights,
    ):

        inputs = jnp.array(inputs)
        weights = jnp.array(weights)

        grad_f = jax.vmap(jax.jacobian(self.circuit, (0, 1)), (0, None))
        inputs_grad, weights_grad = grad_f(inputs, weights)

        if not self._input_gradients:
            return None, np.array(weights_grad)

        return np.array(inputs_grad), np.array(weights_grad)
