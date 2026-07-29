"""
=========================================================
NetApp Health Dashboard
Health Rules
=========================================================
"""

# Total Score
MAX_SCORE = 100

# Module Scores
CLUSTER_SCORE = 15
NODE_SCORE = 20
AGGREGATE_SCORE = 20
VOLUME_SCORE = 15
DISK_SCORE = 10
NETWORK_SCORE = 5
PERFORMANCE_SCORE = 5
SNAPMIRROR_SCORE = 5
EVENT_SCORE = 5


# Thresholds

CPU_LIMIT = 80

MEMORY_LIMIT = 85

AGGREGATE_USED_LIMIT = 80

VOLUME_USED_LIMIT = 85

FAILED_DISK_ALLOWED = 0

CRITICAL_EVENT_ALLOWED = 0

SNAPMIRROR_LAG_LIMIT = 3600