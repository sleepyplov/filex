from flask import current_app


def _format_log_message(message: str, **params):
    log_message = message + ':\n'
    for key in params:
        log_message += f'\t{key} = %s\n'
    return log_message


def debug(message: str, **params):
    current_app.logger.debug(_format_log_message(message, **params), *params.values())


def info(message: str, **params):
    current_app.logger.info(_format_log_message(message, **params), *params.values())


def warning(message: str, **params):
    current_app.logger.warning(_format_log_message(message, **params), *params.values())


def error(message: str, **params):
    current_app.logger.error(_format_log_message(message, **params), *params.values())


def fatal(message: str, **params):
    current_app.logger.fatal(_format_log_message(message, **params), params.values())