import pulumi
import pulumi_aws as aws


vpc = aws.ec2.get_vpc(default=True)

group = aws.ec2.SecurityGroup(
    "Se-app",
    description="anything man",
    ingress=[
        {
            "protocol": "tcp",
            "from_port":22,
            "to_port":22,
            "cidr_blocks": ["0.0.0.0/0"],
        }
    ]
)

ami = aws.ec2.get_ami(
most_recent="false",
    owners=["099720109477"],
    filters=[{"name": "image-id", "values": ["ami-052efd3df9dad4825*"]}]
)


user_data = """"
#!/bin/bash
uname -n > index.html
nohup python -m SimpleHTTPServer 80 &
"""

instance = aws.ec2.Instance(
    "Deora-test",
    instance_type="t2.micro",
    vpc_security_group_ids=[group.name],
    ami=ami.id,
    key_name="acer1",
    user_data=user_data,
)

#deployer = aws.ec2.KeyPair("deployer",
    #key_name="acer4",
    #public_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD3F6tyPEFEzV0LX3X8BsXdMsQz1x2cEikKDEY0aIj41qgxMCP/iteneqXSIFZBp5vizPvaoIR3Um9xK7PGoW8giupGn+EPuxIA4cDM4vzOqOkiMPhz5XK0whEjkVzTo4+S0puvDZuwIsdiW9mxhJc7tgBNL0cYlWSYVkz4G/fslNfRPW5mYAM49f4fhtxPb5ok4Q2Lg9dPKVHO/Bgeu5woMc7RY0p1ej6D4CKFE6lymSDJpW0YHX/wqE9+cfEauh7xZcG0q9t2ta6F6fmX0agvpFyZo8aFbXeUBr7osSCJNgvavWbM/06niWrOvYX2xwWdhXmXSrbX8ZbabVohBK41 email@example.com",
    #opts=pulumi.ResourceOptions(protect=False)
                           #)

pulumi.export("se-app-ip", instance.public_ip)