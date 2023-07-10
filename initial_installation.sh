#!/usr/bin/env bash

# update network configuration
# sudo cat << EOF >> /etc/wpa_supplicant/wpa_supplicant.conf

# network={
#     ssid="Beta Centauri"
#     psk="HEtV24c7j6vz"
#     key_mgmt=WPA-PSK
# }

# EOF

# sudo reboot

# install pyenv
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
cd ~/.pyenv && src/configure && make -C src

sudo cat << EOF >> /.bashrc

# pyenv configuration
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

EOF

source ~/.bashrc

# install python 3.10.12 wiht pyenv
pyenv install 3.10.12

# install Rust toolchain properly
curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
source "$HOME/.cargo/env"
rustc --version
# rustup update

# install poetry
pip3 install poetry
poetry --version

# clone project and install python dependencies
git clone https://github.com/Kristina-Pianykh/esp32_event_processing.git
cd esp32_event_processing
pyenv local 3.10.12
rm -rf .venv/
poetry env use 3.10.12
poetry install --no-root

# additional dependencies
sudo apt-get install sense-hat -y
sudo reboot
