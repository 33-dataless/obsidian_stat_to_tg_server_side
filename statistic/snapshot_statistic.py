class SnapshotStatistic:
    def __init__(self):
        pass

    async def count_changes(self, new_snapshot: dict, old_snapshot: dict) -> tuple[int, int]:
        increased = 0
        decreased = 0
        all_chars = sum(new_snapshot.values())
        
        for name, new_value in new_snapshot.items():
            difference = new_value - old_snapshot.get(name, 0)

            if difference > 0:
                increased += difference
                all_chars += new_value
            elif difference < 0:
                decreased += abs(difference)
        
        return increased, decreased, all_chars


    