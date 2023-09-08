# design.


```
┌────────────────────────────┐
│                            │                  ┌─────────────────────────────────────┐
│           Camera           │   Every 5 mins.  │                                     │
│                            ├─────────────────►│ images/YYYYMMDD/YYYYMMDD_HHMMSS.jpg │
│                            │                  └─────────────────────────────────────┘
└────────────────────────────┘                                    │
                                                                  │
┌────────────────────────────┐◄───────────────────────────────────┘
│                            │                  ┌─────────────────────────────────────┐
│     Timestamped Images     │  Every 60 mins.  │ timestamped_\                       │
│                            ├─────────────────►│ images/YYYYMMDD/YYYYMMDD_HHMMSS.jpg │
│                            │                  └─────────────────────────────────────┘
└────────────────────────────┘                                    │
                                                                  │
┌────────────────────────────┐◄───────────────────────────────────┘
│                            │                  ┌─────────────────────────────────────┐
│   Colour Profiled Images   │  Every 6 hours.  │ processed_\                         │
│                            ├─────────────────►│ images/YYYYMMDD/YYYYMMDD_HHMMSS.jpg │
│                            │ Skip current day └─────────────────────────────────────┘
└────────────────────────────┘                                    │
                                                                  │
┌────────────────────────────┐◄───────────────────────────────────┘
│                            │                  ┌─────────────────────────────────────┐
│  Generate processed video  │  Every 6 hours.  │                                     │
│                            ├─────────────────►│    processed_videos/YYYYMMDD.mp4    │
│                            │ Skip current day.└─────────────────────────────────────┘
└────────────────────────────┘ Don't run whilst "Colour Profiled Images" is running.
                               (don't run for directories that have the .processing file)
```
