from pinecone import Pinecone
from app.config import pinecone_api_key


pc = Pinecone(api_key=pinecone_api_key)

index = pc.Index("qa-test-agent-fdd")

# QTY of records BEFORE deletion
stats_before = index.describe_index_stats()
count_before = stats_before["total_vector_count"]

print("Records before deletion:", count_before)

# delete record by index
index.delete(
    ids=["8e06c4fe-ceeb-40f1-a7f1-1a561681515b"]
)

print("Record deleted")

# QTY of records AFTER deletion
stats_after = index.describe_index_stats()
count_after = stats_after["total_vector_count"]

print("Records after deletion:", count_after)

# Check if exactly 1 record was deleted
if count_after == count_before - 1:
    print("SUCCESS: exactly 1 record was deleted")
else:
    print("WARNING: unexpected number of records deleted")
