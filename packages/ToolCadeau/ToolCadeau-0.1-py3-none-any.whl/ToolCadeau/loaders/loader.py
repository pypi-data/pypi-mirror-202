import sys
import os

class QueryLoader:
    """QueryLoader to get queries saved in the "query" directory
    Directory "query" must be located at the parent root

    Args:
        None

    Returns:
        dictionary: python dictionary with key corresponds to the file name before .sql, and values query text.
    """
    def __init__(self):
        # file = sys.modules[__class__.__module__].__file__
        # path = os.path.abspath(file)
        # # root dir + "/query"
        # directory = os.path.dirname(path) + "/query"
        
        path = os.path.abspath(os.getcwd())
        directory = path + "/" + "query"
        self.fetch = None
        
        try:
            function = sys._getframe().f_code.co_name
            self.fetch = self.load_query(directory)
        except Exception as e:
            message = f"Loading SQL queris from {directory} error"
            self.print_f("Fail", message, function)
            print(e)
    
    def print_f(self, alert, message, function):
        print(alert + " | " + function + " | " + message)

    def load_query(self, directory):
        try:
            fetched = dict()
            sql_file = [x for x in os.listdir(directory) if x.split(".")[-1] == "sql"]
            for x in sql_file:
                file = open(directory + "/" + x, "r")
                fetched[x.split(".")[0]] = file.read()
                # Clear Buffer
                file.flush()
                file.close()
            return fetched
        except Exception as e:
            print(e)
            return False
        
if __name__ == "__main__":
    loader = QueryLoader()
    print(loader.fetch["item"])

        