import torch
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--weight")
parser.add_argument("--output")

args = parser.parse_args()

model_input = torch.load(args.input)
model_weight = torch.load(args.weight)

emb_input = model_input["model"]["encoder.embed_tokens.weight"]
prj_input = model_input["model"]["decoder.output_projection.weight"]
img_emb = prj_input[emb_input.shape[0]:,:]
emb_weight = model_weight["model"]["encoder.embed_tokens.weight"]
model_input["model"]["decoder.output_projection.weight"] = torch.cat((emb_weight, img_emb), 0)

for k in model_weight["model"].keys():
    model_input["model"][k] = model_weight["model"][k]

torch.save(model_input, args.output)
