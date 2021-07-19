from enum import IntEnum
from typing import Any
from mesa import Model, Agent
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import BaseScheduler, RandomActivation
import numpy as np
from scipy import spatial

from utils_for_corona_model import Policy, HealthStatus, generate_socio, generate_age, logistic_prob, mask_protection, \
    Queue, prob_recovery, prob_during_ill, prob_distance


def count_ills(model):
    only_people_agents = [people_agent for people_agent in model.schedule.agents
                          if type(people_agent) == PeopleAgent]
    return len([k for k in only_people_agents if k.health == HealthStatus.ILL])


def count_from_outside_ills(model):
    return len([k for k in [people_agent for people_agent in model.schedule.agents
                            if type(people_agent) == PeopleAgent] if k.health == HealthStatus.ILL and k.import_ and
                k.active])


def count_teish(model):
    return len([k for k in [people_agent for people_agent in model.schedule.agents
                            if type(people_agent) == PeopleAgent] if k.health == HealthStatus.TEISH])


def count_recovering(model):
    return len([k for k in [people_agent for people_agent in model.schedule.agents
                            if type(people_agent) == PeopleAgent] if k.health == HealthStatus.RECOVERING])


class PoliceAgent(Agent):
    def __init__(self, unique_id: int, model: Model):
        super().__init__(unique_id, model)
        # self.initial_position = 0
        self.health = HealthStatus.HEALTHY

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True,
                                                          include_center=True,
                                                          radius=1)
        new_position = self.random.choice([pos for pos in possible_steps])
        self.model.grid.move_agent(self, new_position)

    def step(self) -> None:
        self.move()


class PeopleAgent(Agent):
    def __init__(self, unique_id: int, model: Model, health: HealthStatus):
        super().__init__(unique_id, model)
        self.health = health
        self.age = generate_age()
        self.socioeconomic = generate_socio()
        self.social_influence = 0
        self.mask = False
        self.active = True
        self.import_ = False

    def move(self, policeman, crowded):
        threshold = logistic_prob(self.model.move_coeff, [self.age / 100, -self.health / HealthStatus.TEISH,
                                                          self.socioeconomic,
                                                          self.model.policy / Policy.CLOSURE,
                                                          min(policeman, 1), self.social_influence,
                                                          -crowded / 10,
                                                          ])
        # Change distance according the situation
        distance = np.random.geometric(prob_distance(self.age, threshold))
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True,
                                                          include_center=True,
                                                          radius=distance)
        new_position = self.random.choice([pos for pos in possible_steps])
        # Random moving
        self.model.grid.move_agent(self, new_position)

    def contagious(self, cellmates):
        if self.health == HealthStatus.ILL:
            for p in cellmates:
                # if p.health == HealthStatus.HEALTHY and type(p) == PeopleAgent:
                if np.random.random() < mask_protection(self.mask, p.mask,
                                                        protection_level=self.model.influence_rate):
                    p.health = HealthStatus.ILL
                    p.time_infection = self.model.time

    def update_influence(self, cellmates):
        wearing_mask = [c for c in cellmates if c.mask]
        if len(wearing_mask) < 0.5 * len(cellmates):
            self.social_influence = 1 * self.model.socio_inf
        else:
            self.social_influence = -1 * self.model.socio_inf

    def wear_mask(self, crowded, policeman):
        threshold = logistic_prob(self.model.mask_coeff,
                                  [self.age / 100, self.health / HealthStatus.TEISH,
                                   self.socioeconomic,
                                   self.model.policy / Policy.CLOSURE,
                                   min(policeman, 1), self.social_influence,
                                   crowded / 10,
                                   ])
        # print('mask:', threshold)
        if np.random.random() < threshold:
            self.mask = True
        else:
            self.mask = False

    def self_change_health(self):
        if self.health != HealthStatus.ILL:
            return
        chance_to_recovery = prob_recovery(self.age) * prob_during_ill(self.age, HealthStatus.RECOVERING)
        chance_to_other = (1 - prob_recovery(self.age)) * prob_during_ill(self.age, HealthStatus.TEISH)

        change = np.random.random()
        if change < chance_to_recovery:
            self.health = HealthStatus.RECOVERING
        elif change < chance_to_recovery + chance_to_other:
            self.health = HealthStatus.TEISH

    def travel_agent(self):
        # return True
        if self.active:
            if np.random.random() < self.model.agent_turnover_rate:
                self.active = False
        else:
            if np.random.random() < np.random.normal(0.2, 0.1):
                self.active = True
                if np.random.random() < self.model.disease_importing:
                    self.health = HealthStatus.ILL
                    self.import_ = True
        return self.active

    def get_environment_data(self, radius=5):
        cellmates = self.model.grid.get_cell_list_contents(self.model.grid.get_neighborhood(self.pos, moore=True,
                                                                                            include_center=True,
                                                                                            radius=radius))
        close_policeman = sum([1 for c in cellmates
                               if spatial.distance.euclidean(c.pos, self.pos) <= 3 and
                               type(c) == PoliceAgent])
        return cellmates, close_policeman

    def step(self) -> None:
        if self.model.policy < Policy.PARTIAL_CLOSURE:
            active = self.travel_agent()
        else:
            active = self.active
        if not active or self.health == HealthStatus.TEISH:
            return
        # Before move
        cellmates, close_policeman = self.get_environment_data(radius=3)
        self.move(close_policeman, len(cellmates) - close_policeman)
        # After moving
        cellmates, close_policeman = self.get_environment_data(radius=5)
        crowd = len(cellmates) - close_policeman
        optional_to_be_infection = [c for c in cellmates
                                    if spatial.distance.euclidean(c.pos, self.pos) <= 2 and
                                    type(c) == PeopleAgent and c.health == HealthStatus.HEALTHY]

        self.wear_mask(crowded=crowd, policeman=close_policeman)
        self.contagious(optional_to_be_infection)
        self.self_change_health()


# self.model.police_deterrence
class CoronaModel(Model):
    def __init__(self, N=100, width=30, height=30, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.num_agents = N
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.time = 0

        self.influence_rate = kwargs['infRate']
        self.mask_coeff = kwargs['mask_coeff']
        self.move_coeff = kwargs['mask_coeff']
        self.goverment_policy_coeff = kwargs['government_policy_coeff']
        self.agent_turnover_rate = 0.005
        self.disease_importing = kwargs['disease_importing']

        self.save_seven_days_before = Queue(kwargs['R_mean'])
        self.policy = Policy.OPEN
        self.R = 0
        self.economic_status = 100
        self.cops_num = int(kwargs['enforcement_level'] * self.num_agents)

        self.datacollector_1 = DataCollector(
            model_reporters={"Ills": count_ills},
            agent_reporters={"Health": "health"})

        self.datacollector_2 = DataCollector(
            model_reporters={"Teish": count_teish},
            agent_reporters={"Health": "health"})

        self.datacollector_3 = DataCollector(
            model_reporters={"RECOVERING": count_recovering},
            agent_reporters={"Health": "health"})

        self.datacollector_4 = DataCollector(
            model_reporters={"Ills_from_outside": count_from_outside_ills},
            agent_reporters={"Health": "health"})

        self.datacollector_5 = DataCollector(
            model_reporters={"R": self.get_current_R},
            agent_reporters={"Health": "health"})

        self.datacollector_6 = DataCollector(
            model_reporters={"Policy": self.get_current_policy},
            agent_reporters={"Health": "health"})

        # EXPERT VERSION
        # if len(kwargs) > 0:
        #
        #     self.disease_importing = kwargs['disease_importing']
        #     self.number_of_hospital_beds = kwargs['disease_importing']
        #     self.cop_area = width / kwargs['number_of_cops']

        # SIMPLE VERSION
        # else:
        #     self.agent_turnover_rate = -1
        #     self.disease_importing = -1
        #     self.number_of_hospital_beds = -1
        #     self.cop_max_dist = -1

        for i in range(self.num_agents):
            a = PeopleAgent(i, self, HealthStatus.HEALTHY)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.height)
            y = self.random.randrange(self.grid.width)
            self.grid.place_agent(a, (x, y))
        for i in range(self.num_agents, self.num_agents + self.cops_num):
            a = PoliceAgent(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.height)
            y = self.random.randrange(self.grid.width)
            self.grid.place_agent(a, (x, y))

    def get_current_policy(self):
        return self.policy

    def get_current_R(self):
        return self.R

    def cal_R(self):
        if len(self.save_seven_days_before.queue) > 0:
            if self.save_seven_days_before.queue[0] > 0:
                self.R = count_ills(self) / self.save_seven_days_before.queue[0]

    def update_policy(self):
        threshold = logistic_prob(self.goverment_policy_coeff, [count_ills(self) / self.num_agents,
                                                                self.R, self.economic_status / 100])
        if threshold < 0.2:
            self.policy = Policy.OPEN
        elif threshold < 0.4:
            self.policy = Policy.MASK_AND_DISTANCE
        elif threshold < 0.7:
            self.policy = Policy.PARTIAL_CLOSURE
        else:
            self.policy = Policy.CLOSURE

    def step(self) -> None:
        self.time += 1
        self.schedule.step()
        self.save_seven_days_before.insert(count_ills(self))
        self.cal_R()
        self.update_policy()
        self.datacollector_1.collect(self)
        self.datacollector_2.collect(self)
        self.datacollector_3.collect(self)
        self.datacollector_4.collect(self)
        self.datacollector_5.collect(self)
        self.datacollector_6.collect(self)
