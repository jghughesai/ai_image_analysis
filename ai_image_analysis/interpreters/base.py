class BaseInterpreter:
    def get_results(self, model, prompt, image):
        raise NotImplementedError("This method should be overridden by subclasses")
