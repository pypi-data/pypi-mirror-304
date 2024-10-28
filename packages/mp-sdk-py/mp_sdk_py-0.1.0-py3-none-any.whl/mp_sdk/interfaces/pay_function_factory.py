# pay_functions/pay_function_factory.py
import importlib
import inspect
from typing import List, Type
import pkgutil
from pathlib import Path
from .pay_function import IPayFunction
from .pay_function_metadata import PayFunctionMetadata
from ..decorators.bank_automation import BankAutomation


class PayFunctionFactory:
    _metadatas: List[PayFunctionMetadata] = []
    _initialized: bool = False

    @classmethod
    def initialize_metadatas(cls, package_prefix: str = "mp_executor"):
        """
        Initialize metadata by scanning all modules with the given prefix
        """
        if cls._initialized:
            return

        # Get the root package
        root_package = importlib.import_module(package_prefix)
        root_path = Path(root_package.__file__).parent

        # Scan all modules in the package
        for module_info in pkgutil.walk_packages([str(root_path)], f"{package_prefix}."):
            if module_info.ispkg:
                continue

            try:
                module = importlib.import_module(module_info.name)

                # Find all classes in the module
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (not inspect.isabstract(obj) and
                            issubclass(obj, IPayFunction) and
                            obj != IPayFunction):

                        # Check for BankAutomation decorator
                        bank_names = getattr(obj, '_bank_names', [])
                        for bank_name in bank_names:
                            metadata = next(
                                (m for m in cls._metadatas
                                 if m.name.lower() == bank_name.lower()),
                                None
                            )

                            if metadata is None:
                                metadata = PayFunctionMetadata()
                                metadata.name = bank_name
                                cls._metadatas.append(metadata)

                            metadata.pay_function_types.append(obj)

            except ImportError as e:
                print(f"Error importing module {module_info.name}: {e}")

        cls._initialized = True

    @classmethod
    def create_functions(cls, bank_name: str) -> List[IPayFunction]:
        """
        Create instances of pay functions for the specified bank
        """
        if not cls._initialized:
            cls.initialize_metadatas()

        functions = []
        metadata = next(
            (m for m in cls._metadatas if m.name.lower() == bank_name.lower()),
            None
        )

        if metadata:
            for function_type in metadata.pay_function_types:
                try:
                    function = function_type()
                    functions.append(function)
                except Exception as e:
                    print(f"Error creating instance of {function_type.__name__}: {e}")

        return functions

    @classmethod
    def get_supported_banks(cls) -> List[str]:
        """
        Get a list of all supported bank names
        """
        if not cls._initialized:
            cls.initialize_metadatas()

        return [metadata.name for metadata in cls._metadatas]