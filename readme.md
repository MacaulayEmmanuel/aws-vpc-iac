# AWS VPC Network Infrastructure - Pulumi IaC

## Project Overview

This project automates the deployment of a network infrastructure in AWS using Pulumi and Python. It provisions:
- A Virtual Private Cloud (VPC)
- Public and Private Subnets
- NAT Gateways for Internet access from private subnets
- Internet Gateway for public subnets
- Route Tables and Network ACLs for traffic control

This documentation will guide you through setting up the project, configuring AWS, and deploying the infrastructure.

## Features

- **VPC**: Creates a VPC with DNS support and hostnames enabled.
- **Subnets**: 2 public subnets and 2 private subnets in different availability zones.
- **NAT Gateway**: Ensures private subnets can access the internet.
- **Internet Gateway**: Allows internet access for resources in public subnets.
- **Route Tables**: Controls traffic within the VPC and from/to the internet.
- **Network ACLs**: Provides an additional layer of security at the subnet level.

---

## Prerequisites

1. **AWS Account**: You must have an AWS account.
2. **AWS CLI**: Install and configure the AWS CLI:
   ```bash
   aws configure
