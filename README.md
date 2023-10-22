# Showcase
## Usage
```bash
# Login to linux distro
proot-distro login debian --shared-tmp
# Load python venv
source .venv/bin/activate
# Run script
cd mobile-stable-diffusion
python text2image_cli.py demo
```
## Outputs
| Config | DPMSolverMultistepScheduler  | EulerDiscreteSchedule |
|--------|-------------------------|-------------------------|
| {<br>&nbsp;&nbsp;"modelName": "meinamix_meinaV9",<br>  "steps": 20,<br>  "prompt": "(masterpiece, best quality, high quality, highresolution:1.4), ambient soft lighting, 4K, 1girl,cute,huge breasts,close-up,long hair,pink hair,black hairband,pink eyes, well defined nose, happy, close-up,((gradient hair))",<br>  "negativePrompt": "easynegative, badhandv4, (worst quality, low quality, normal quality), bad-artist, blurry, ugly, ((bad anatomy)),((bad hands)),((bad proportions)),((duplicate limbs)),((fused limbs)),((interlocking fingers)),((poorly drawn face)),clothes,logo,watermark,muscles:1.3,elf,elf ears,headphones,",<br>  "width": 216,<br>  "height": 320,<br>  "seed": 78583<br>  } | ![Image](./Showcase/dpm20/meinamix_meinaV9_78583_2023_10_15_16_29_49.png) | ![Image](./Showcase/euler20/meinamix_meinaV9_78583_2023_10_15_16_37_13.png) |
|  |  ![Image](./Showcase/dpm32/meinamix_meinaV9_78583_2023_10_15_16_07_14.png) | ![Image](./Showcase/euler32/meinamix_meinaV9_78583_2023_10_15_16_47_33.png) |
|  |  ![Image](./Showcase/dpm64/meinamix_meinaV9_78583_2023_10_15_16_20_03.png) | ![Image](./Showcase/euler64/meinamix_meinaV9_78583_2023_10_15_16_59_46.png) |

See the prompts and other configuration [here](./Showcase).

# Intro
To use stable diffusion you'll need [Termux](https://termux.dev), this app allows you to use a linux distro in your mobile phone.

You'll also need a model to work with. In this case I'll be [MeinaMix](https://civitai.com/models/7240/meinamix) a model hosted in [Civitai](https://civitai.com) and [HuggingFace](https://huggingface.co/models).

I usually generate the model form a .safetensors file or download the files directly from a [HuggingFace repo](https://huggingface.co/Meina/MeinaMix_V10/tree/main).

The model should be placed inside the Models folder and have the following structure:

```
Models/meinamix_meinaV9
├── feature_extractor
│   └── preprocessor_config.json
├── model_index.json
├── safety_checker
│   ├── config.json
│   └── pytorch_model.bin
├── scheduler
│   └── scheduler_config.json
├── text_encoder
│   ├── config.json
│   └── pytorch_model.bin
├── tokenizer
│   ├── merges.txt
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   └── vocab.json
├── unet
│   ├── config.json
│   └── diffusion_pytorch_model.bin
└── vae
    ├── config.json
    └── diffusion_pytorch_model.bin
```

# Set up
Download [Termux](https://termux.dev) and install it on your phone.

## Install a linux distro
```bash
pkg install proot
pkg install proot-debian
pkg install proot-distro
proot-distro install debian
```
Note that the distro will be located at `/data/data/com.termux/files/usr/var/lib/proot-distro/installed-rootfs/debian/root`.

### Login to the linux distro
```bash
proot-distro login debian --shared-tmp
```

#### Install dependencies
```bash
apt update
apt install git git-lfs vim python3 python3-pip python3-venv
```

#### Python venv
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade diffusers transformers accelerate ftfy xformers
pip install pytorch
pip install torch
```

## Clone repo
```bash
git clone https://github.com/zehr0s/mobile-stable-diffusion
cd mobile-stable-diffusion
```

## Download model
Download the [model](https://huggingface.co/Meina/MeinaMix_V10/tree/main) and place it inside the folder `Models`.

# Run the script
```bash
python text2image_cli.py
```
