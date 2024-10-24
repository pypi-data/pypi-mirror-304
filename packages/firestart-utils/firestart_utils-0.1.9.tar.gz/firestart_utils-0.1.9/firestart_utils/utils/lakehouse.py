import notebookutils.lakehouse
import notebookutils.notebook
import notebookutils.mssparkutils.runtime

def get_context_value(key: str) -> str:
    return notebookutils.mssparkutils.runtime.context[key]

class Lakehouse:

    def by_name(self, lakehouse_name: str) -> dict:
        current_workspace_id = get_context_value('currentWorkspaceId')
        return {
                "uid": notebookutils.lakehouse.get(lakehouse_name, current_workspace_id),
                "abfsPath": eval("notebookutils.lakehouse.get(lakehouse_name, current_workspace_id).properties['abfsPath']")
            }
