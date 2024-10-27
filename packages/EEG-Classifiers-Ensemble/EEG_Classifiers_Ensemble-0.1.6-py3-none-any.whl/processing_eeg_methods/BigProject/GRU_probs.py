import matplotlib.pyplot as plt
import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import GRU, Activation, BatchNormalization, Dense, Dropout, Flatten
from keras.models import Sequential, load_model
from scipy import signal
from scipy.fftpack import dct, idct
from sklearn import preprocessing

from processing_eeg_methods.data_utils import train_test_val_split
from processing_eeg_methods.share import ROOT_VOTING_SYSTEM_PATH


def GRU_train(dataset_name, data, labels, num_classes: int):
    # substract data from list
    X_train, X_test, _, y_train, y_test, _ = train_test_val_split(
        dataX=data, dataY=labels, valid_flag=False
    )

    # get data dimension
    N_train, T_train, C_train = X_train.shape
    N_test, T_test, C_test = X_test.shape

    # add dummy zeros for y classification
    lb = preprocessing.LabelBinarizer()
    lb.fit(list(range(0, num_classes)))
    y_train = lb.transform(y_train)
    y_test = lb.transform(y_test)

    # Filtering through FFT(discrete cosine transform)

    def filter(x, low=0, high=1, plot=False):
        N = x.shape[0]
        t = np.linspace(0, N, N)
        y = dct(x, norm="ortho")
        window = np.zeros(N)
        window[int(low * N) : int(high * N)] = 1
        yr = idct(y * window, norm="ortho")
        sum(abs(x - yr) ** 2) / sum(abs(x) ** 2)
        if plot:
            plt.plot(t, x, "-b")
            plt.plot(t, yr, "r")
        return x

    # Filter band
    low_freq = 0.02
    high_freq = 0.4

    for i in np.arange(N_train):
        for j in np.arange(C_train):
            X_train[i, :, j] = filter(X_train[i, :, j], low_freq, high_freq)

    for i in np.arange(N_test):
        for j in np.arange(C_test):
            X_test[i, :, j] = filter(X_test[i, :, j], low_freq, high_freq)

    # Downsampling in time through FFT

    t_sample = 50
    X_train_sub = signal.resample(X_train, t_sample, axis=1)
    X_test_sub = signal.resample(X_test, t_sample, axis=1)

    data_dim = C_train
    seq_split = 1  # Set to one when using FFT to down sample
    seq_len = int(X_train_sub.shape[1] * seq_split)
    timesteps = seq_len
    batch_size = 200
    num_epoch = 100

    model = Sequential()
    # 1
    model.add(
        GRU(
            200,
            return_sequences=True,
            stateful=False,
            recurrent_dropout=0.6,
            dropout=0.6,
            input_shape=(timesteps, data_dim),
        )
    )

    # 2
    model.add(
        GRU(
            100,
            return_sequences=True,
            stateful=False,
            recurrent_dropout=0.5,
            dropout=0.5,
        )
    )

    # 3
    model.add(
        GRU(
            50,
            return_sequences=True,
            stateful=False,
            recurrent_dropout=0.4,
            dropout=0.4,
        )
    )
    model.add(Flatten())

    # 4
    model.add(Dense(100))
    model.add(BatchNormalization(axis=-1))
    model.add(Activation("relu"))
    model.add(Dropout(0.5))

    # 5
    model.add(Dense(num_classes, activation="softmax"))

    model.compile(
        loss="categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"]
    )

    # define early stopping callback
    earlystop = EarlyStopping(
        monitor="val_loss", min_delta=0.001, patience=30, mode="auto"
    )

    # saves the model weights after each epoch if the validation loss decreased
    checkpointer = ModelCheckpoint(
        filepath=f"{ROOT_VOTING_SYSTEM_PATH}/Results/BigProject/GRU_model_{dataset_name}.hdf5",
        monitor="val_accuracy",
        verbose=1,
        save_best_only=True,
    )

    callbacks_list = [earlystop, checkpointer]

    model.fit(
        X_train_sub[:, :seq_len, :],
        y_train,
        batch_size=batch_size,
        epochs=num_epoch,
        shuffle=True,
        validation_split=0.15,
        callbacks=callbacks_list,
    )

    # evaluate model on entire training set
    model = load_model(
        f"{ROOT_VOTING_SYSTEM_PATH}/Results/BigProject/GRU_model_{dataset_name}.hdf5"
    )
    results = model.evaluate(X_train_sub, y_train, batch_size=N_train)
    print("GRU training acuracy: ", results[1])

    # evaluate model on test set
    results = model.evaluate(X_test_sub, y_test, batch_size=N_test)
    print("GRU testing acuracy: ", results[1])
    acc = results[1]
    return model, acc


def GRU_test(model, trial_data):
    t_sample = 50
    trial_data = signal.resample(trial_data, t_sample, axis=1)
    output_array = model.predict(trial_data)
    return output_array
