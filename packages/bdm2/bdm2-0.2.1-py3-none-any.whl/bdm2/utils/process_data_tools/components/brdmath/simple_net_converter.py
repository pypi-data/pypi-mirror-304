import copy
import os
from typing import List

import numpy as np
import pandas as pd

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'tensorflow.python.keras'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

keras = checker.get_module('tensorflow.python.keras')

# from tensorflow.python.keras import backend as K
# from tensorflow.python.keras.layers import Activation
# from tensorflow.python.keras.layers import Dense
# from tensorflow.python.keras.losses import MeanSquaredError
# from tensorflow.python.keras.models import Sequential
# from tensorflow.python.keras.utils.generic_utils import get_custom_objects


from brddb.utils.common import colorstr

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class SimpleNet2Keras:
    def __init__(self, file_simple_model, path_save_weights=None, path_save_model_struct=None):
        functions = {"halflinear": keras.layers.Activation(self.halflinear),
                     "halflinearpos": keras.layers.Activation(self.halflinearpos),
                     "sigmoid_symm2": keras.layers.Activation(self.sigmoid_symm2),
                     "tanh": keras.layers.Activation(self.tanh)}
        keras.utils.generic_utils.get_custom_objects().update(functions)
        self.activations = {0: "sigmoid",
                            2: "tanh",
                            3: "sigmoid_symm2",
                            4: "linear",
                            5: "halflinear",
                            6: "relu",
                            7: "halflinearpos"}
        self.model = self.create_model(file_simple_model)
        if path_save_weights:
            self.model.save_weights(path_save_weights)
        if path_save_model_struct:
            self.save_model_json(path_save_model_struct)

    def halflinear(self, x):
        return keras.backend.switch(x < 0, keras.backend.sigmoid(x) - 0.5, x * 0.25)

    def halflinearpos(self, x):
        return keras.backend.switch(x < 0, keras.backend.sigmoid(x), x * 0.25 + 0.5)

    def sigmoid_symm2(self, x):
        return keras.backend.sigmoid(x) - 0.5

    def tanh(self, x):
        return 1.7159 * keras.backend.tanh((2.0 / 3.0) * x)

    def compute_weights(self, str_weights, l):
        lines = [line.strip("\n").strip(" ").split(" ") for line in str_weights]
        lines = [float(x) for line in lines for x in line]

        weights = []
        for i in range(len(l)):
            w = []
            b = []
            for j in range(l[i][-1]):
                w.append(lines[:l[i][0]])
                del lines[:l[i][0]]
                b.append(lines.pop(0))
            w = np.array(w)
            b = np.array(b).reshape((l[i][-1],))
            w = w.T
            weights.extend([w, b])
        return weights

    def load_file(self, simple_w):
        if not os.path.exists(simple_w):
            raise FileNotFoundError(f"Check path simpleNet model: {simple_w}")
        with open(simple_w, "r") as fin:
            simple_w = fin.readlines()

        dict_config = {}
        n = 2
        for i, line in enumerate(simple_w[1:]):
            line = line.strip("\n").strip(" ")
            if line == "Weights":
                n += i
                break
            key, value = line.strip("\n").strip(" ").split(":")
            dict_config[key] = value

        l = []
        layers = [int(x) for x in dict_config["Config"].split(" ")]
        for i in range(1, int(dict_config["Layers"])):
            l.append([layers[i - 1], layers[i]])
        weights = self.compute_weights(simple_w[n:], l)
        dict_config["Weights"] = weights
        dict_config["Config"] = layers
        return dict_config

    def create_model(self, file_simple_model):
        dict_config = self.load_file(file_simple_model)
        acts = int(dict_config["Activations"])
        output_activation = int(dict_config["Output activation"])
        if acts not in self.activations or output_activation not in self.activations:
            raise KeyError(
                f"Check activations in model.net. Not found {acts} keras.layers.Activation or {output_activation} keras.layers.Activation")

        else:
            acts = self.activations[acts]
            output_activation = self.activations[output_activation]

        model = keras.models.Sequential()
        layers = dict_config["Config"]
        for i in range(1, int(dict_config["Layers"])):
            if i == int(dict_config["Layers"]) - 1:
                model.add(keras.layers.Dense(layers[i], input_dim=layers[i - 1], activation=output_activation))
            else:
                model.add(keras.layers.Dense(layers[i], input_dim=layers[i - 1], activation=acts))

        model.compile(loss=keras.losses.MeanSquaredError(), metrics=['mse'], optimizer='adam')
        model.set_weights(dict_config["Weights"])
        return model

    def save_model_json(self, path):
        # serialize model to JSON
        model_json = self.model.to_json()
        with open(path, "w") as json_file:
            json_file.write(model_json)


class Keras2SimpleNet():
    def __init__(self, model_keras):
        functions = {"halflinear": keras.layers.Activation(self.halflinear),
                     "halflinearpos": keras.layers.Activation(self.halflinearpos),
                     "sigmoid_symm2": keras.layers.Activation(self.sigmoid_symm2),
                     "tanh": keras.layers.Activation(self.tanh)}
        keras.utils.generic_utils.get_custom_objects().update(functions)
        activations = {0: "sigmoid",
                       2: "tanh",
                       3: "sigmoid_symm2",
                       4: "linear",
                       5: "halflinear",
                       6: "relu",
                       7: "halflinearpos"}

        self.reverse_activations = {v: keras.backend for keras.backend, v in activations.items()}

        self.model = model_keras
        self.dict_config = {}
        self.create_file_structure()

    def halflinear(self, x):
        return keras.backend.switch(x < 0, keras.backend.sigmoid(x) - 0.5, x * 0.25)

    def halflinearpos(self, x):
        return keras.backend.switch(x < 0, keras.backend.sigmoid(x), x * 0.25 + 0.5)

    def sigmoid_symm2(self, x):
        return keras.backend.sigmoid(x) - 0.5

    def tanh(self, x):
        return 1.7159 * keras.backend.tanh((2.0 / 3.0) * x)

    def create_file_structure(self):
        config = self.model.get_config()
        weights = self.model.get_weights()
        start_layer = 0
        if keras.__version__ > "2.4.2":
            self.dict_config["Layers"] = len(config["layers"])
            start_layer = 1
        else:
            self.dict_config["Layers"] = len(config["layers"]) + 1

        for num, name in zip([start_layer, -1], ["Activations", "Output activation"]):
            if type(config['layers'][num]['config']['activation']) == str:
                self.dict_config[name] = self.reverse_activations[config['layers'][num]['config']['activation']]
            else:
                self.dict_config[name] = self.reverse_activations[
                    config['layers'][num]['config']['activation']['config']['activation']]

        layers = []
        for i in range(0, len(weights), 2):
            sh = [str(x) for x in weights[i].shape]
            layers.extend(sh)

        self.dict_config["Config"] = " ".join(list(dict.fromkeys(layers)))
        self.dict_config["Weights"] = " ".join(self.get_weights_from_model(weights))

    def get_weights_from_model(self, weights):
        weights_flatten = []

        for i in range(0, len(weights), 2):
            for j in range(weights[i].shape[1]):
                weights_flatten.extend(weights[i][:, j])
                weights_flatten.append(weights[i + 1][j])
        return [str(x) for x in weights_flatten]

    def save_simple_file(self, path):
        with open(path, "w") as fout:
            fout.write("(C) Pawlin Technologies Ltd FNN file format. PWNLIB 1.02" + "\n")
            for key in self.dict_config.keys():
                if key != "Weights":
                    fout.write(f"{key}:{self.dict_config[key]}" + "\n")
                else:
                    fout.write(key + "\n")
                    fout.write(str(self.dict_config[key]) + "\n")


def compare_results(true_val, pred_val):
    z = pred_val.flatten().tolist()
    y = true_val.flatten().tolist()

    z = [round(x, 6) for x in z]
    y = [round(x, 6) for x in y]

    return all([z[i] == y[i] for i in range(len(z))])


def check_inputs(df: pd.DataFrame, model: SimpleNet2Keras, inp_features: List[str]) -> List[str]:
    _inp_features = copy.copy(inp_features)

    # Check if model input size is equal to len(inp_features)
    n_inputs = model.model.input_shape[1]
    if n_inputs != len(_inp_features):
        print(colorstr('red', 'bold',
                       f'Size of featuremask != input size of model. '
                       f'Supposed input features are: {_inp_features}'))
        union_inp_features = []
        for f in _inp_features:
            if f in df.columns:
                union_inp_features.append(f)
        if n_inputs != len(union_inp_features):
            print(colorstr('red', 'bold', 'Size of UNION input features != input size of model'))
            raise RuntimeError('Wrong model or feature mask')
        else:
            print(colorstr('yellow', 'bold',
                           f'In order to suit the model, next input features will be used: {union_inp_features}, '
                           'Please, check the order!'))
        _inp_features = union_inp_features
    return _inp_features
