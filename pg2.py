/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/transformers/optimization.py:306: FutureWarning: This implementation of AdamW is deprecated and will be removed in a future version. Use the PyTorch implementation torch.optim.AdamW instead, or set `no_deprecation_warning=True` to disable this warning
  warnings.warn(
/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/transformers/optimization.py:306: FutureWarning: This implementation of AdamW is deprecated and will be removed in a future version. Use the PyTorch implementation torch.optim.AdamW instead, or set `no_deprecation_warning=True` to disable this warning
  warnings.warn(
/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/transformers/optimization.py:306: FutureWarning: This implementation of AdamW is deprecated and will be removed in a future version. Use the PyTorch implementation torch.optim.AdamW instead, or set `no_deprecation_warning=True` to disable this warning
  warnings.warn(
/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/transformers/optimization.py:306: FutureWarning: This implementation of AdamW is deprecated and will be removed in a future version. Use the PyTorch implementation torch.optim.AdamW instead, or set `no_deprecation_warning=True` to disable this warning
  warnings.warn(
/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/transformers/optimization.py:306: FutureWarning: This implementation of AdamW is deprecated and will be removed in a future version. Use the PyTorch implementation torch.optim.AdamW instead, or set `no_deprecation_warning=True` to disable this warning
  warnings.warn(
/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/transformers/optimization.py:306: FutureWarning: This implementation of AdamW is deprecated and will be removed in a future version. Use the PyTorch implementation torch.optim.AdamW instead, or set `no_deprecation_warning=True` to disable this warning
  warnings.warn(
***** Running training *****
  Num examples = 132466043
  Num Epochs = 10
  Instantaneous batch size per device = 128
  Total train batch size (w. parallel, distributed & accumulation) = 24576
  Gradient Accumulation steps = 32
  Total optimization steps = 53900
Automatic Weights & Biases logging enabled, to disable set os.environ["WANDB_DISABLED"] = "true"
wandb: Currently logged in as: hoonrae. Use `wandb login --relogin` to force relogin
wandb: Tracking run with wandb version 0.12.21
wandb: Run data is saved locally in /home1/hoonrae/Pretrain_T5/wandb/run-20220710_163723-17r791a9
wandb: Run `wandb offline` to turn off syncing.
wandb: Syncing run outputs/
wandb: ⭐️ View project at https://wandb.ai/hoonrae/huggingface
wandb: 🚀 View run at https://wandb.ai/hoonrae/huggingface/runs/17r791a9
[W reducer.cpp:1289] Warning: find_unused_parameters=True was specified in DDP constructor, but did not find any unused parameters in the forward pass. This flag results in an extra traversal of the autograd graph every iteration,  which can adversely affect performance. If your model indeed never has any unused parameters in the forward pass, consider turning this flag off. Note that this warning may be a false positive if your model has flow control causing later iterations to have unused parameters. (function operator())
[W reducer.cpp:1289] Warning: find_unused_parameters=True was specified in DDP constructor, but did not find any unused parameters in the forward pass. This flag results in an extra traversal of the autograd graph every iteration,  which can adversely affect performance. If your model indeed never has any unused parameters in the forward pass, consider turning this flag off. Note that this warning may be a false positive if your model has flow control causing later iterations to have unused parameters. (function operator())
[W reducer.cpp:1289] Warning: find_unused_parameters=True was specified in DDP constructor, but did not find any unused parameters in the forward pass. This flag results in an extra traversal of the autograd graph every iteration,  which can adversely affect performance. If your model indeed never has any unused parameters in the forward pass, consider turning this flag off. Note that this warning may be a false positive if your model has flow control causing later iterations to have unused parameters. (function operator())
[W reducer.cpp:1289] Warning: find_unused_parameters=True was specified in DDP constructor, but did not find any unused parameters in the forward pass. This flag results in an extra traversal of the autograd graph every iteration,  which can adversely affect performance. If your model indeed never has any unused parameters in the forward pass, consider turning this flag off. Note that this warning may be a false positive if your model has flow control causing later iterations to have unused parameters. (function operator())
[W reducer.cpp:1289] Warning: find_unused_parameters=True was specified in DDP constructor, but did not find any unused parameters in the forward pass. This flag results in an extra traversal of the autograd graph every iteration,  which can adversely affect performance. If your model indeed never has any unused parameters in the forward pass, consider turning this flag off. Note that this warning may be a false positive if your model has flow control causing later iterations to have unused parameters. (function operator())
[W reducer.cpp:1289] Warning: find_unused_parameters=True was specified in DDP constructor, but did not find any unused parameters in the forward pass. This flag results in an extra traversal of the autograd graph every iteration,  which can adversely affect performance. If your model indeed never has any unused parameters in the forward pass, consider turning this flag off. Note that this warning may be a false positive if your model has flow control causing later iterations to have unused parameters. (function operator())
wandb: Network error (ReadTimeout), entering retry loop.
wandb: Network error (ReadTimeout), entering retry loop.
wandb: Network error (ReadTimeout), entering retry loop.
Traceback (most recent call last):
  File "/home1/hoonrae/Pretrain_T5/train.py", line 150, in <module>
    trainer.train()
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/transformers/trainer.py", line 1317, in train
    return inner_training_loop(
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/transformers/trainer.py", line 1528, in _inner_training_loop
    for step, inputs in enumerate(epoch_iterator):
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/torch/utils/data/dataloader.py", line 530, in __next__
    data = self._next_data()
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/torch/utils/data/dataloader.py", line 1224, in _next_data
    return self._process_data(data)
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/torch/utils/data/dataloader.py", line 1250, in _process_data
    data.reraise()
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/torch/_utils.py", line 457, in reraise
    raise exception
IndexError: Caught IndexError in DataLoader worker process 25.
Original Traceback (most recent call last):
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/torch/utils/data/_utils/worker.py", line 287, in _worker_loop
    data = fetcher.fetch(index)
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/torch/utils/data/_utils/fetch.py", line 49, in fetch
    data = [self.dataset[idx] for idx in possibly_batched_index]
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/torch/utils/data/_utils/fetch.py", line 49, in <listcomp>
    data = [self.dataset[idx] for idx in possibly_batched_index]
  File "/home1/hoonrae/Pretrain_T5/train.py", line 35, in __getitem__
    noised_text = splited[1]
IndexError: list index out of range

WARNING:torch.distributed.elastic.multiprocessing.api:Sending process 24317 closing signal SIGTERM
WARNING:torch.distributed.elastic.multiprocessing.api:Sending process 24318 closing signal SIGTERM
WARNING:torch.distributed.elastic.multiprocessing.api:Sending process 24319 closing signal SIGTERM
WARNING:torch.distributed.elastic.multiprocessing.api:Sending process 24320 closing signal SIGTERM
WARNING:torch.distributed.elastic.multiprocessing.api:Sending process 24322 closing signal SIGTERM
ERROR:torch.distributed.elastic.multiprocessing.api:failed (exitcode: 1) local_rank: 4 (pid: 24321) of binary: /home1/hoonrae/anaconda3/envs/T5/bin/python
Traceback (most recent call last):
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/runpy.py", line 197, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/runpy.py", line 87, in _run_code
    exec(code, run_globals)
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/torch/distributed/launch.py", line 193, in <module>
    main()
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/torch/distributed/launch.py", line 189, in main
    launch(args)
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/torch/distributed/launch.py", line 174, in launch
    run(args)
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/torch/distributed/run.py", line 715, in run
    elastic_launch(
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/torch/distributed/launcher/api.py", line 131, in __call__
    return launch_agent(self._config, self._entrypoint, list(args))
  File "/home1/hoonrae/anaconda3/envs/T5/lib/python3.9/site-packages/torch/distributed/launcher/api.py", line 245, in launch_agent
    raise ChildFailedError(
torch.distributed.elastic.multiprocessing.errors.ChildFailedError: 
============================================================
train.py FAILED
------------------------------------------------------------
Failures:
  <NO_OTHER_FAILURES>
------------------------------------------------------------
Root Cause (first observed failure):
[0]:
  time      : 2022-07-11_09:56:03
  host      : n20.cluster
  rank      : 4 (local_rank: 4)
  exitcode  : 1 (pid: 24321)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
============================================================