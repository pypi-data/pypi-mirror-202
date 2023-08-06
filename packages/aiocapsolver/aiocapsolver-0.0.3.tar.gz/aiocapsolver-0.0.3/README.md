# Capsolver.com API for Python
CapSolverPython is an elegant API implementation of Capsolver.com for python

### Features:
* Async/Sync support
* All endpoints/inputs (soon)
* Error handling

### Installation
```pip install aiofiles```
(https://pypi.org/project/aiocapsolver/)
### Usage

```python
from aiocapsolver.capsolver import AsyncCapSolver

solver = AsyncCapSolver(MyCapSolverApiKey)


async def myasyncfunction():
    result = await solver.solve_image_to_text(images / myimage.png)
```

### WIP
Currently only supports:
* async
* Image captcha solving

Watch this space for future additions