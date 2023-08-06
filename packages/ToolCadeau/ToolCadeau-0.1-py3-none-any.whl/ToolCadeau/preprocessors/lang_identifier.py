import sys
import os
import fasttext

def print_error(status, func_name, message):
    print(status + "|" + func_name + "|" + message)

class FasttextIdentifier:
    """Fasttext language identifier to identify the languaga

    Args:
        None

    Returns:
        object: Fasttext language identifier model with function predict_lang
    """
    def __init__(self):
        file = sys.modules[__class__.__module__].__file__
        path = os.path.abspath(file)
        directory = os.path.dirname(path) + "/" + "tools"
        # root directory + "../" + "models" 
        self.model = None
        
        try:
            function = sys._getframe().f_code.co_name
            self.model = fasttext.load_model(directory + "/fasttext.bin")
        except Exception as e:
            message = f"Loading model from {directory} error."
            print_error("Fail", function, message)

    def predict_lang(self, text):
        predictions = self.model.predict(text, k=1)
        # |predictions| = tuple(lang), (accuracy))
        return predictions