# Showcase
```
# Login to linux distro
proot-distro login debian --shared-tmp
# Load python venv
source .venv/bin/activate
# Run script
python generate.py
```

# Set up
You'll need to install Termux on your mobile phone.

## Install a linux distro
```
pkg install proot
pkg install proot-debian
pkg install proot-distro
proot-distro install debian
```

### Login to the linux distro
```
proot-distro login debian --shared-tmp
```

#### Install dependencies
```
apt update
apt install git git-lfs vim python3 python3-pip python3-venv
```

#### Python venv
```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade diffusers transformers accelerate ftfy xformers
pip install pytorch
pip install torch
```

Now you can follow the showcase steps.
