import sys
import logging


class UnhandledExceptionLogger:
    def enable(self):
        # Direct all uncaught exceptions to handle_exception
        sys.excepthook = self.handle_exception

    def handle_exception(
        self, exc_type=None, exc_value=None, exc_traceback=None
    ):  # noqa: E501
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger = logging.getLogger(__name__)
        logger.critical(
            "Unhandled exception",
            exc_info=(exc_type, exc_value, exc_traceback),  # noqa: E501
        )


def unhandled_exception_setup():
    unhandled_exception_logger = UnhandledExceptionLogger()
    unhandled_exception_logger.enable()
