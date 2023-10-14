# Imports
import torch
import datetime, os
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler, EulerDiscreteScheduler
# from diffusers import StableDiffusionPipeline

# Use local model
model_id = "./Models/meinamix_meinaV9"
model_name = model_id.split("/")[-1]

# Create pipeline obj
pipeline = DiffusionPipeline.from_pretrained(
    model_id,
    custom_pipeline="lpw_stable_diffusion",
    revision='0.15.1',
    custom_revision='0.15.1',
    low_cpu_mem_usage=True,
    torch_dtype=torch.float32 # torch.float16
)
# pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)
pipeline.scheduler = EulerDiscreteScheduler.from_config(pipeline.scheduler.config)

# pipeline = pipeline.to("cuda")

# Bypass nsfw filter
pipeline.safety_checker = lambda images, clip_input: (images, False)

# Some settings
mobile = True
option = input("Portrait: [y/n]: ")
portrait = option.lower() == 'y'
res = [320, 512] if mobile else [512, 768]
res = sorted(res, reverse=True) if portrait else sorted(res)
if option == '':
    res = [320, 320]

# Prompt engineering
character = input("Describe character: ")
prompt = f"(masterpiece, best quality, high quality, highres:1.4), ambient soft lighting, 4K, 1girl,{character}, cute, huge breasts,close-up,((gradient hair))"
negative = "easynegative, badhandv4, (worst quality, low quality, normal quality), bad-artist, blurry, ugly, ((bad anatomy)),((bad hands)),((bad proportions)),((duplicate limbs)),((fused limbs)),((interlocking fingers)),((poorly drawn face)),clothes,logo,watermark,muscles:1.3,elf,elf ears,"

# print(f"[+] Prompt: {prompt}")
# print(f"[+] Negative: {negative}")
# print(f"[+] Res: {res}")

# Generate image
with torch.no_grad():
    img = pipeline(
        prompt=prompt,
        negative_prompt =negative,
        height=res[0],
        width=res[1],
        num_inference_steps=26,
        guidance_scale=8,
        max_embeddings_multiples = 8,
    ).images[0]

# Save image
out_path = "./Outputs"
mobile_path = "/sdcard/Download"
if os.path.isdir(mobile_path):
    out_path = mobile_path
out_name = f"{model_name}_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.png"
out_file = os.path.join(out_path, out_name)
img.save(out_file)
