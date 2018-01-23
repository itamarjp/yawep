# yum -y install ansible

copy ansible.cfg to ~/.ansible.cfg

copy hosts to ~/hosts and adjust it

run

$ ansible-playbook install.yml
$ ansible-playbook enable.yml

alternative you can run booth of them in one command

$ ansible-playbook -k all.yml



