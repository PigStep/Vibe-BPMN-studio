def extract_system_and_config(configuration: dict) -> tuple[str, dict]:
    # Using copy because working with global object (partial)
    config_copy = configuration.copy()
    system = config_copy.pop("system_prompt", None)
    return system, config_copy
