##Kops cluster setup 
```
 
export AWS_REGION="ap-south-1"

export NODE_SIZE="t3.medium"

export MASTER_SIZE="t3.medium"

export ZONES="ap-south-1a,ap-south-1b,ap-south-1c"

export MASTER_ZONES="ap-south-1a"

export KOPS_STATE_STORE="s3://<bucket-name>"

export MASTER_COUNT="1"

export NODE_COUNT="1"

export TOPOLOGY="private"

export ELB="public"

export VPCID="<vpc-ip>"

export PROVIDER=aws

export LABELS="owner=devops,Project=k8s_cluster"

export SUBNET_IDS="subnet-xxxx,subnet-yyyy,subnet-zzzz"

export UTILITY_SUBNETS="subnet-xxxx,subnet-yyyy,subnet-zzzz"

export UTILITY_CIDRS="10.0.0.0/20","10.0.16.0/20","10.0.32.0/20"

export NETWORK_CIDR=10.0.0.0/16

export SUBNET_CIDR="10.0.128.0/20","10.0.144.0/20","10.0.160.0/20"

export NAME=example.k8s.local

export SECURITY_GROUPS="<security-group-id>"

export NODE_VOLUME="20"


kops create cluster \

--cloud=${PROVIDER} \

--control-plane-count=${MASTER_COUNT} \

--node-count=${NODE_COUNT} \

--zones=${ZONES} \

--networking=calico \

--network-cidr=${NETWORK_CIDR} \

--network-id=${VPCID} \

--node-size=${NODE_SIZE} \

--control-plane-size=${MASTER_SIZE} \

--control-plane-zones=${MASTER_ZONES} \

--cloud-labels=${LABELS} \

--subnets=${SUBNET_IDS} \

--utility-subnets=${UTILITY_SUBNETS} \

--name=${NAME} \

--associate-public-ip=false \

--control-plane-security-groups=${SECURITY_GROUPS} \

--ssh-public-key=~/.ssh/id_ed25519.pub \

--state=${KOPS_STATE_STORE} \

--node-volume-size=${NODE_VOLUME} \

--control-plane-volume-size=40 \

--dns=none \

--topology=${TOPOLOGY} \

--api-loadbalancer-type=${ELB}

```