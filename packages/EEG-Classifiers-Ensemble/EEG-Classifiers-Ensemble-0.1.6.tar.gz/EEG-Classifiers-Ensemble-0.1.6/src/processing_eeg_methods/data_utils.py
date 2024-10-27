import os

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.linear_model import RidgeClassifier, SGDClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split

from processing_eeg_methods.share import GLOBAL_SEED, ROOT_VOTING_SYSTEM_PATH

# from sklearn.linear_model import LogisticRegression
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
# from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
# from sklearn.gaussian_process import GaussianProcessClassifier
# from sklearn.gaussian_process.kernels import RBF
# from sklearn.naive_bayes import GaussianNB
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.neural_network import MLPClassifier
# from sklearn.svm import SVC
# from sklearn.tree import DecisionTreeClassifier

# MDM() Always nan at the end
classifiers = [  # The Good, Medium and Bad is decided on Torres dataset. This to avoid most of the processings.
    # KNeighborsClassifier(3), # Good
    # SVC(kernel='linear', probability=True), # Good
    RidgeClassifier()
    # GaussianProcessClassifier(1.0 * RBF(1.0), random_state=42), # Good # It doesn't have .coef
    # DecisionTreeClassifier(max_depth=5, random_state=42), # Good # It doesn't have .coef
    # RandomForestClassifier(max_depth=5, n_estimators=100, max_features=1, random_state=42), # Good It doesn't have .coef
    # MLPClassifier(alpha=1, max_iter=1000, random_state=42), # Good
    # AdaBoostClassifier(algorithm="SAMME", random_state=42), # Medium
    # GaussianNB(), # Medium
    # QuadraticDiscriminantAnalysis(), # Bad
    # LinearDiscriminantAnalysis(), # Bad
    # LogisticRegression(), # Good
]


def write_model_info(
    filepath: str,
    model_name: str,
    independent_channels: bool,
    dataset_info: dict,
    notes: str = "",
):
    """
    Writes information about a model to a text file.

    Parameters:
    filename (str): The name of the file to write to.
    model_name (str): The name of the model.
    montage_style (str): independent channels or standard montage.
    dataset_info (dict): Information about the dataset.
    notes (str): Any additional notes about the model.

    Returns:
    None
    """
    montage_style = (
        "independent channels" if independent_channels else "standard montage"
    )

    with open(filepath, "w") as file:
        file.write(f"Model Name: {model_name}\n")
        file.write(f"Montage Style: {montage_style}\n")
        file.write("\nDataset Information:\n")
        for key, value in dataset_info.items():
            file.write(f"{key}: {value}\n")
        if notes:
            file.write(f"Notes: {notes}\n")


def class_selection(dataX, dataY, event_dict: dict, selected_classes: list[int]):
    dataX_selected: list = []
    dataY_selected: list = []
    for dataX_idx, dataY_idx in zip(dataX, dataY):
        if dataY_idx in selected_classes:
            dataX_selected.append(dataX_idx)
            dataY_selected.append(dataY_idx)
    dataX_selected_np = np.asarray(dataX_selected)
    dataY_selected_df = pd.Series(dataY_selected)

    label_remap = {
        dataY_original: dataY_remap_idx
        for dataY_remap_idx, dataY_original in enumerate(selected_classes)
    }

    event_dict = {
        key: label_remap[value]
        for key, value in event_dict.items()
        if value in selected_classes
    }

    return (
        dataX_selected_np,
        np.asarray(dataY_selected_df.replace(label_remap)),
        event_dict,
    )


def convert_into_binary(label, chosen_numbered_label):
    label_copy = label.copy()
    for i, label_i in enumerate(label_copy):
        if label_i == chosen_numbered_label:
            label[i] = 1
        else:
            label[i] = 0
    return label


def train_test_val_split(dataX, dataY, valid_flag: bool = False):
    train_ratio = 0.75
    test_ratio = 0.10

    # train is now 75% of the entire data set
    x_train, x_test, y_train, y_test = train_test_split(
        dataX, dataY, test_size=1 - train_ratio
    )

    if valid_flag:
        validation_ratio = 1 - train_ratio - test_ratio
        # test is now 10% of the initial data set
        # validation is now 15% of the initial data set
        x_val, x_test, y_val, y_test = train_test_split(
            x_test, y_test, test_size=test_ratio / (test_ratio + validation_ratio)
        )
    else:
        x_val = None
        y_val = None
    return x_train, x_test, x_val, y_train, y_test, y_val


def standard_saving_path(
    dataset_info: dict,
    processing_name: str,
    version_name: str,
    file_ending: str = "txt",
    subject_id: int = 0,
):
    saving_folder: str = (
        f"{ROOT_VOTING_SYSTEM_PATH}/Results/{dataset_info['dataset_name']}/{processing_name}"
    )
    os.makedirs(saving_folder, exist_ok=True)
    if subject_id:
        return f"{saving_folder}/{version_name}_{subject_id}.{file_ending}"
    else:
        return f"{saving_folder}/{version_name}.{file_ending}"


def get_dataset_basic_info(datasets_basic_infos: dict, dataset_name: str) -> dict:
    if dataset_name not in datasets_basic_infos:
        raise Exception(
            f"Not supported dataset named '{dataset_name}', choose from the following: "
            f"{list(datasets_basic_infos.keys())}"
        )
    else:
        return datasets_basic_infos[dataset_name]


def get_best_classificator_and_test_accuracy(data, labels, estimators):
    param_grid = []
    for classificator in classifiers:
        param_grid.append({"clf__estimator": [classificator]})

    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=GLOBAL_SEED)
    clf = GridSearchCV(
        estimator=estimators, param_grid=param_grid, cv=cv
    )  # https://stackoverflow.com/questions/52580023/how-to-get-the-best-estimator-parameters-out-from-pipelined-gridsearch-and-cro
    clf.fit(data, labels)

    return clf.best_estimator_, clf.best_score_


def convert_into_independent_channels(data, labels):
    data_independent_channels = data.reshape(
        [data.shape[0] * data.shape[1], data.shape[2]], order="C"
    )  # [trials, channels, time] to [trials*channels, time]
    labels_independent_channels = np.repeat(labels, data.shape[1], axis=0)
    return data_independent_channels, labels_independent_channels


def flat_a_list(list_to_flat: list):
    return [x for xs in list_to_flat for x in xs]


class ClfSwitcher(BaseEstimator):
    # https://stackoverflow.com/questions/48507651/multiple-classification-models-in-a-scikit-pipeline-python

    def __init__(
        self,
        estimator=SGDClassifier(),
    ):
        """
        A Custom BaseEstimator that can switch between classifiers.
        :param estimator: sklearn object - The classifier
        """

        self.estimator = estimator

    def fit(self, X, y=None, **kwargs):
        self.estimator.fit(X, y)
        return self

    def predict(self, X, y=None):
        return self.estimator.predict(X)

    def predict_proba(self, X):
        return self.estimator._predict_proba_lr(X)

    def score(self, X, y):
        return self.estimator.score(X, y)

    def coef_(self):
        return self.estimator.coef_


def data_normalization(data):
    min_val = np.min(data)
    max_val = np.max(data)
    scaled_data = (data - min_val) / (max_val - min_val)

    return scaled_data


def get_input_data_path(dataset_name: str) -> str:
    return ROOT_VOTING_SYSTEM_PATH + "/Datasets/" + dataset_name + "_dataset"


def probabilities_to_answer(probs_by_channels: list, voting_by_mode: bool = False):
    if voting_by_mode:
        overall_decision = flat_a_list(probs_by_channels)
        return max(set(overall_decision), key=list(overall_decision).count)
    else:  # voting_by_array_probabilities
        by_channel_decision = np.nanmean(probs_by_channels, axis=0)  # Mean over columns
        return np.argmax(by_channel_decision)
