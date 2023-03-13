resource "aws_vpc" "envapp-vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = false
  enable_dns_support   = true
  instance_tenancy     = "default"

  tags = {
    "Name" : "envapp-vpc"
  }
}
resource "aws_subnet" "envapp-pub" {
  vpc_id            = aws_vpc.envapp-vpc.id
  cidr_block        = "10.0.0.0/24"
  availability_zone = "ap-northeast-3a"
  tags = {
    "Name" : "envapp-pub"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.envapp-vpc.id
  tags = {
    "Name" = "internet_gateway"
  }
}

resource "aws_eip" "envapp-eip" {
  instance = aws_instance.envapp-ec2.id
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_default_route_table" "public_rt" {
  default_route_table_id = aws_vpc.envapp-vpc.default_route_table_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "public route table"
  }
}

resource "aws_route_table_association" "public_rta_a" {
  subnet_id      = aws_subnet.envapp-pub.id
  route_table_id = aws_default_route_table.public_rt.id
}

resource "aws_default_network_acl" "vpc_network_acl" {
  default_network_acl_id = aws_vpc.envapp-vpc.default_network_acl_id

  egress {
    protocol   = "-1"
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  ingress {
    protocol   = "-1"
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  tags = {
    Name = "network acl"
  }
}