sudo apt-get install -y nodejs git build-essential python2.7

# Install Rust and Cargo
sudo apt-get install -y curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

./do

./cjdroute --genconf > cjdroute.conf

# Now get informabion about the hyperboria network
rm -rf peers
git clone https://github.com/hyperboria/peers.git
cd peers

echo "Testing all available CJDNS peers, this will take approximately 3 minutes..."
python3 testAvailable.py
