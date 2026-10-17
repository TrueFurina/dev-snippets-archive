import torch, warnings
print("torch", torch.__version__, "cuda_available", torch.cuda.is_available())
try:
    x = torch.randn(3, 3, device="cuda")
    y = x @ x
    print("CUDA COMPUTE OK", str(x.device), "result_sum", float(y.sum()))
except Exception as e:
    print("CUDA COMPUTE FAIL", repr(e))
