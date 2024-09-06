def tw_merge(base_tw_class_list: str, tw_class_list_to_merge: str) -> str:
    base_tw_classes = base_tw_class_list.split()
    base_tw_class_prefix = {cls.split("-")[0] for cls in base_tw_classes}

    unique_tw_classes = [
        cls
        for cls in tw_class_list_to_merge.split()
        if cls.split("-")[0] not in base_tw_class_prefix
    ]

    return " ".join(base_tw_classes + unique_tw_classes)
