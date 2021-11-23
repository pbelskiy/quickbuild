class Changes:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get_version(self) -> str:
        """
        Get the data version of changes.

        Returns:
            str: changes version.
        """
        return self.quickbuild._request('GET', 'changes/version')
