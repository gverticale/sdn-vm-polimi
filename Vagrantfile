## Vagrantfile for SDN class Politecnico di Milano

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "bento/ubuntu-20.04"
    # config.vm.box = "tknerr/ubuntu2004-desktop"

    ## Guest Config
    config.vm.hostname = "polimi-sdn"

    # onos gui
    config.vm.network "forwarded_port", guest:8181, host:8181

    # ryu gui
    config.vm.network "forwarded_port", guest:8080, host:8080

    # mininet dashboard
    config.vm.network "forwarded_port", guest:8008, host:8008

    ## Provisioning
    config.vm.provision "shell", path: "setup/basic-setup.sh"
    config.vm.provision "shell", privileged: false, path: "setup/mininet-setup.sh"
    config.vm.provision "shell", privileged: false, path: "setup/ryu-setup.sh"
    # config.vm.provision "shell", privileged: false, path: "setup/onos-setup.sh", env: {"ONOS_VERSION" => "1.12.0"}
    # config.vm.provision "shell", privileged: false, path: "setup/onosdocker-setup.sh"

    # x11 not necessary
    # change to true if x11 is available
    config.ssh.forward_x11 = true

    config.vm.provider "virtualbox" do |vb|
        vb.customize [
            "modifyvm", :id,
            "--paravirtprovider", "minimal",
            "--cpus", "2"
        ]
        vb.gui = true
    end

    config.vm.provider "vmware_desktop" do |v|
        v.gui = true
    end

end
