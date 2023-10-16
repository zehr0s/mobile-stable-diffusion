# Imports
import torch
import datetime, os
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler, EulerDiscreteScheduler

# Use local model
models_path = "./Models"
models = os.listdir(models_path)
model_name = models[0]
model_id = os.path.join(models_path, model_name)

# Create pipeline obj
pipeline = DiffusionPipeline.from_pretrained(
    model_id,
    custom_pipeline="lpw_stable_diffusion",
    revision='0.15.1',
    custom_revision='0.15.1',
    low_cpu_mem_usage=True,
    torch_dtype=torch.float32,
    cache_dir="./.cache",
)

# Scheduler
# pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)
pipeline.scheduler = EulerDiscreteScheduler.from_config(pipeline.scheduler.config)

# Use cpu/cuda
# pipeline = pipeline.to("cuda")

# Bypass nsfw filter
pipeline.safety_checker = lambda images, clip_input: (images, False)

# Some settings
resolution = [320, 320]

# Prompt engineering
prompt = "(masterpiece, best quality, high quality, highresolution:1.4), ambient soft lighting, 4K, 1girl, cute, huge breasts,close-up,long hair,pink hair,hairband,((gradient hair))"
negative_prompt = "easynegative, badhandv4, (worst quality, low quality, normal quality), bad-artist, blurry, ugly, ((bad anatomy)),((bad hands)),((bad proportions)),((duplicate limbs)),((fused limbs)),((interlocking fingers)),((poorly drawn face)),clothes,logo,watermark,muscles:1.3,elf,elf ears,"

# Generate image
with torch.no_grad():
    img = pipeline(
        prompt=prompt,
        negative_prompt=negative_prompt,
        height=resolution[0],
        width=resolution[1],
        num_inference_steps=32,
        guidance_scale=8,
        max_embeddings_multiples = 8,
    ).images[0]

# Save image
out_path = "./Outputs"
mobile_path = "/sdcard/Download"
if os.path.isdir(mobile_path):
    out_path = mobile_path
else:
    os.makedirs(out_path, exist_ok = True)
out_name = f"{model_name}_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.png"
out_file = os.path.join(out_path, out_name)
img.save(out_file)
