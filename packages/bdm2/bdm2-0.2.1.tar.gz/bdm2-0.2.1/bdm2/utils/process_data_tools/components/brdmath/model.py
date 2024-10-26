import copy
import os
from typing import List

import numpy as np
import pandas as pd

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'torch',
    'sklearn',
    'engine'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

torch = checker.get_module('torch')
nn = checker.get_module('torch.nn')
mixture = checker.get_module('sklearn.mixture')
engine_configs = checker.get_module('engine.models.configs')
engine_nn_models = checker.get_module('engine.nn_models.utils')


class HalfLinear(nn.Module):
    def forward(self, x):
        return torch.where(x < 0, torch.sigmoid(x) - 0.5, x * 0.25)


class HalfLinearPos(nn.Module):
    def forward(self, x):
        return torch.where(x < 0, torch.sigmoid(x), x * 0.25 + 0.5)


class SigmoidSymm2(nn.Module):
    def forward(self, x):
        return torch.sigmoid(x) - 0.5


class SimpleNet2PyTorch(nn.Module):
    def __init__(self, file_simple_model, path_save_weights=None, path_save_model_struct=None):
        super(SimpleNet2PyTorch, self).__init__()
        self.activations = {
            0: "sigmoid",
            2: "tanh",
            3: "sigmoid_symm2",
            4: "linear",
            5: "halflinear",
            6: "relu",
            7: "halflinearpos",
        }
        self.config = self.load_file(file_simple_model)
        self.model = self.create_model()
        self.load_weights()
        if path_save_weights:
            torch.save(self.model.state_dict(), path_save_weights)
        if path_save_model_struct:
            self.save_model_json(path_save_model_struct)

    def tanh(self, x):
        return 1.7159 * torch.tanh((2.0 / 3.0) * x)

    def compute_weights(self, str_weights, l):
        lines = [line.strip("\n").strip(" ").split(" ") for line in str_weights]
        lines = [float(x) for line in lines for x in line]

        weights = {}
        for i in range(len(l)):
            w = []
            b = []
            for j in range(l[i][-1]):
                w.append(lines[: l[i][0]])
                del lines[: l[i][0]]
                b.append(lines.pop(0))
            w = np.array(w)
            b = np.array(b).reshape((l[i][-1],))
            weights[i] = [w, b]
        return weights

    def load_file(self, file_simple_model):
        if not os.path.exists(file_simple_model):
            raise FileNotFoundError(f"Check path simpleNet model: {file_simple_model}")
        with open(file_simple_model, "r") as fin:
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

    def create_model(self):
        dict_config = self.config
        acts = int(dict_config["Activations"])
        output_activation = int(dict_config["Output activation"])
        if acts not in self.activations or output_activation not in self.activations:
            raise KeyError(
                f"Check activations in model.net. Not found {acts} activation or {output_activation} activation")

        else:
            acts = self.activations[acts]
            output_activation = self.activations[output_activation]

        layers = dict_config["Config"]
        model = nn.Sequential()
        for i in range(1, int(dict_config["Layers"])):
            activation = acts if i < int(dict_config["Layers"]) - 1 else output_activation
            model.add_module(f"fc_{i}", nn.Linear(layers[i - 1], layers[i]))
            model.add_module(f"activation_{i}", self.get_activation(activation))
        return model

    def load_weights(self):
        state_dict = {}
        weights = self.config["Weights"]
        for i, layer in enumerate(weights):
            state_dict[f"fc_{i + 1}.weight"] = torch.tensor(weights[i][0], dtype=torch.float32)
            state_dict[f"fc_{i + 1}.bias"] = torch.tensor(weights[i][1], dtype=torch.float32)
        self.model.load_state_dict(state_dict)

    def get_activation(self, activation):
        activations = {
            "sigmoid": nn.Sigmoid(),
            "tanh": nn.Tanh(),
            "relu": nn.ReLU(),
            "linear": nn.Identity(),
            "halflinear": HalfLinear(),
            "halflinearpos": HalfLinearPos(),
            "sigmoid_symm2": SigmoidSymm2(),
        }
        if activation not in activations:
            raise ValueError(f"Activation {activation} not implemented.")
        return activations[activation]

    def forward(self, x):
        return self.model(x)

    def save_model_json(self, path):
        # Not implemented
        pass


class SimpleNet(SimpleNet2PyTorch):
    def __init__(self, model_path: str, feature_mask_path: str = None):
        super().__init__(model_path)
        if feature_mask_path:
            self.inp_feature_mask = self.get_inp_feature_mask(feature_mask_path)

    def get_inp_feature_mask(self, feature_mask_path: str) -> List[str]:
        _fm = pd.read_csv(feature_mask_path, sep=";", header=None)
        _fm = _fm.transpose()
        _fm = _fm.set_index(1)[0].sort_index()
        return list(_fm.values)

    def check_inputs(self, df: pd.DataFrame) -> List[str]:
        _inp_features = copy.copy(self.inp_feature_mask)

        # Check if model input size is equal to len(inp_features)
        n_inputs = self.model[0].in_features
        if n_inputs != len(_inp_features):
            print(f"Size of featuremask != input size of model. " f"Supposed input features are: {_inp_features}")
            union_inp_features = []
            for f in _inp_features:
                if f in df.columns:
                    union_inp_features.append(f)
            if n_inputs != len(union_inp_features):
                print("Size of UNION input features != input size of model")
                raise RuntimeError("Wrong model or feature mask")
            else:
                print(
                    f"In order to suit the model, next input features will be used: {union_inp_features}, " "Please, check the order!")
            _inp_features = union_inp_features
        return _inp_features

    def predict(self, df) -> pd.DataFrame:
        self.check_inputs(df)
        inp = torch.tensor(df[self.inp_feature_mask].values, dtype=torch.float32)
        with torch.no_grad():
            res = self.model(inp).detach().numpy()
        return res


class StatisticalClassifier:
    def __init__(self, feature_tag: str, num_clusters: int, min_feature_threshold: float = None,
                 max_feature_threshold: float = None):
        self.data = pd.DataFrame()
        self.stats = {}
        self.random_seed = engine_configs.RANDOM_SEED
        self.feature_tag = feature_tag
        self.num_clusters = num_clusters
        self.min_feature_threshold = 1 if min_feature_threshold is None else min_feature_threshold
        self.max_feature_threshold = 50 if max_feature_threshold is None else max_feature_threshold

    def intake_data(self, df):
        """
        Intake data from a DataFrame and filter based on feature thresholds.

        :param df: DataFrame with a column corresponding to feature_tag.
        """
        # Filter data by the given thresholds
        self.data = df[
            (df[self.feature_tag] >= self.min_feature_threshold) & (df[self.feature_tag] <= self.max_feature_threshold)]
        self.data = self.data[[self.feature_tag]].copy()  # Keep only the feature_tag column

    def clear_data(self):
        self.data = pd.DataFrame()

    def classify(self, value):
        if not self.stats:
            return {}

        outputs = {}
        for class_name, params in self.stats.items():
            mean, var = params["mean"], params["variance"]
            prob = engine_nn_models.norm_distr_nonorm(value, mean, np.sqrt(var))
            outputs[class_name] = prob
        return outputs

    def get_sigmas_diff(self, value):
        if not self.stats:
            return {}

        sigmas = {}
        for class_name, params in self.stats.items():
            mean, var = params["mean"], params["variance"]
            diff = value - mean
            sigma_diff = diff / np.sqrt(var)
            sigmas[class_name] = sigma_diff
        return sigmas

    def train(self):
        if self.data.empty:
            return

        # Convert to NumPy array for training
        data = self.data[self.feature_tag].values.reshape(-1, 1)
        gmm = mixture.GaussianMixture(n_components=self.num_clusters, covariance_type="diag", max_iter=1000, tol=0.01,
                                      random_state=self.random_seed)
        gmm.fit(data)

        means = gmm.means_.flatten()
        covariances = gmm.covariances_.flatten()

        class_names = {np.argmin(means): "down", np.argmax(means): "up"}
        self.stats.clear()

        for i in range(self.num_clusters):
            mean = means[i]
            variance = covariances[i]
            count = np.sum(gmm.predict(data) == i)

            M1 = mean
            M2 = variance * (count - 1)
            M3 = 0  # Assuming zero skewness
            M4 = 3 * variance ** 2 / count  # Assuming kurtosis = 3 for Gaussian

            self.stats[class_names.get(i, f"class_{i}")] = {"count": count, "mean": mean, "variance": variance,
                                                            "skewness": M3, "kurtosis": M4}

    def save(self, folder_name, filename, backup=True):
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)

        filepath = os.path.join(folder_name, filename)

        if backup and os.path.exists(filepath):
            backup_filepath = os.path.join(folder_name, f"{filename}_backup.txt")
            os.rename(filepath, backup_filepath)

        rows = []
        for class_name, stats in self.stats.items():
            row = [class_name, stats["count"], stats["mean"], np.sqrt(stats["variance"]), stats["skewness"],
                   stats["kurtosis"]]
            rows.append(row)

        df = pd.DataFrame(rows, columns=["class", "count", "mean", "stdev", "skew", "kurtosis"])
        df.to_csv(filepath, sep=";", index=False)

    def load(self, folder_name, filename):
        filepath = os.path.join(folder_name, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} not found.")

        df = pd.read_csv(filepath, sep=";")
        self.stats.clear()

        for _, row in df.iterrows():
            class_name = row["class"]

            self.stats[class_name] = {
                "count": row["count"],
                "mean": row["mean"],
                "variance": row["stdev"] ** 2,
                "skewness": row["skew"],
                "kurtosis": row["kurtosis"],
            }


if __name__ == "__main__":
    classifier = StatisticalClassifier(feature_tag="feature_1", num_clusters=2, min_feature_threshold=0,
                                       max_feature_threshold=10)

    data = pd.DataFrame({"feature_1": [5, 6, 7, 8, 9]})
    classifier.intake_data(data)

    classifier.train()
    output_probs = classifier.classify(8)
    print(output_probs)
    print(classifier.stats)
    # model_file_path = r"\\Datasets\chikens\MHDR_Chicken\RESULTS\CGTHBG\RESULTS_v4.10.7.45_CGTHBG_Arbor-Acres_male_2304_final_fast_restore\engine_snapshot\OtherData\prediction_nets\zbage.net"
    # feature_mask_path = r"\\Datasets\chikens\MHDR_Chicken\RESULTS\CGTHBG\RESULTS_v4.10.7.45_CGTHBG_Arbor-Acres_male_2304_final_fast_restore\engine_snapshot\OtherData\prediction_nets\featuremask.txt"
    # net = SimpleNet(model_file_path, feature_mask_path)
    # weights_not_loaded = net.config["Weights"]
    # weights_loaded = net.state_dict()
    # print("Weights not loaded: {}".format(weights_not_loaded))
    # print("Weights loaded: {}".format(weights_loaded))
    # torch.save(net.state_dict(), "model.pth")
    # print(net)
    # with torch.no_grad():
    #     arr = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0]])
    #     print(net)
    #     print(net.predict(arr))
    # for param in weights_not_loaded:
    #     print(param)
