from reports.csv_writer import write_csv
from modules.cluster import collect

cluster = collect(session)

write_csv(
    "Cluster.csv",
    cluster
)