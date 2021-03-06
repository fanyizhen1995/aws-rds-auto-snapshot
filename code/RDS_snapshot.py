import boto3
import time
def lambda_handler(event, context):
    MAX_SNAPSHOTS = 5
    DB_INSTANCE_NAMES = ['test','mydbinstance']
    clientRDS = boto3.client('rds')
    for DB_INSTANCE_NAME in DB_INSTANCE_NAMES:
        db_snapshots = clientRDS.describe_db_snapshots(
            SnapshotType='manual',
            DBInstanceIdentifier= DB_INSTANCE_NAME
        )['DBSnapshots']
        for i in range(0, len(db_snapshots) - MAX_SNAPSHOTS + 1):
            oldest_snapshot = db_snapshots[0]
            for db_snapshot in db_snapshots:
                if oldest_snapshot['SnapshotCreateTime'] > db_snapshot['SnapshotCreateTime']:
                    oldest_snapshot = db_snapshot
            clientRDS.delete_db_snapshot(DBSnapshotIdentifier=oldest_snapshot['DBSnapshotIdentifier'])
            db_snapshots.remove(oldest_snapshot)
        clientRDS.create_db_snapshot(
            DBSnapshotIdentifier=DB_INSTANCE_NAME + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()),
            DBInstanceIdentifier=DB_INSTANCE_NAME
        )