# cd to the root of this repo
# then run:
#             sh INSTALL.md

sudo pip3 install -r requirements.txt
sudo pip3 install -e .

# test the system

if read -p "Enter, to run tests; cntrl-c to about"; then
  python3 -m bnbad2 -T
fi
