import pulumi
import pulumi_aws as aws
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Create a VPC
    vpc = aws.ec2.Vpc("my-vpc",
                      cidr_block="10.0.0.0/16",
                      enable_dns_support=True,
                      enable_dns_hostnames=True,
                      tags={"Name": "my-vpc"})
    logger.info("VPC created with ID: %s", vpc.id)

    # Create an Internet Gateway
    igw = aws.ec2.InternetGateway("my-igw",
                                  vpc_id=vpc.id,
                                  tags={"Name": "my-igw"})
    logger.info("Internet Gateway created with ID: %s", igw.id)

    # Create Route Table for Public Subnets
    public_route_table = aws.ec2.RouteTable("public-route-table",
                                            vpc_id=vpc.id,
                                            routes=[aws.ec2.RouteTableRouteArgs(
                                                cidr_block="0.0.0.0/0",
                                                gateway_id=igw.id,
                                            )],
                                            tags={"Name": "public-route-table"})
    logger.info("Public Route Table created with ID: %s", public_route_table.id)

    # Create public subnets
    public_subnet1 = aws.ec2.Subnet("public-subnet1",
                                    vpc_id=vpc.id,
                                    cidr_block="10.0.1.0/24",
                                    availability_zone="us-west-2a",
                                    map_public_ip_on_launch=True,
                                    tags={"Name": "public-subnet1"})
    logger.info("Public Subnet 1 created with ID: %s", public_subnet1.id)

    public_subnet2 = aws.ec2.Subnet("public-subnet2",
                                    vpc_id=vpc.id,
                                    cidr_block="10.0.2.0/24",
                                    availability_zone="us-west-2b",
                                    map_public_ip_on_launch=True,
                                    tags={"Name": "public-subnet2"})
    logger.info("Public Subnet 2 created with ID: %s", public_subnet2.id)

    # Associate public subnets with route table
    public_assoc1 = aws.ec2.RouteTableAssociation("public-assoc1",
                                                  subnet_id=public_subnet1.id,
                                                  route_table_id=public_route_table.id)
    public_assoc2 = aws.ec2.RouteTableAssociation("public-assoc2",
                                                  subnet_id=public_subnet2.id,
                                                  route_table_id=public_route_table.id)
    logger.info("Public subnets associated with the route table.")

    # Create NAT Gateways
    eip1 = aws.ec2.Eip("eip1", tags={"Name": "eip1"}, vpc=True)
    nat_gw1 = aws.ec2.NatGateway("nat-gw1",
                                 allocation_id=eip1.id,
                                 subnet_id=public_subnet1.id,
                                 tags={"Name": "nat-gw1"})
    logger.info("NAT Gateway 1 created with ID: %s", nat_gw1.id)

    eip2 = aws.ec2.Eip("eip2", tags={"Name": "eip2"}, vpc=True)
    nat_gw2 = aws.ec2.NatGateway("nat-gw2",
                                 allocation_id=eip2.id,
                                 subnet_id=public_subnet2.id,
                                 tags={"Name": "nat-gw2"})
    logger.info("NAT Gateway 2 created with ID: %s", nat_gw2.id)

    # Create Route Table for Private Subnets
    private_route_table = aws.ec2.RouteTable("private-route-table",
                                             vpc_id=vpc.id,
                                             routes=[aws.ec2.RouteTableRouteArgs(
                                                 cidr_block="0.0.0.0/0",
                                                 nat_gateway_id=nat_gw1.id,  # route through nat_gw1 for this example
                                             )],
                                             tags={"Name": "private-route-table"})
    logger.info("Private Route Table created with ID: %s", private_route_table.id)

    # Create private subnets
    private_subnet1 = aws.ec2.Subnet("private-subnet1",
                                     vpc_id=vpc.id,
                                     cidr_block="10.0.3.0/24",
                                     availability_zone="us-west-2a",
                                     tags={"Name": "private-subnet1"})
    logger.info("Private Subnet 1 created with ID: %s", private_subnet1.id)

    private_subnet2 = aws.ec2.Subnet("private-subnet2",
                                     vpc_id=vpc.id,
                                     cidr_block="10.0.4.0/24",
                                     availability_zone="us-west-2b",
                                     tags={"Name": "private-subnet2"})
    logger.info("Private Subnet 2 created with ID: %s", private_subnet2.id)

    # Associate private subnets with route table
    private_assoc1 = aws.ec2.RouteTableAssociation("private-assoc1",
                                                   subnet_id=private_subnet1.id,
                                                   route_table_id=private_route_table.id)
    private_assoc2 = aws.ec2.RouteTableAssociation("private-assoc2",
                                                   subnet_id=private_subnet2.id,
                                                   route_table_id=private_route_table.id)
    logger.info("Private subnets associated with the route table.")

    # Create Network ACLs
    nacl = aws.ec2.NetworkAcl("my-nacl",
                              vpc_id=vpc.id,
                              egress=[aws.ec2.NetworkAclEgressArgs(
                                  protocol="-1",
                                  rule_no=100,
                                  action="allow",
                                  cidr_block="0.0.0.0/0",
                                  from_port=0,
                                  to_port=0,
                              )],
                              ingress=[aws.ec2.NetworkAclIngressArgs(
                                  protocol="-1",
                                  rule_no=100,
                                  action="allow",
                                  cidr_block="0.0.0.0/0",
                                  from_port=0,
                                  to_port=0,
                              )],
                              tags={"Name": "my-nacl"})
    logger.info("Network ACL created with ID: %s", nacl.id)

    # Apply Network ACL to Subnets
    nacl_assoc1 = aws.ec2.NetworkAclAssociation("nacl-assoc1",
                                                subnet_id=public_subnet1.id,
                                                network_acl_id=nacl.id)
    nacl_assoc2 = aws.ec2.NetworkAclAssociation("nacl-assoc2",
                                                subnet_id=public_subnet2.id,
                                                network_acl_id=nacl.id)
    nacl_assoc3 = aws.ec2.NetworkAclAssociation("nacl-assoc3",
                                                subnet_id=private_subnet1.id,
                                                network_acl_id=nacl.id)
    nacl_assoc4 = aws.ec2.NetworkAclAssociation("nacl-assoc4",
                                                subnet_id=private_subnet2.id,
                                                network_acl_id=nacl.id)
    logger.info("Network ACL applied to all subnets.")

    # Export VPC ID
    pulumi.export("vpc_id", vpc.id)

    # Export subnet IDs
    pulumi.export("public_subnet1_id", public_subnet1.id)
    pulumi.export("public_subnet2_id", public_subnet2.id)
    pulumi.export("private_subnet1_id", private_subnet1.id)
    pulumi.export("private_subnet2_id", private_subnet2.id)

    # Export NAT Gateway IDs
    pulumi.export("nat_gw1_id", nat_gw1.id)
    pulumi.export("nat_gw2_id", nat_gw2.id)

except Exception as e:
    logger.error("An error occurred: %s", str(e))
