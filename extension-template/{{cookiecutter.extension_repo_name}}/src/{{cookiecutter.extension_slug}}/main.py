from ai_atlas_nexus.toolkit.logging import configure_logger


logger = configure_logger(__name__)


class Extension:

    def __init__(self):
        """Main extension class to run the task"""
        ...

    def run(self):
        """Extension run method.

        Returns:
            None
        """

        ...
