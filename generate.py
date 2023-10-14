import torch
import datetime, os
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
# from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler

# Use local model
model_id = "./Models/meinamix_meinaV9"
model_name = model_id.split("/")[-1]

# Create pipeline obj
pipelineAux = DiffusionPipeline.from_pretrained(
    model_id,
    custom_pipeline="lpw_stable_diffusion",
    revision='0.15.1',
    custom_revision='0.15.1',
    torch_dtype=torch.float32 # torch.float16
)
pipelineAux.scheduler = DPMSolverMultistepScheduler.from_config(pipelineAux.scheduler.config)

pipeline = pipelineAux
# pipeline = pipeline.to("cuda")

# Bypass nsfw filter
pipeline.safety_checker = lambda images, clip_input: (images, False)

# Some settings
mobile = False
portrait = True
res = [360, 640] if mobile else [512, 768]
res = sorted(res, reverse=True) if portrait else sorted(res)

# Prompt engineering
prompt = "(masterpiece, best quality, high quality, highres:1.4), ambient soft lighting, 4K, 1girl, cute, huge breasts,, close-up,long hair,pink hair,hairband,((gradient hair))"

negative = "easynegative, badhandv4, (worst quality, low quality, normal quality), bad-artist, blurry, ugly, ((bad anatomy)),((bad hands)),((bad proportions)),((duplicate limbs)),((fused limbs)),((interlocking fingers)),((poorly drawn face)),clothes,logo,watermark,muscles:1.3,elf,elf ears,"

print(f"[+] Prompt: {prompt}")
print(f"[+] Negative: {negative}")
print(f"[+] Res: {res}")

# Generate image
with torch.no_grad():
    img = pipeline(
        prompt=prompt,
        negative_prompt =negative,
        height=res[0],
        width=res[1],
        num_inference_steps=32,
        guidance_scale=8,
        max_embeddings_multiples = 8,
    ).images[0]

# Save image
out_path = "."
out_name = f"{model_name}_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.png"
out_file = os.path.join(out_path, out_name)
img.save(out_file)

### Deprecated
# Use Euler sampling
# scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")

# Enable low memory usage, set image size to 320x320 and steps to 50.
# pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, low_cpu_mem_usage=True, height=320, width=320, num_inference_steps=30)

# Bypass NSFW filter
# pipe.safety_checker = lambda images, clip_input: (images, False)

# Prompts
# prompt = "A victorian woman stands on grass field."

# Start generating the image. Use CPU only
# image = pipe(prompt).images[0]

# Save the image
# image.save("result.png")
