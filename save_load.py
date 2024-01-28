import os
import pickle

save_data_path = 'data'


def save_object(object, object_name):
    try:
        if not os.path.exists(save_data_path):
            os.makedirs(save_data_path)

        with open(f'data/{object_name}.pickle', 'wb') as f:
            pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print(f'Error while trying to save object {object_name}: {ex}')


def load_object(object_name):
    try:
        file_path = f'data/{object_name}.pickle'
        if not os.path.exists(file_path):
            return None

        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except Exception as ex:
        print(f'Error while trying to load object {object_name}: {ex}')