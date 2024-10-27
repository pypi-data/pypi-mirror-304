from typing import Union

import numpy as np
from sklearn.model_selection import StratifiedKFold

from processing_eeg_methods.data_dataclass import (
    ProcessingMethods,
    complete_experiment,
    probability_input,
)
from processing_eeg_methods.data_loaders import load_data_labels_based_on_dataset
from processing_eeg_methods.data_utils import (
    convert_into_independent_channels,
    get_dataset_basic_info,
    get_input_data_path,
    standard_saving_path,
    write_model_info,
)
from processing_eeg_methods.share import GLOBAL_SEED, datasets_basic_infos


def pseudo_trial_exhaustive_training_and_testing(
    ce: complete_experiment,
    pm: ProcessingMethods,
    dataset_info: dict,
    data_path: str,
    selected_classes: list[int],
    subject_range: Union[range, list],
):
    save_original_channels = dataset_info["#_channels"]
    save_original_trials = dataset_info["total_trials"]

    for subject_id in subject_range:
        print(subject_id)

        dataset_info["#_channels"] = save_original_channels
        dataset_info["total_trials"] = save_original_trials

        epochs, data, labels = load_data_labels_based_on_dataset(
            dataset_info,
            subject_id,
            data_path,
            selected_classes=selected_classes,
            normalize=True,
            apply_autoreject=True,
        )

        # Because we are using independent channels:
        dataset_info["total_trials"] = len(labels)
        dataset_info["#_channels"] = 1

        cv = StratifiedKFold(
            n_splits=10, shuffle=True, random_state=GLOBAL_SEED
        )  # Do cross-validation

        count_Kfolds: int = 0
        index_count: int = 0
        trial_index_count: int = 0
        for train, test in cv.split(epochs, labels):
            print(
                "******************************** Training ********************************"
            )
            count_Kfolds += 1
            # Convert independent channels to pseudo-trials
            data_train, labels_train = convert_into_independent_channels(
                data[train], labels[train]
            )
            data_train = np.transpose(np.array([data_train]), (1, 0, 2))

            pm.train(
                subject_id=subject_id,
                data=data_train,
                labels=labels_train,
                dataset_info=dataset_info,
            )

            print(
                "******************************** Test ********************************"
            )

            for epoch_number in test:
                trial_index_count += 1
                # Convert independent channels to pseudo-trials
                data_test, labels_test = convert_into_independent_channels(
                    np.asarray([data[epoch_number]]), labels[epoch_number]
                )
                data_test = np.transpose(np.array([data_test]), (1, 0, 2))

                for pseudo_trial in range(len(data_test)):
                    index_count += 1
                    pm.test(
                        subject_id=subject_id,
                        data=np.asarray([data_test[pseudo_trial]]),
                        dataset_info=dataset_info,
                    )

                    for method_name in vars(pm):
                        method = getattr(pm, method_name)
                        if method.activation:
                            ce.data_point.append(
                                probability_input(
                                    trial_group_index=trial_index_count,
                                    group_index=index_count,
                                    dataset_name=dataset_name,
                                    methods=method_name,
                                    probabilities=method.testing.probabilities,
                                    subject_id=subject_id,
                                    channel=pseudo_trial,
                                    kfold=count_Kfolds,
                                    label=labels[epoch_number],
                                    training_accuracy=method.training.accuracy,
                                    training_timing=method.training.timing,
                                    testing_timing=method.testing.timing,
                                )
                            )

    dataset_info["#_channels"] = (
        save_original_channels  # todo: is there a better way to do this? maybe dataclass?
    )
    dataset_info["total_trials"] = save_original_trials
    return ce


def trial_exhaustive_training_and_testing(
    ce: complete_experiment,
    pm: ProcessingMethods,
    dataset_info: dict,
    data_path: str,
    selected_classes: list[int],
    subject_range: Union[range, list],
):
    for subject_id in subject_range:
        print(subject_id)

        epochs, data, labels = load_data_labels_based_on_dataset(
            dataset_info,
            subject_id,
            data_path,
            selected_classes=selected_classes,
            normalize=True,
            apply_autoreject=True,
        )

        cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=GLOBAL_SEED)

        count_Kfolds: int = 0
        trial_index_count: int = 0
        for train, test in cv.split(epochs, labels):
            print(
                "******************************** Training ********************************"
            )
            count_Kfolds += 1
            pm.train(
                subject_id=subject_id,
                data=data[train],
                labels=labels[train],
                dataset_info=dataset_info,
            )

            print(
                "******************************** Test ********************************"
            )

            for epoch_number in test:
                trial_index_count += 1

                pm.test(
                    subject_id=subject_id,
                    data=np.asarray([data[epoch_number]]),
                    dataset_info=dataset_info,
                )

                for method_name in vars(pm):
                    method = getattr(pm, method_name)
                    if method.activation:
                        ce.data_point.append(
                            probability_input(
                                trial_group_index=trial_index_count,
                                group_index=99,
                                dataset_name=dataset_name,
                                methods=method_name,
                                probabilities=method.testing.probabilities,
                                subject_id=subject_id,
                                channel=99,
                                kfold=count_Kfolds,
                                label=labels[epoch_number],
                                training_accuracy=method.training.accuracy,
                                training_timing=method.training.timing,
                                testing_timing=method.testing.timing,
                            )
                        )
    return ce


if __name__ == "__main__":
    combinations = [[0, 1, 2, 3]]
    import time

    start = time.time()
    for combo in combinations:

        # Manual Inputs
        dataset_name = "braincommand"
        selected_classes = combo  # [0, 1, 2, 3]
        subject_range = range(1, 27)
        independent_channels = True

        ce = complete_experiment()

        pm = ProcessingMethods()

        dataset_info = get_dataset_basic_info(datasets_basic_infos, dataset_name)
        dataset_info["#_class"] = len(selected_classes)

        pm.activate_methods(
            spatial_features=True,  # Training is over-fitted. Training accuracy >90
            simplified_spatial_features=True,  # Simpler than selected_transformers, only one transformer and no frequency bands. No need to activate both at the same time
            ShallowFBCSPNet=True,
            LSTM=False,  # Training is over-fitted. Training accuracy >90
            GRU=False,  # Training is over-fitted. Training accuracy >90
            diffE=False,  # It doesn't work if you only use one channel in the data
            feature_extraction=True,
            number_of_classes=dataset_info["#_class"],
        )
        activated_methods: list[str] = pm.get_activated_methods()
        combo_str = "_".join(map(str, combo))
        version_name = f"formal_calibration3_all_channels_{combo_str}"  # To keep track what the output processing alteration went through

        data_path = get_input_data_path(dataset_name)

        if independent_channels:
            ce = pseudo_trial_exhaustive_training_and_testing(
                ce,
                pm,
                dataset_info,
                data_path,
                selected_classes,
                subject_range=subject_range,
            )
        else:
            ce = trial_exhaustive_training_and_testing(
                ce, pm, dataset_info, data_path, selected_classes, subject_range
            )

        ce.to_df().to_csv(
            standard_saving_path(
                dataset_info,
                "methods_for_real_time",
                version_name + "_all_probabilities",
                file_ending="csv",
            )
        )

        write_model_info(
            standard_saving_path(
                dataset_info,
                "methods_for_real_time",
                version_name + "_all_probabilities",
            ),
            model_name="_".join(activated_methods),
            independent_channels=independent_channels,
            dataset_info=dataset_info,
            notes="Real subjects.",
        )

    end = time.time() - start
    print(f"In total it took {end} seconds, ")

    print("Congrats! The processing methods are done processing.")
