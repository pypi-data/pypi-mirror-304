import numpy as np


class ReLU:
    def __call__(self, z):
        return np.maximum(0, z)

    @staticmethod
    def derivative(z):
        derivative = np.ones_like(z)
        derivative[z <= 0] = 0
        return derivative


class Sigmoid:
    def __call__(self, z):
        return 1 / (1 + np.exp(-z))

    @staticmethod
    def derivative(z):
        sigmoid = 1 / (1 + np.exp(-z))
        return sigmoid * (1 - sigmoid)


class Tanh:
    def __call__(self, z):
        return np.tanh(z)

    @staticmethod
    def derivative(z):
        return 1 - np.tanh(z) ** 2


class Softmax:
    def __call__(self, z):
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    @staticmethod
    def derivative(z):
        s = Softmax()(z)
        jacobian = np.zeros((z.shape[0], z.shape[1], z.shape[1]))
        for i in range(z.shape[0]):
            for j in range(z.shape[1]):
                for k in range(z.shape[1]):
                    if j == k:
                        jacobian[i, j, k] = s[i, j] * (1 - s[i, j])
                    else:
                        jacobian[i, j, k] = -s[i, j] * s[i, k]
        return jacobian
