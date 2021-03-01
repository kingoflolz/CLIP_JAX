import numpy as np
from PIL import Image

import clip_jax
import clip

image_fn, text_fn, jax_params, jax_preprocess = clip_jax.load('ViT-B/32', "cpu")

jax_image = np.expand_dims(jax_preprocess(Image.open("CLIP.png")), 0)
jax_text = clip_jax.tokenize(["a diagram", "a dog", "a cat"])

jax_image_embed = image_fn(jax_params, jax_image)
jax_text_embed = text_fn(jax_params, jax_text)

pytorch_clip, pyt_preprocess = clip.load('ViT-B/32', "cpu")

pyt_image = pyt_preprocess(Image.open("CLIP.png")).unsqueeze(0).to("cpu")
pyt_text = clip.tokenize(["a diagram", "a dog", "a cat"])

pyt_image_embed = pytorch_clip.encode_image(pyt_image)
pyt_text_embed = pytorch_clip.encode_text(pyt_text)

assert np.allclose(np.array(jax_image_embed), pyt_image_embed.cpu().detach().numpy(), atol=0.01, rtol=0.01)
assert np.allclose(np.array(jax_text_embed), pyt_text_embed.cpu().detach().numpy(), atol=0.01, rtol=0.01)

print("done!")