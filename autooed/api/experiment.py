import json

import numpy as np
from flask import Blueprint, request

from autooed.mobo import build_algorithm
from autooed.problem.common import build_problem
from autooed.utils.initialization import generate_random_initial_samples

exp_bp = Blueprint('exp', __name__)


@exp_bp.route('/exp')
def get_exp():
    return {'code': 0, 'data': [], 'message': ""}


@exp_bp.route('/exp/create', methods=['POST'])
def create_exp():
    if request.method == 'POST':
        data_json = request.get_json()
        data_dict = dict(data_json)
        print(data_dict)
        # build problem
        problem = build_problem(data_dict.get("problemName"))
        print(problem)
        problem_cfg = problem.get_config()

        # build algorithm
        algorithm = build_algorithm(data_dict.get("algorithmName"), problem, data_dict)

        # generate initial random samples
        X = generate_random_initial_samples(problem, data_dict.get('n_init_sample'))
        Y = np.array([problem.evaluate_objective(x) for x in X])

        # optimization
        n_total_sample = 100
        # while len(X) < n_total_sample:
        #     # propose design samples
        #     X_next = algorithm.optimize(X, Y, None, 10)
        #
        #     # evaluate proposed samples
        #     Y_next = np.array([problem.evaluate_objective(x) for x in X_next])
        #
        #     # combine into dataset
        #     X = np.vstack([X, X_next])
        #     Y = np.vstack([Y, Y_next])
        #
        #     print(f'{len(X)}/{n_total_sample} complete')
        data = {
            "code": 0,
            "data": {
                "x": X.tolist(),
                "y": Y.tolist()
            }
        }
        return json.dumps(data)
    else:
        return '404'
