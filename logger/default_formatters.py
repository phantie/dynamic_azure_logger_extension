from .custom_formatter import CustomFormatter



AZ_APPINSIGHTS_FORMATTER = CustomFormatter(
    # asctime present in timestamp column
    "[step {step}] "
    "[%(levelname)s] "
    "[name: %(name)s] "
    "[detached: %(detached)s] "
    "%(message)s"
)


STDOUT_FORMATTER = CustomFormatter(
    "[step {step}] "
    "[%(asctime)s] "
    "[%(levelname)s] "
    "[name: %(name)s] "
    "[detached: %(detached)s] "
    "[mod: %(module)s] "
    "[fn: %(funcName)s] "
    "[line: %(lineno)s] - "
    "%(message)s"
)
