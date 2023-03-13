data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}


resource "aws_instance" "envapp-ec2" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.envapp-pub.id
  vpc_security_group_ids = ["${aws_security_group.allow-all.id}"]
  key_name               = aws_key_pair.mykey.key_name
  tags = {
    Name = "envapp-ec2"
  }
}