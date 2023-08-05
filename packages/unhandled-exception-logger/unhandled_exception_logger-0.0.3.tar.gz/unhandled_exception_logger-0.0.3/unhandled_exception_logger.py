import sys
import logging


class UnhandledExceptionLogger:
    def __init__(self, handler=None):
        self.handler = handler
        self.logger = logging.getLogger(__name__)
        if self.handler is not None:
            self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.CRITICAL)

    def enable(self):
        # Direct all uncaught exceptions to handle_exception
        sys.excepthook = self.handle_exception

    def handle_exception(
        self, exc_type=None, exc_value=None, exc_traceback=None
    ):  # noqa: E501
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        self.logger.critical(
            "Unhandled exception",
            exc_info=(exc_type, exc_value, exc_traceback),  # noqa: E501
        )


def unhandled_exception_setup(handler=None):
    unhandled_exception_logger = UnhandledExceptionLogger(handler)
    unhandled_exception_logger.enable()


def handle_exception(
    exc_type=None,
    exc_value=None,
    exc_traceback=None,
    handler=None,
):
    unhandled_exception_logger = UnhandledExceptionLogger(handler=handler)
    unhandled_exception_logger.handle_exception(
        exc_type, exc_value, exc_traceback
    )  # noqa: E501
