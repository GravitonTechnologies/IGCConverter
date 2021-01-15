from typing import Optional


def get_selected_export_format(title: str) -> Optional[str]:
    if title == 'acmi-TacView':
        return 'acmi'
    elif title == 'csv':
        return 'csv'
    else:
        return None
