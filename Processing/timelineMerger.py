from config import TimelineMergerConfig

class timelineMerger:
    def __init__(self):
        self.config = TimelineMergerConfig()

    def mergeTimelines(self, timelines):
        """Merges overlapping and close timelines into a single sorted timeline without duplicates."""
        timelines.sort(key=lambda x: x[0])
        mergedTimeline = []
        
        prev = timelines[0]

        for current in timelines[1:]:
            if current[0] <= prev[1] + self.config.mergeThreshold:
                prev[1] = max(prev[1], current[1])
            else:
                mergedTimeline.append(prev)
                prev = current
        mergedTimeline.append(prev)

        return mergedTimeline
        