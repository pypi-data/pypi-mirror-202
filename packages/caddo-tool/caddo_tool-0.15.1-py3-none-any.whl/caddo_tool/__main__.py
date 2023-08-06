from copy import deepcopy

from caddo_tool.modules.attributes import Attributes
from caddo_tool.modules.module_loader import ModuleLoader
from caddo_tool.settings.settings_loader import SettingsLoader

from caddo_tool.utils.data_loader import DataLoader
from utils.dict_utils import merge_dict


class Caddo:
    def __init__(self):
        SettingsLoader().load()
        self.date_loader = DataLoader()
        self.model_initializer_module = None
        self.data_preprocessor_module = None
        self.model_trainer_module = None
        self.model_tester_module = None
        self.model_evaluator_module = None
        self.load_modules()
        self.run()

    def load_modules(self):
        print("LOADING MODULES:")
        module_loader = ModuleLoader()
        self.model_initializer_module = module_loader.load_model_initializer()
        self.data_preprocessor_module = module_loader.load_data_preprocessor()
        self.model_trainer_module = module_loader.load_model_trainer()
        self.model_tester_module = module_loader.load_model_tester()
        self.model_evaluator_module = module_loader.load_model_evaluator()
        self.summarize_module = module_loader.load_summarize()
        print()

    def run(self):
        metadata = self.date_loader.init_metadata()
        print("\nPREPARING DATA")
        attributes = self.date_loader.init_attributes_dict()
        self.summarize_raw_attributes(attributes)
        print("\n\n\nPREPROCESSING FILE")
        attributes = self.data_preprocessor_module.preprocess(attributes)
        self._check_if_x_and_y_has_same_cardinality(attributes)
        self.summarize_preprocessed_files(attributes)
        print("\n\n\nInitializing model")
        attributes = self.model_initializer_module.init_model(attributes)
        print("\nBENCHMARKING MODEL\n")
        for run in metadata[Attributes.RUNS]:
            for index_set in run.index_sets:
                print(f"Running benchmark on Run {run.number} index_set {index_set.number}")
                train_attributes = self.date_loader.create_train_attributes(attributes, index_set)
                print("Training model")
                self.model_trainer_module.train(train_attributes)
                print("Testing model")
                test_attributes = self.date_loader.create_test_attributes(attributes, index_set, train_attributes)
                self.model_tester_module.test(test_attributes)
                print("Evaluating model")
                self._copy_attributes_back(test_attributes, attributes)
                evaluate_attributes = self.date_loader.enchance_with_proper_responses(attributes, index_set, test_attributes)
                self.model_evaluator_module.evaluate(evaluate_attributes)
                self._copy_attributes_back(evaluate_attributes, attributes)
                print()
        self.summarize_module.summarize(attributes)

    def summarize_raw_attributes(self, attributes):
        print("Input data summary")
        print("Raw X head:")
        print(attributes[Attributes.X_RAW].head(5))
        print()
        print("Raw Y head:")
        print(attributes[Attributes.Y_RAW].head(5))

    def summarize_preprocessed_files(self, attributes):
        print("Input data summary after preprocessing")
        print("X head:")
        print(attributes[Attributes.X].head(5))
        print()
        print("Y head:")
        print(attributes[Attributes.Y].head(5))

    def _check_if_x_and_y_has_same_cardinality(self, attributes):
        print('Checking if number of X and Y is the same')
        x = attributes[Attributes.X]
        y = attributes[Attributes.Y]
        has_same_cardinality = len(x) == len(y)
        if not has_same_cardinality:
            raise AttributeError('Cardinality of post processed X and  Y are different')

    def _copy_attributes_back(self, test_attributes, attributes):
        attributes[Attributes.STORE] = deepcopy(merge_dict(test_attributes[Attributes.STORE], attributes[Attributes.STORE]))


if __name__ == '__main__':
    Caddo()
