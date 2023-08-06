# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torch_simple_timing']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.11']

setup_kwargs = {
    'name': 'torch-simple-timing',
    'version': '0.1.0',
    'description': 'A simple package to time CPU/GPU/Multi-GPU ops',
    'long_description': '# Torch Simple Timing\n\nA simple yet versatile package to time CPU/GPU/Multi-GPU ops.\n\n1. "*I want to time operations once*"\n   1. That\'s what a `Clock` is for\n2. "*I want to time the same operations multiple times*"\n   1. That\'s what a `Timer` is for\n\nIn simple terms:\n\n* A `Clock` is an object (and context-manager) that will compute the ellapsed time between its `start()` (or `__enter__`) and `stop()` (or `__exit__`)\n* A `Timer` will internally manage clocks so that you can focus on readability and not data structures\n\n## Installation\n\n```\npip install torch_simple_timing\n```\n\n## How to use\n\n### A `Clock`\n\n```python\nfrom torch_simple_parsing import Clock\nimport torch\n\nt = torch.rand(2000, 2000)\ngpu = torch.cuda.is_available()\n\nwith Clock(gpu=gpu) as context_clock:\n    torch.inverse(t @ t.T)\n\nclock = Clock(gpu=gpu).start()\ntorch.inverse(t @ t.T)\nclock.stop()\n\nprint(context_clock.duration) # 0.29688501358032227\nprint(clock.duration)         # 0.292896032333374\n```\n\nMore examples, including bout how to easily share data structures using a `store` can be found in the [documentation]().\n\n### A `Timer`\n\n```python\nfrom torch_simple_timing import Timer\nimport torch\n\ndevice = torch.device("cuda" if torch.cuda.is_available() else "cpu")\n\nX = torch.rand(5000, 5000, device=device)\nY = torch.rand(5000, 100, device=device)\nmodel = torch.nn.Linear(5000, 100).to(device)\noptimizer = torch.optim.Adam(model.parameters())\n\ngpu = device.type == "cuda"\ntimer = Timer(gpu=gpu)\n\nfor epoch in range(10):\n    timer.mark("epoch").start()\n    for b in range(50):\n        x = X[b*100: (b+1)*100]\n        y = Y[b*100: (b+1)*100]\n        optimizer.zero_grad()\n        with timer.mark("forward", ignore=epoch>0):\n            p = model(x)\n        loss = torch.nn.functional.cross_entropy(p, y)\n        with timer.mark("backward", ignore=epoch>0):\n            loss.backward()\n        optimizer.step()\n    timer.mark("epoch").stop()\n\nstats = timer.stats()\n# use stats for display and/or logging\n# wandb.summary.update(stats)\nprint(timer.display(stats=stats, precision=5))\n```\n\n```\nepoch    : 0.25064 ± 0.02728 (n=10)\nforward  : 0.00226 ± 0.00526 (n=50)\nbackward : 0.00209 ± 0.00387 (n=50)\n```\n',
    'author': 'vict0rsch',
    'author_email': 'vsch@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
