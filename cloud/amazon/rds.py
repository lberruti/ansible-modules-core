#!/usr/bin/python
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: rds
version_added: "1.3"
short_description: create, delete, or modify an Amazon rds instance
description:
     - Creates, deletes, or modifies rds instances.  When creating an instance it can be either a new instance or a read-only replica of an existing instance. This module has a dependency on python-boto >= 2.5. The 'promote' command requires boto >= 2.18.0. Certain features such as tags rely on boto.rds2 (boto >= 2.26.0)
options:
  command:
    description:
      - Specifies the action to take.  
    required: true
    default: null
    aliases: []
    choices: [ 'create', 'replicate', 'delete', 'facts', 'modify' , 'promote', 'snapshot', 'restore' ]
  instance_name:
    description:
      - Database instance identifier. Required except when using command=facts or command=delete on just a snapshot
    required: false
    default: null
    aliases: []
  source_instance:
    description:
      - Name of the database to replicate. Used only when command=replicate.
    required: false
    default: null
    aliases: []
  db_engine:
    description:
      - The type of database.  Used only when command=create. 
    required: false
    default: null
    aliases: []
    choices: [ 'MariaDB', 'MySQL', 'oracle-se1', 'oracle-se', 'oracle-ee', 'sqlserver-ee', 'sqlserver-se', 'sqlserver-ex', 'sqlserver-web', 'postgres']
  size:
    description:
      - Size in gigabytes of the initial storage for the DB instance. Used only when command=create or command=modify.
    required: false
    default: null
    aliases: []
  instance_type:
    description:
      - The instance type of the database.  Must be specified when command=create. Optional when command=replicate, command=modify or command=restore. If not specified then the replica inherits the same instance type as the source instance. 
    required: false
    default: null
    aliases: []
  username:
    description:
      - Master database username. Used only when command=create.
    required: false
    default: null
    aliases: []
  password:
    description:
      - Password for the master database username. Used only when command=create or command=modify.
    required: false
    default: null
    aliases: []
  region:
    description:
      - The AWS region to use. If not specified then the value of the EC2_REGION environment variable, if any, is used.
    required: true
    default: null
    aliases: [ 'aws_region', 'ec2_region' ]
  db_name:
    description:
      - Name of a database to create within the instance.  If not specified then no database is created. Used only when command=create.
    required: false
    default: null
    aliases: []
  engine_version:
    description:
      - Version number of the database engine to use. Used only when command=create. If not specified then the current Amazon RDS default engine version is used.
    required: false
    default: null
    aliases: []
  parameter_group:
    description:
      - Name of the DB parameter group to associate with this instance.  If omitted then the RDS default DBParameterGroup will be used. Used only when command=create or command=modify.
    required: false
    default: null
    aliases: []
  license_model:
    description:
      - The license model for this DB instance. Used only when command=create or command=restore. 
    required: false
    default: null
    aliases: []
    choices:  [ 'license-included', 'bring-your-own-license', 'general-public-license' ]
  multi_zone:
    description:
      - Specifies if this is a Multi-availability-zone deployment. Can not be used in conjunction with zone parameter. Used only when command=create or command=modify.
    choices: [ "yes", "no" ] 
    required: false
    default: null
    aliases: []
  iops:
    description:
      - Specifies the number of IOPS for the instance.  Used only when command=create or command=modify. Must be an integer greater than 1000.
    required: false
    default: null
    aliases: []
  security_groups:
    description:
      - Comma separated list of one or more security groups.  Used only when command=create or command=modify.
    required: false
    default: null
    aliases: []
  vpc_security_groups:
    description:
      - Comma separated list of one or more vpc security group ids. Also requires `subnet` to be specified. Used only when command=create or command=modify.
    required: false
    default: null
    aliases: []
  port:
    description:
      - Port number that the DB instance uses for connections.  Defaults to 3306 for mysql. Must be changed to 1521 for Oracle, 1443 for SQL Server, 5432 for PostgreSQL. Used only when command=create or command=replicate.
    required: false
    default: null
    aliases: []
  upgrade:
    description:
      - Indicates that minor version upgrades should be applied automatically. Used only when command=create or command=replicate. 
    required: false
    default: no
    choices: [ "yes", "no" ]
    aliases: []
  option_group:
    description:
      - The name of the option group to use.  If not specified then the default option group is used. Used only when command=create.
    required: false
    default: null
    aliases: []
  maint_window:
    description:
      - "Maintenance window in format of ddd:hh24:mi-ddd:hh24:mi.  (Example: Mon:22:00-Mon:23:15) If not specified then a random maintenance window is assigned. Used only when command=create or command=modify."
    required: false
    default: null
    aliases: []
  backup_window:
    description:
      - Backup window in format of hh24:mi-hh24:mi.  If not specified then a random backup window is assigned. Used only when command=create or command=modify.
    required: false
    default: null
    aliases: []
  backup_retention:
    description:
      - "Number of days backups are retained.  Set to 0 to disable backups.  Default is 1 day.  Valid range: 0-35. Used only when command=create or command=modify."
    required: false
    default: null
    aliases: []
  zone:
    description:
      - availability zone in which to launch the instance. Used only when command=create, command=replicate or command=restore.
    required: false
    default: null
    aliases: ['aws_zone', 'ec2_zone']
  subnet:
    description:
      - VPC subnet group.  If specified then a VPC instance is created. Used only when command=create.
    required: false
    default: null
    aliases: []
  snapshot:
    description:
      - Name of snapshot to take. When command=delete, if no snapshot name is provided then no snapshot is taken. If used with command=delete with no instance_name, the snapshot is deleted. Used with command=facts, command=delete or command=snapshot.
    required: false
    default: null
    aliases: []
  aws_secret_key:
    description:
      - AWS secret key. If not set then the value of the AWS_SECRET_KEY environment variable is used. 
    required: false
    default: null
    aliases: [ 'ec2_secret_key', 'secret_key' ]
  aws_access_key:
    description:
      - AWS access key. If not set then the value of the AWS_ACCESS_KEY environment variable is used.
    required: false
    default: null
    aliases: [ 'ec2_access_key', 'access_key' ]
  wait:
    description:
      - When command=create, replicate, modify or restore then wait for the database to enter the 'available' state.  When command=delete wait for the database to be terminated.
    required: false
    default: "no"
    choices: [ "yes", "no" ]
    aliases: []
  wait_timeout:
    description:
      - how long before wait gives up, in seconds
    default: 300
    aliases: []
  apply_immediately:
    description:
      - Used only when command=modify.  If enabled, the modifications will be applied as soon as possible rather than waiting for the next preferred maintenance window.
    default: no
    choices: [ "yes", "no" ]
    aliases: []
  new_instance_name:
    description:
      - Name to rename an instance to. Used only when command=modify.
    required: false
    default: null
    aliases: []
    version_added: 1.5
  character_set_name:
    description:
      - Associate the DB instance with a specified character set. Used with command=create.
    required: false
    default: null
    aliases: []
    version_added: 1.9
  publicly_accessible:
    description:
      - explicitly set whether the resource should be publicly accessible or not. Used with command=create, command=replicate. Requires boto >= 2.26.0
    required: false
    default: null
    aliases: []
    version_added: 1.9
  tags:
    description:
      - tags dict to apply to a resource. Used with command=create, command=replicate, command=restore. Requires boto >= 2.26.0
    required: false
    default: null
    aliases: []
    version_added: 1.9
requirements: [ "boto" ]
author: Bruce Pennypacker, Will Thames
'''

# FIXME: the command stuff needs a 'state' like alias to make things consistent -- MPD

EXAMPLES = '''
# Basic mysql provisioning example
- rds:
    command: create
    instance_name: new-database
    db_engine: MySQL
    size: 10
    instance_type: db.m1.small
    username: mysql_admin
    password: 1nsecure
    tags:
      Environment: testing
      Application: cms

# Create a read-only replica and wait for it to become available
- rds:
    command: replicate
    instance_name: new-database-replica
    source_instance: new_database
    wait: yes
    wait_timeout: 600

# Delete an instance, but create a snapshot before doing so
- rds:
    command: delete
    instance_name: new-database
    snapshot: new_database_snapshot

# Get facts about an instance
- rds:
    command: facts
    instance_name: new-database
    register: new_database_facts

# Rename an instance and wait for the change to take effect
- rds:
    command: modify
    instance_name: new-database
    new_instance_name: renamed-database
    wait: yes
'''

import sys
import time

try:
    import boto.rds
except ImportError:
    print "failed=True msg='boto required for this module'"
    sys.exit(1)

try:
    import boto.rds2
    has_rds2 = True
except ImportError:
    has_rds2 = False


class RDSException(Exception):
    def __init__(self, exc):
        if hasattr(exc, 'error_message') and exc.error_message:
            self.message = exc.error_message
            self.code = exc.error_code
        elif hasattr(exc, 'body') and 'Error' in exc.body:
            self.message = exc.body['Error']['Message']
            self.code = exc.body['Error']['Code']
        else:
            self.message = str(exc)
            self.code = 'Unknown Error'


class RDSConnection:
    def __init__(self, module, region, **aws_connect_params):
        try:
            self.connection  = connect_to_aws(boto.rds, region, **aws_connect_params)
        except boto.exception.BotoServerError, e:
             module.fail_json(msg=e.error_message)

    def get_db_instance(self, instancename):
        try:
            return RDSDBInstance(self.connection.get_all_dbinstances(instancename)[0])
        except boto.exception.BotoServerError, e:
            return None

    def get_db_snapshot(self, snapshotid):
        try: 
            return RDSSnapshot(self.connection.get_all_dbsnapshots(snapshot_id=snapshotid)[0])
        except boto.exception.BotoServerError, e:
            return None

    def create_db_instance(self, instance_name, size, instance_class, db_engine,
            username, password, **params):
        params['engine'] = db_engine
        try:
            result = self.connection.create_dbinstance(instance_name, size, instance_class,
                    username, password, **params)
            return RDSDBInstance(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)

    def create_db_instance_read_replica(self, instance_name, source_instance, **params):
        try:
            result = self.connection.createdb_instance_read_replica(instance_name, source_instance, **params)
            return RDSDBInstance(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)

    def delete_db_instance(self, instance_name, **params):
        try:
            result = self.connection.delete_dbinstance(instance_name, **params)
            return RDSDBInstance(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)

    def delete_db_snapshot(self, snapshot):
        try:
            result = self.connection.delete_dbsnapshot(snapshot)
            return RDSSnapshot(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)

    def modify_db_instance(self, instance_name, **params):
        try:
            result = self.connection.modify_dbinstance(instance_name, **params)
            return RDSDBInstance(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)

    def restore_db_instance_from_db_snapshot(self, instance_name, snapshot, instance_type, **params):
        try:
            result = self.connection.restore_dbinstance_from_dbsnapshot(snapshot, instance_name, instance_type, **params)
            return RDSDBInstance(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)

    def create_db_snapshot(self, snapshot, instance_name, **params):
        try:
            result = self.connection.create_dbsnapshot(snapshot, instance_name)
            return RDSSnapshot(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)

    def promote_read_replica(self, instance_name, **params):
        try:
            result = self.connection.promote_read_replica(instance_name, **params)
            return RDSDBInstance(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)


class RDS2Connection:
    def __init__(self, module, region, **aws_connect_params):
        try:
            self.connection  = connect_to_aws(boto.rds2, region, **aws_connect_params)
        except boto.exception.BotoServerError, e:
             module.fail_json(msg=e.error_message)

    def get_db_instance(self, instancename):
        try:
            dbinstances = self.connection.describe_db_instances(db_instance_identifier=instancename)['DescribeDBInstancesResponse']['DescribeDBInstancesResult']['DBInstances']
            result =  RDS2DBInstance(dbinstances[0])
            return result
        except boto.rds2.exceptions.DBInstanceNotFound, e:
            return None
        except Exception, e:
            raise e

    def get_db_snapshot(self, snapshotid):
        try:
            snapshots = self.connection.describe_db_snapshots(db_snapshot_identifier=snapshotid, snapshot_type='manual')['DescribeDBSnapshotsResponse']['DescribeDBSnapshotsResult']['DBSnapshots']
            result = RDS2Snapshot(snapshots[0])
            return result
        except boto.rds2.exceptions.DBSnapshotNotFound, e:
            return None

    def create_db_instance(self, instance_name, size, instance_class, db_engine,
            username, password, **params):
        try:
            result = self.connection.create_db_instance(instance_name, size, instance_class,
                db_engine, username, password, **params)['CreateDBInstanceResponse']['CreateDBInstanceResult']['DBInstance']
            return RDS2DBInstance(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)

    def create_db_instance_read_replica(self, instance_name, source_instance, **params):
        try:
            result = self.connection.create_db_instance_read_replica(instance_name, source_instance, **params)['CreateDBInstanceReadReplicaResponse']['CreateDBInstanceReadReplicaResult']['DBInstance']
            return RDS2DBInstance(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)

    def delete_db_instance(self, instance_name, **params):
        try:
            result = self.connection.delete_db_instance(instance_name, **params)['DeleteDBInstanceResponse']['DeleteDBInstanceResult']['DBInstance']
            return RDS2DBInstance(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)

    def delete_db_snapshot(self, snapshot):
        try:
            result = self.connection.delete_db_snapshot(snapshot)['DeleteDBSnapshotResponse']['DeleteDBSnapshotResult']['DBSnapshot']
            return RDS2Snapshot(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)

    def modify_db_instance(self, instance_name, **params):
        try:
            result = self.connection.modify_db_instance(instance_name, **params)['ModifyDBInstanceResponse']['ModifyDBInstanceResult']['DBInstance']
            return RDS2DBInstance(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)

    def restore_db_instance_from_db_snapshot(self, instance_name, snapshot, instance_type, **params):
        try:
            result = self.connection.restore_db_instance_from_db_snapshot(instance_name, snapshot, **params)['RestoreDBInstanceFromDBSnapshotResponse']['RestoreDBInstanceFromDBSnapshotResult']['DBInstance']
            return RDS2DBInstance(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)

    def create_db_snapshot(self, snapshot, instance_name, **params):
        try:
            result = self.connection.create_db_snapshot(snapshot, instance_name, **params)['CreateDBSnapshotResponse']['CreateDBSnapshotResult']['DBSnapshot']
            return RDS2Snapshot(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)

    def promote_read_replica(self, instance_name, **params):
        try:
            result = self.connection.promote_read_replica(instance_name, **params)['PromoteReadReplicaResponse']['PromoteReadReplicaResult']['DBInstance']
            return RDS2DBInstance(result)
        except boto.exception.BotoServerError, e:
            raise RDSException(e)


class RDSDBInstance:
    def __init__(self, dbinstance):
        self.instance = dbinstance
        self.name = dbinstance.id
        self.status = dbinstance.status

    def get_data(self):
        d = {
            'id'                 : self.name,
            'create_time'        : self.instance.create_time,
            'status'             : self.status,
            'availability_zone'  : self.instance.availability_zone,
            'backup_retention'   : self.instance.backup_retention_period,
            'backup_window'      : self.instance.preferred_backup_window,
            'maintenance_window' : self.instance.preferred_maintenance_window,
            'multi_zone'         : self.instance.multi_az,
            'instance_type'      : self.instance.instance_class,
            'username'           : self.instance.master_username,
            'iops'               : self.instance.iops
            }

        # Endpoint exists only if the instance is available
        if self.status == 'available':
            d["endpoint"] = self.instance.endpoint[0]
            d["port"] = self.instance.endpoint[1]
            if self.instance.vpc_security_groups is not None:
                d["vpc_security_groups"] = ','.join(x.vpc_group for x in self.instance.vpc_security_groups)
            else:
                d["vpc_security_groups"] = None
        else:
            d["endpoint"] = None
            d["port"] = None
            d["vpc_security_groups"] = None

        # ReadReplicaSourceDBInstanceIdentifier may or may not exist
        try:
            d["replication_source"] = self.instance.ReadReplicaSourceDBInstanceIdentifier
        except Exception, e:
            d["replication_source"] = None
        return d




class RDS2DBInstance:
    def __init__(self, dbinstance):
        self.instance = dbinstance
        if 'DBInstanceIdentifier' not in dbinstance:
            self.name = None
        else:
            self.name = self.instance.get('DBInstanceIdentifier')
        self.status = self.instance.get('DBInstanceStatus')

    def get_data(self):
        d = {
            'id': self.name,
            'create_time': self.instance['InstanceCreateTime'],
            'status': self.status,
            'availability_zone': self.instance['AvailabilityZone'],
            'backup_retention': self.instance['BackupRetentionPeriod'],
            'maintenance_window': self.instance['PreferredMaintenanceWindow'],
            'multi_zone': self.instance['MultiAZ'],
            'instance_type': self.instance['DBInstanceClass'],
            'username': self.instance['MasterUsername'],
            'iops': self.instance['Iops'],
            'replication_source': self.instance['ReadReplicaSourceDBInstanceIdentifier']
        }
        if self.instance["VpcSecurityGroups"] is not None:
            d['vpc_security_groups'] = ','.join(x['VpcSecurityGroupId'] for x in self.instance['VpcSecurityGroups'])
        if self.status == 'available':
            d['endpoint'] = self.instance["Endpoint"]["Address"]
            d['port'] = self.instance["Endpoint"]["Port"]
        else:
            d['endpoint'] = None
            d['port'] = None

        return d


class RDSSnapshot:
    def __init__(self, snapshot):
        self.snapshot = snapshot
        self.name = snapshot.id
        self.status = snapshot.status

    def get_data(self):
        d = {
            'id'                 : self.name,
            'create_time'        : self.snapshot.snapshot_create_time,
            'status'             : self.status,
            'availability_zone'  : self.snapshot.availability_zone,
            'instance_id'        : self.snapshot.instance_id,
            'instance_created'   : self.snapshot.instance_create_time,
        }
        # needs boto >= 2.21.0
        if hasattr(self.snapshot, 'snapshot_type'):
            d["snapshot_type"] = self.snapshot.snapshot_type
        if hasattr(self.snapshot, 'iops'):
            d["iops"] = self.snapshot.iops
        return d


class RDS2Snapshot:
    def __init__(self, snapshot):
        if 'DeleteDBSnapshotResponse' in snapshot:
            self.snapshot = snapshot['DeleteDBSnapshotResponse']['DeleteDBSnapshotResult']['DBSnapshot']
        else:
            self.snapshot = snapshot
        self.name = self.snapshot.get('DBSnapshotIdentifier')
        self.status = self.snapshot.get('Status')

    def get_data(self):
        d = {
            'id'                 : self.name,
            'create_time'        : self.snapshot['SnapshotCreateTime'],
            'status'             : self.status,
            'availability_zone'  : self.snapshot['AvailabilityZone'],
            'instance_id'        : self.snapshot['DBInstanceIdentifier'],
            'instance_created'   : self.snapshot['InstanceCreateTime'],
            'snapshot_type'      : self.snapshot['SnapshotType'],
            'iops'               : self.snapshot['Iops'],
        }
        return d


def await_resource(conn, resource, status, module):
    wait_timeout = module.params.get('wait_timeout') + time.time()
    while wait_timeout > time.time() and resource.status != status:
        time.sleep(5)
        if wait_timeout <= time.time():
            module.fail_json(msg="Timeout waiting for resource %s" % resource.id)
        if module.params.get('command') == 'snapshot':
            # Temporary until all the rds2 commands have their responses parsed
            if resource.name is None:
                module.fail_json(msg="Problem with snapshot %s" % resource.snapshot)
            resource = conn.get_db_snapshot(resource.name)
        else:
            # Temporary until all the rds2 commands have their responses parsed
            if resource.name is None:
                module.fail_json(msg="Problem with instance %s" % resource.instance)
            resource = conn.get_db_instance(resource.name)
    return resource


def create_db_instance(module, conn):
    subnet = module.params.get('subnet')
    required_vars = ['instance_name', 'db_engine', 'size', 'instance_type', 'username', 'password']
    valid_vars = ['backup_retention', 'backup_window',
                  'character_set_name', 'db_name', 'engine_version',
                  'instance_type', 'iops', 'license_model', 'maint_window',
                  'multi_zone', 'option_group', 'parameter_group','port',
                  'subnet', 'upgrade', 'zone']
    if module.params.get('subnet'):
        valid_vars.append('vpc_security_groups')
    else:
        valid_vars.append('security_groups')
    if has_rds2:
        valid_vars.extend(['publicly_accessible', 'tags'])
    params = validate_parameters(required_vars, valid_vars, module)
    instance_name = module.params.get('instance_name')

    result = conn.get_db_instance(instance_name)
    if result:
        changed = False
    else:
        try:
            result = conn.create_db_instance(instance_name, module.params.get('size'),
                    module.params.get('instance_type'), module.params.get('db_engine'),
                    module.params.get('username'), module.params.get('password'), **params)
            changed = True
        except RDSException, e:
            module.fail_json(msg="failed to create instance: %s" % e.message)

    if module.params.get('wait'):
        resource = await_resource(conn, result, 'available', module)
    else:
        resource = conn.get_db_instance(instance_name)

    module.exit_json(changed=changed, instance=resource.get_data())


def replicate_db_instance(module, conn):
    required_vars = ['instance_name', 'source_instance']
    valid_vars = ['instance_type', 'port', 'upgrade', 'zone']
    if has_rds2:
        valid_vars.extend(['iops', 'option_group', 'publicly_accessible', 'tags'])
    params = validate_parameters(required_vars, valid_vars, module)
    instance_name = module.params.get('instance_name')
    source_instance = module.params.get('source_instance')

    result = conn.get_db_instance(instance_name)
    if result:
        changed = False
    else:
        try:
            result = conn.create_db_instance_read_replica(instance_name, source_instance, **params)
            changed = True
        except RDSException, e:
            module.fail_json(msg="failed to create replica instance: %s " % e.message)

    if module.params.get('wait'):
        resource = await_resource(conn, result, 'available', module)
    else:
        resource = conn.get_db_instance(instance_name)

    module.exit_json(changed=changed, instance=resource.get_data())


def delete_db_instance_or_snapshot(module, conn):
    required_vars = []
    valid_vars = ['instance_name', 'snapshot', 'skip_final_snapshot']
    params = validate_parameters(required_vars, valid_vars, module)
    instance_name = module.params.get('instance_name')
    snapshot = module.params.get('snapshot')

    if not instance_name:
        result = conn.get_db_snapshot(snapshot)
    else:
        result = conn.get_db_instance(instance_name)
    if not result:
        module.exit_json(changed=False)
    if result.status == 'deleting':
        module.exit_json(changed=False)
    try:
        if instance_name:
            if snapshot:
                params["skip_final_snapshot"] = False
                params["final_snapshot_id"] = snapshot
            else:
                params["skip_final_snapshot"] = True
            result = conn.delete_db_instance(instance_name, **params)
        else:
            result = conn.delete_db_snapshot(snapshot)
    except RDSException, e:
        module.fail_json(msg="failed to delete instance: %s" % e.message)

    # If we're not waiting for a delete to complete then we're all done
    # so just return
    if not module.params.get('wait'):
        module.exit_json(changed=True)
    try:
        resource = await_resource(conn, result, 'deleted', module)
        module.exit_json(changed=True)
    except RDSException, e:
        if e.code == 'DBInstanceNotFound':
            module.exit_json(changed=True)
        else:
            module.fail_json(msg=e.message)
    except Exception, e:
        module.fail_json(msg=str(e))


def facts_db_instance_or_snapshot(module, conn):
    required_vars = []
    valid_vars = ['instance_name', 'snapshot']
    params = validate_parameters(required_vars, valid_vars, module)
    instance_name = module.params.get('instance_name')
    snapshot = module.params.get('snapshot')

    if instance_name and snapshot:
        module.fail_json(msg="facts must be called with either instance_name or snapshot, not both")
    if instance_name:
        resource = conn.get_db_instance(instance_name)
        if not resource:
            module.fail_json(msg="DB Instance %s does not exist" % instance_name)
    if snapshot:
        resource = conn.get_db_snapshot(snapshot)
        if not resource:
            module.fail_json(msg="DB snapshot %s does not exist" % snapshot)

    module.exit_json(changed=False, instance=resource.get_data())


def modify_db_instance(module, conn):
    required_vars = ['instance_name']
    valid_vars = ['apply_immediately', 'backup_retention', 'backup_window',
                  'db_name', 'engine_version', 'instance_type', 'iops', 'license_model',
                  'maint_window', 'multi_zone', 'new_instance_name',
                  'option_group', 'parameter_group', 'password', 'size', 'upgrade']

    params = validate_parameters(required_vars, valid_vars, module)
    instance_name = module.params.get('instance_name')
    new_instance_name = module.params.get('new_instance_name')

    try:
        result = conn.modify_db_instance(instance_name, **params)
    except RDSException, e:
        module.fail_json(msg=e.message)
    if params.get('apply_immediately'):
        if new_instance_name:
            # Wait until the new instance name is valid
            new_instance = None
            while not new_instance:
                new_instance = conn.get_db_instance(new_instance_name)
                time.sleep(5)

            # Found instance but it briefly flicks to available
            # before rebooting so let's wait until we see it rebooting
            # before we check whether to 'wait'
            result = await_resource(conn, new_instance, 'rebooting', module)

    if module.params.get('wait'):
        resource = await_resource(conn, result, 'available', module)
    else:
        resource = conn.get_db_instance(instance_name)

    # guess that this changed the DB, need a way to check
    module.exit_json(changed=True, instance=resource.get_data())


def promote_db_instance(module, conn):
    required_vars = ['instance_name']
    valid_vars = ['backup_retention', 'backup_window']
    params = validate_parameters(required_vars, valid_vars, module)
    instance_name = module.params.get('instance_name')
    
    result = conn.get_db_instance(instance_name)
    if result.get_data().get('replication_source'):
        changed = False
    else:
        try:
            result = conn.promote_read_replica(instance_name, **params)
        except RDSException, e:
            module.fail_json(msg=e.message)

    if module.params.get('wait'):
        resource = await_resource(conn, result, 'available', module)
    else:
        resource = conn.get_db_instance(instance_name)

    module.exit_json(changed=changed, instance=resource.get_data())


def snapshot_db_instance(module, conn):
    required_vars = ['instance_name', 'snapshot']
    valid_vars = ['tags']
    params = validate_parameters(required_vars, valid_vars, module)
    instance_name = module.params.get('instance_name')
    snapshot = module.params.get('snapshot')
    changed = False
    result = conn.get_db_snapshot(snapshot)
    if not result:
        try:
            result = conn.create_db_snapshot(snapshot, instance_name, **params)
            changed = True
        except RDSException, e:
            module.fail_json(msg=e.message)

    if module.params.get('wait'):
        resource = await_resource(conn, result, 'available', module)
    else:
        resource = conn.get_db_snapshot(snapshot)

    module.exit_json(changed=changed, snapshot=resource.get_data())


def restore_db_instance(module, conn):
    required_vars = ['instance_name', 'snapshot']
    valid_vars = ['db_name', 'iops', 'license_model', 'multi_zone',
                  'option_group', 'port', 'publicly_accessible',
                  'subnet', 'tags', 'upgrade', 'zone']
    if has_rds2:
        valid_vars.append('instance_type')
    else:
        required_vars.append('instance_type')
    params = validate_parameters(required_vars, valid_vars, module)
    instance_name = module.params.get('instance_name')
    instance_type = module.params.get('instance_type')
    snapshot = module.params.get('snapshot')

    changed = False
    result = conn.get_db_instance(instance_name)
    if not result:
        try:
            result = conn.restore_db_instance_from_db_snapshot(instance_name, snapshot, instance_type, **params)
            changed = True
        except RDSException, e:
            module.fail_json(msg=e.message)

    if module.params.get('wait'):
        resource = await_resource(conn, result, 'available', module)
    else:
        resource = conn.get_db_instance(instance_name)

    module.exit_json(changed=changed, instance=resource.get_data())


def validate_parameters(required_vars, valid_vars, module):
    command = module.params.get('command')
    for v in required_vars:
        if not module.params.get(v):
            module.fail_json(msg="Parameter %s required for %s command" % (v, command))

    # map to convert rds module options to boto rds and rds2 options
    optional_params = {
            'port': 'port',
            'db_name': 'db_name',
            'zone': 'availability_zone',
            'maint_window': 'preferred_maintenance_window',
            'backup_window': 'preferred_backup_window',
            'backup_retention': 'backup_retention_period',
            'multi_zone': 'multi_az',
            'engine_version': 'engine_version',
            'upgrade': 'auto_minor_version_upgrade',
            'subnet': 'db_subnet_group_name',
            'license_model': 'license_model',
            'option_group': 'option_group_name',
            'iops': 'iops',
            'new_instance_name': 'new_instance_id',
            'apply_immediately': 'apply_immediately',
    }
    # map to convert rds module options to boto rds options
    optional_params_rds = {
            'db_engine': 'engine',
            'password': 'master_password',
            'parameter_group': 'param_group',
            'instance_type': 'instance_class',
    }
    # map to convert rds module options to boto rds2 options
    optional_params_rds2 = {
            'tags': 'tags',
            'publicly_accessible': 'publicly_accessible',
            'parameter_group': 'db_parameter_group_name',
            'character_set_name': 'character_set_name',
            'instance_type': 'db_instance_class',
            'password': 'master_user_password',
            'new_instance_name': 'new_db_instance_identifier',
    }
    if has_rds2:
        optional_params.update(optional_params_rds2)
        sec_group = 'db_security_groups'
    else:
        optional_params.update(optional_params_rds)
        sec_group = 'security_groups'
        # Check for options only supported with rds2
        for k in set(optional_params_rds2.keys()) - set(optional_params_rds.keys()):
            if module.params.get(k):
                module.fail_json(msg="Parameter %s requires boto.rds (boto >= 2.26.0)" % k)

    params = {}
    for (k, v) in optional_params.items():
        if module.params.get(k) and k not in required_vars:
            if k in valid_vars:
                params[v] = module.params[k]
            else:
                module.fail_json(msg="Parameter %s is not valid for %s command" % (k, command))

    if module.params.get('security_groups'):
        params[sec_group] = module.params.get('security_groups').split(',')

    vpc_groups = module.params.get('vpc_security_groups')
    if vpc_groups:
        if has_rds2:
            params['vpc_security_group_ids'] = vpc_groups
        else:
            groups_list = []
            for x in vpc_groups:
                groups_list.append(boto.rds.VPCSecurityGroupMembership(vpc_group=x))
            params['vpc_security_groups'] = groups_list

    # Convert tags dict to list of tuples that rds2 expects
    if 'tags' in params:
        params['tags'] = module.params['tags'].items()
    return params


def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(
            command           = dict(choices=['create', 'replicate', 'delete', 'facts', 'modify', 'promote', 'snapshot', 'restore'], required=True),
            instance_name     = dict(required=False),
            source_instance   = dict(required=False),
            db_engine         = dict(choices=['MariaDB', 'MySQL', 'oracle-se1', 'oracle-se', 'oracle-ee', 'sqlserver-ee', 'sqlserver-se', 'sqlserver-ex', 'sqlserver-web', 'postgres'], required=False),
            size              = dict(required=False),
            instance_type     = dict(aliases=['type'], required=False),
            username          = dict(required=False),
            password          = dict(no_log=True, required=False),
            db_name           = dict(required=False),
            engine_version    = dict(required=False),
            parameter_group   = dict(required=False),
            license_model     = dict(choices=['license-included', 'bring-your-own-license', 'general-public-license'], required=False),
            multi_zone        = dict(type='bool', default=False),
            iops              = dict(required=False), 
            security_groups   = dict(required=False),
            vpc_security_groups = dict(type='list', required=False),
            port              = dict(required=False),
            upgrade           = dict(type='bool', default=False),
            option_group      = dict(required=False),
            maint_window      = dict(required=False),
            backup_window     = dict(required=False),
            backup_retention  = dict(required=False), 
            zone              = dict(aliases=['aws_zone', 'ec2_zone'], required=False),
            subnet            = dict(required=False),
            wait              = dict(type='bool', default=False),
            wait_timeout      = dict(type='int', default=300),
            snapshot          = dict(required=False),
            apply_immediately = dict(type='bool', default=False),
            new_instance_name = dict(required=False),
            tags              = dict(type='dict', required=False),
            publicly_accessible = dict(required=False),
            character_set_name = dict(required=False),
        )
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    invocations = {
            'create': create_db_instance,
            'replicate': replicate_db_instance,
            'delete': delete_db_instance_or_snapshot,
            'facts': facts_db_instance_or_snapshot,
            'modify': modify_db_instance,
            'promote': promote_db_instance,
            'snapshot': snapshot_db_instance,
            'restore': restore_db_instance,
    }

    region, ec2_url, aws_connect_params = get_aws_connection_info(module)
    if not region:
        module.fail_json(msg="region not specified and unable to determine region from EC2_REGION.")

    # connect to the rds endpoint
    if has_rds2:
        conn = RDS2Connection(module, region, **aws_connect_params)
    else:
        conn = RDSConnection(module, region, **aws_connect_params)

    invocations[module.params.get('command')](module, conn)
        
# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

main()
