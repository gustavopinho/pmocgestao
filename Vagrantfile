# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = '2'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Specify the base box
  config.vm.box = 'debian/contrib-stretch64'

  # Setup port forwarding
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 5432, host: 5432

  # Forward for gulpjs
  config.vm.network "forwarded_port", guest: 3000, host: 3000
  config.vm.network "forwarded_port", guest: 3001, host: 3001

  # VM name
  config.vm.hostname = "pmoc"

  # Setup synced folder
  config.vm.synced_folder "./" , "/vagrant", :mount_options => ["dmode=777","fmode=777"]

  # Shell provisioning
  config.vm.provision "shell" do |s|
    s.path = "provision/setup.sh"
  end

  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1536"]
  end
end
