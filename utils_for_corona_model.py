from enum import IntEnum
import numpy as np


class Policy(IntEnum):
    OPEN = 0
    MASK_AND_DISTANCE = 1
    PARTIAL_CLOSURE = 2
    CLOSURE = 3


class HealthStatus(IntEnum):
    HEALTHY = 0
    ILL = 1
    TEISH = 2
    RECOVERING = -1
    IMMUNE = -2


def generate_socio():
    return max(min(np.random.normal(0.5, 0.1), 1), 0)


def generate_age():
    chance = np.random.random()
    if chance < 0.102:
        return int(np.random.random() * 5) + 0
    elif chance < 0.197:
        return int(np.random.random() * 5) + 5
    elif chance < 0.282:
        return int(np.random.random() * 5) + 10
    elif chance < 0.361:
        return int(np.random.random() * 5) + 15
    elif chance < 0.433:
        return int(np.random.random() * 5) + 20
    elif chance < 0.501:
        return int(np.random.random() * 5) + 25
    elif chance < 0.567:
        return int(np.random.random() * 5) + 30
    elif chance < 0.631:
        return int(np.random.random() * 5) + 35
    elif chance < 0.693:
        return int(np.random.random() * 5) + 40
    elif chance < 0.749:
        return int(np.random.random() * 5) + 45
    elif chance < 0.796:
        return int(np.random.random() * 5) + 50
    elif chance < 0.84:
        return int(np.random.random() * 5) + 55
    elif chance < 0.882:
        return int(np.random.random() * 5) + 60
    elif chance < 0.921:
        return int(np.random.random() * 5) + 65
    elif chance < 0.952:
        return int(np.random.random() * 5) + 70
    elif chance < 0.97:
        return int(np.random.random() * 5) + 75
    elif chance < 0.985:
        return int(np.random.random() * 5) + 80
    elif chance < 0.994:
        return int(np.random.random() * 5) + 85
    else:
        return int(np.random.random() * 5) + 90


def logistic_prob(factors=None, variables=None):
    if factors is None or variables is None:
        return 0
    norm = sum([f for f in factors])
    exponent = (sum([f / norm * v for f, v in zip(factors, variables)]) - 1) / 0.1
    return 1 / (1 + np.exp(-exponent))


def mask_protection(a: bool, b: bool, protection_level=None):
    if protection_level is None:
        protection_level = [0.1, 0.2, 0.3, 0.8]
    if a and b:
        return protection_level[0]
    elif a:
        return protection_level[1]
    elif b:
        return protection_level[2]
    else:
        return protection_level[3]


class Queue():
    def __init__(self, n: int):
        self.queue = []
        self.max_len = n

    def insert(self, x):
        self.queue.append(x)
        if len(self.queue) > self.max_len:
            self.queue.pop(0)


def prob_recovery(age: int):
    return 1 - 4.337 * 10 ** -6 * np.exp(0.1281 * age)
    # 1 - 4.337 * 10 ** -6 * np.exp(0.1281 * age)
    # 14.77 * 10 ** -5 * np.exp(11 * 10 ** -3 * age)


def prob_during_ill(age: int, end_status: HealthStatus):
    if end_status == HealthStatus.RECOVERING:
        if age < 20:
            return 1 / 12.3
        elif age < 30:
            return 1 / 14.4
        elif age < 40:
            return 1 / 14.6
        elif age < 50:
            return 1 / 14.9
        elif age < 60:
            return 1 / 15.6
        else:
            return 1 / 18.9
    else:
        if age < 30:
            return 1 / 21
        elif age < 40:
            return 1 / 20.5
        elif age < 50:
            return 1 / 25.5
        elif age < 60:
            return 1 / 23.5
        elif age < 70:
            return 1 / 20.6
        elif age < 80:
            return 1 / 18.1
        elif age < 90:
            return 1 / 15
        else:
            return 1 / 14.4


def prob_distance(age: int, t):
    sigma = 15
    mu = 30
    return 1 - 1 / (np.sqrt(2 * np.pi) * sigma) * np.exp(-(age - mu) ** 2 / (2 * sigma ** 2) + 3) * t
