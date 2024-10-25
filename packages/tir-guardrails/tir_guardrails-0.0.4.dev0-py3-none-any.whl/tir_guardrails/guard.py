import importlib

from tir_guardrails.constants import ConfigKeys, VALIDATOR_MODULE_NAMES


class Guard:
    def __init__(self, config: dict):
        self.block_message = config.pop(ConfigKeys.BLOCK_MESSAGE.value)
        self.validators: list = []
        module_name = "tir_guardrails.{}.validator"
        for validator_name in config.keys():
            if validator_name in VALIDATOR_MODULE_NAMES:
                module = importlib.import_module(module_name.format(validator_name))
                validator_class = getattr(module, "Validator")
                validator = validator_class(config.get(validator_name))
                self.validators.append(validator)

    def validate(self, messages=None, prompt=None):
        if (messages or prompt) is None:
            raise ValueError("Either 'messages' or 'prompt' must be provided.")
        validation_passed = True
        is_messages = True if messages else False

        latest_validated_input = messages if is_messages else prompt
        for validator in self.validators:
            kwargs = {"messages" if is_messages else "prompt": latest_validated_input}
            result = validator.validate(**kwargs)
            validation_passed = validation_passed and result["validation_passed"]
            latest_validated_input = result["validated_output"]

        if validation_passed:
            return {
                "status": "success",
                "validation_passed": validation_passed,
                "validated_output": latest_validated_input
            }

        return {
            "status": "error",
            "validation_passed": validation_passed,
            "validated_output": latest_validated_input
        }
