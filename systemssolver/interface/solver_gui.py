import json
import os
import sys
from http import HTTPStatus

from flask import Flask, render_template, Response, request

from systemssolver.methods.factory import SolverMethods
from systemssolver.modeling.equation import EqualitySigns, Constraint
from systemssolver.modeling.objective import ObjectiveGoal, Objective
from systemssolver.modeling.parsing import ExpressionParser
from systemssolver.modeling.variables import Variable
from systemssolver.problem import Problem


class FlaskApp:

    def __init__(self, host='0.0.0.0', port=50000):
        if getattr(sys, 'frozen', False):
            template_folder = os.path.join(sys._MEIPASS, 'templates')
            static_folder = os.path.join(sys._MEIPASS, 'static')
            self.app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
        else:
            self.app = Flask(__name__)
        self.app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        self.app.config['TEMPLATES_AUTO_RELOAD'] = True
        self.host, self.port = host, port
        self.problem = Problem()
        self.parser = ExpressionParser()
        self.app.add_url_rule("/", "/", self.index)

        self.app.add_url_rule("/api/variables", "/api/variables", self.list_variables, methods=['GET'])
        self.app.add_url_rule("/api/variables/set", "/api/variables/set", self.set_variable, methods=['POST'])

        self.app.add_url_rule("/api/objective", "/api/objective", self.list_objectives, methods=['GET'])
        self.app.add_url_rule("/api/objective/add", "/api/objective/add", self.add_objective, methods=['POST'])
        self.app.add_url_rule("/api/objective/remove", "/api/objective/remove", self.remove_objective, methods=['POST'])

        self.app.add_url_rule("/api/constraint", "/api/constraint", self.list_constraints, methods=['GET'])
        self.app.add_url_rule("/api/constraint/add", "/api/constraint/add", self.add_constraint, methods=['POST'])
        self.app.add_url_rule("/api/constraint/remove", "/api/constraint/remove", self.remove_constraint,
                              methods=['POST'])
        self.app.add_url_rule("/api/reset", "/api/reset", self.reset, methods=['POST'])
        self.app.add_url_rule("/api/solve", "/api/solve", self.solve, methods=['POST'])

    def index(self):
        return render_template("index.html")

    def reset(self):
        self.problem = Problem()
        return Response("Ok", HTTPStatus.OK, content_type="text/plain")

    def list_variables(self):
        return Response(json.dumps({
            'variables': [
                {'name': var.name, 'isInverted': var.is_inverted, 'type': str(var.var_type.value)}
                for var in self.problem.variables
            ]}),
            HTTPStatus.OK, content_type="application/json;charset=utf-8")

    def set_variable(self):
        data = request.json
        var_name = data['name']
        is_inverted = data['inverted']
        self.problem.set_variable(Variable(name=var_name, inverted=is_inverted))
        return Response('Ok', HTTPStatus.OK, content_type="text/plain")

    def list_objectives(self):
        return Response(json.dumps({
            'objectives': [{
                'goal': objective.goal.value, 'expression': str(objective.expression)
            } for objective in self.problem.objectives]
        }), HTTPStatus.OK, content_type="application/json;charset=utf-8")

    def add_objective(self):
        data = request.json
        goal = ObjectiveGoal.from_str(data['goal'])
        expression = self.parser.parse(data['expression'])
        self.problem.add_objective(Objective(expression=expression, goal=goal))
        return Response('Created', HTTPStatus.CREATED, content_type="text/plain")

    def remove_objective(self):
        pass

    def list_constraints(self):
        return Response(json.dumps({
            'constraints': [{
                'left': str(constraint.left),
                'sign': str(constraint.sign.value),
                'right': str(constraint.right)
            } for constraint in self.problem.constraints
            ]}), HTTPStatus.OK, content_type="application/json;charset=utf-8")

    def add_constraint(self):
        data = request.json
        left = self.parser.parse(data['left'])
        sign = EqualitySigns.from_val(data['sign'])
        right = self.parser.parse(data['right'])
        self.problem.add_constraint(Constraint(left=left, sign=sign, right=right))
        return Response('Created', HTTPStatus.CREATED, content_type="text/plain")

    def remove_constraint(self):
        pass

    def solve(self):
        data = request.json
        solver = SolverMethods.from_val(data['method']).get_solver()
        debug = data['debug']
        solution = solver.solve(self.problem)
        if not solution:
            return Response("Definied system is not suitable for this method.", HTTPStatus.BAD_REQUEST,
                            content_type="text/plain")
        return Response(json.dumps({
            'vars': {var.name: var.val for var in solution.variables}
        }), HTTPStatus.OK, content_type="application/json; charset=utf-8")

    def start(self):
        self.app.run(host=self.host, port=self.port, threaded=True)
