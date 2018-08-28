from strainer import formatters


@formatters.export_formatter
def enum_formatter(value, context=None):
    return value.name
