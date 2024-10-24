import notebookutils.lakehouse
import notebookutils.notebook

class Lakehouse:

    def by_name(self, lakehouse_name: str) -> dict:
        current_workspace_id = notebookutils.runtime.getCurrentWorkspaceId()

        return {
                "uid": notebookutils.lakehouse.get(lakehouse_name, current_workspace_id),
                "abfsPath": eval("notebookutils.lakehouse.get(lakehouse_name, current_workspace_id).properties['abfsPath']")
            }
