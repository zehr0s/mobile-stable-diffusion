# Imports
import sys
import torch
import datetime, random, json, os
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler, EulerDiscreteScheduler

# Args
is_demo = False
if len(sys.argv) == 2:
    if not sys.argv[1] == 'demo':
        print(f'Usage: {sys.argv[0]} <demo>')
        sys.exit(0)
    is_demo = True
    print(f"Demo mode: {is_demo}")
elif len(sys.argv) > 2:
    print(f'Usage: {sys.argv[0]} <demo>')
    sys.exit(0)

# Use local model
models_path = "./Models"
models = os.listdir(models_path)
model_name = models[0]
model_id = os.path.join(models_path, model_name)

#model_id = "./Models/meinamix_meinaV9"
#model_name = model_id.split("/")[-1]

# Create pipeline obj
pipeline = DiffusionPipeline.from_pretrained(
    model_id,
    # use_safetensors=True,
    custom_pipeline="lpw_stable_diffusion",
    revision='0.15.1',
    custom_revision='0.15.1',
    low_cpu_mem_usage=True,
    torch_dtype=torch.float32 # torch.float16
)

# Default settings
scheduler_name = 'd'
portrait_mode = ''
steps = 64
character = ''
schedulers = {
    'e': 'EulerDiscreteScheduler',
    'd': 'DPMSolverMultistepScheduler',
}
seed = int(random.random()*100000)
batch_size = 1

# Scheduler
if not is_demo:
    scheduler_name = input("Scheduler Euler/DPM [e/d]: ")
if scheduler_name == 'e':
    pipeline.scheduler = EulerDiscreteScheduler.from_config(pipeline.scheduler.config)
elif scheduler_name == 'd':
    pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)
else:
    pipeline.scheduler = EulerDiscreteScheduler.from_config(pipeline.scheduler.config)

# Bypass nsfw filter
pipeline.safety_checker = lambda images, clip_input: (images, False)

## User defined settings
mobile = True
mobile_resolutions = [
    [320, 512],
    [216, 320],
]
mobile_resolution = mobile_resolutions[1]
desktop_resolutions = [
    [512, 768],
    [512, 816],
    [512, 912],
    [512, 1024],
]
desktop_resolution = desktop_resolutions[0]
if not is_demo:
    portrait_mode = input("Portrait [y/n]: ")
portrait = portrait_mode.lower() == 'y'
resolution = mobile_resolution if mobile else desktop_resolution
resolution = sorted(resolution, reverse=True) if portrait else sorted(resolution)
if portrait_mode == '':
    resolution = [mobile_resolution[0], mobile_resolution[0]] if mobile else [desktop_resolution[0], desktop_resolution[0]]
if not is_demo:
    try:
        steps = int(input("Steps: "))
    except:
        print(f"Default steps: {steps}")

# Use cuda/cpu
# pipeline = pipeline.to("cuda")
generator = torch.Generator(device="cpu").manual_seed(seed)

## Prompt engineering
if not is_demo:
    character = input("Describe character: ")
if character == '':
    character = '1girl,cute,huge breasts,close-up,long hair,pink hair,black hairband,pink eyes, well defined nose, happy'
prompt = f"(masterpiece, best quality, high quality, highresolution:1.4), ambient soft lighting, 4K, {character}, close-up,((gradient hair))"
negative = "easynegative, badhandv4, (worst quality, low quality, normal quality), bad-artist, blurry, ugly, ((bad anatomy)),((bad hands)),((bad proportions)),((duplicate limbs)),((fused limbs)),((interlocking fingers)),((poorly drawn face)),clothes,logo,watermark,muscles:1.3,elf,elf ears,headphones,"

## Batch size
if not is_demo:
    try:
         batch_size = int(input("Batch size: "))
    except:
        print(f"Default batch size: {batch_size}")

# Final settings
print(f"[+] Model name: {model_name}")
print(f"[+] Scheduler: {schedulers[scheduler_name]}")
print(f"[+] Prompt: {prompt}")
print(f"[+] Negative: {negative}")
print(f"[+] Resolution: {resolution}")
print(f"[+] Width: {resolution[1]}")
print(f"[+] Height: {resolution[0]}")
print(f"[+] Steps: {steps}")
print(f"[+] Seed: {seed}")
print(f"[+] Batch size: {batch_size}")

save_settings = False
for i in range(batch_size):
    # Generate image
    with torch.no_grad():
        img = pipeline(
            prompt=prompt,
            negative_prompt=negative,
            height=resolution[0],
            width=resolution[1],
            num_inference_steps=steps,
            guidance_scale=8,
            max_embeddings_multiples=8,
            generator=generator,
        ).images[0]

    # Save image
    out_path = "./Outputs"
    mobile_path = "/sdcard/Download"
    if os.path.isdir(mobile_path):
        out_path = mobile_path
    else:
        os.makedirs(out_path, exist_ok = True)
    out_name = f"{model_name}_{seed}_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.png"
    out_file = os.path.join(out_path, out_name)
    img.save(out_file)

    # Save settings
    if save_settings:
        settings = {
            'modelName': model_name,
            'scheduler': schedulers[scheduler_name],
            'steps': steps,
            'prompt': prompt,
            'negativePrompt':negative,
            'width': resolution[1],
            'height': resolution[0],
            'seed': seed,
        }
        with open(out_file.replace('.png','.json'), 'w') as f:
            f.write(json.dumps(settings, indent=4))

