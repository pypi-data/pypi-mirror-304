import importlib
from pathlib import Path

from bdm2.logger import build_logger


class DependencyChecker:
    def __init__(self, required_modules):
        self.logger = build_logger(Path(__file__), save_log=False)
        self.required_modules = required_modules
        self.loaded_modules = {}
        self.missing_modules = []

    def dynamic_import(self, module_name):
        try:
            module = importlib.import_module(module_name)
            self.loaded_modules[module_name] = module
            return module
        except ImportError:
            self.missing_modules.append(module_name)
            return None

    def check_dependencies(self):
        for module in self.required_modules:
            self.dynamic_import(module)
        if self.missing_modules:
            missing_list = '\n'.join(self.missing_modules)
            self.logger.error(f"Next dependency is absent:\n{missing_list}")
            self.logger.info("Check poetry dependency groups for install it")

    def get_module(self, module_name):
        return self.loaded_modules.get(module_name)


if __name__ == '__main__':

    # Пример использования класса
    required_modules = [
        'scipy.stats',
        'numpy',
        'pandas',
        # Добавьте сюда все другие модули, которые используются
    ]

    checker = DependencyChecker(required_modules)
    checker.check_dependencies()

    # Использование загруженных модулей
    numpy = checker.get_module('numpy')
    if numpy:
        # Работайте с модулем numpy
        print(numpy.__version__)

    pandas = checker.get_module('pandas')
    if pandas:
        # Работайте с модулем pandas
        print(pandas.__version__)
