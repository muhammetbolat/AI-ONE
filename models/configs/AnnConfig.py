class AnnConfig:
    def __init__(self,
                 model_file: str = None,
                 one_hot_model_file: str = None,
                 epochs: str = None,
                 batch_size: str = None,
                 test_size: str = None,
                 validation_split: str = None,
                 minimum_accuracy: int = None,
                 ):
        self.model_file = model_file
        self.one_hot_model_file = one_hot_model_file
        self.epochs = epochs
        self.batch_size = batch_size
        self.test_size = test_size
        self.validation_split = validation_split
        self.minimum_accuracy = minimum_accuracy
