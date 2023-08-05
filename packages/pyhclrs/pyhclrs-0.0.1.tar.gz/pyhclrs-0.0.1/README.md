# pyhclrs
Python wrapper for [martinohmann/hcl-rs](https://github.com/martinohmann/hcl-rs).

## Setup
```sh
pip install pyhclrs
```

## Usage
```py
>>> import pyhclrs
>>> pyhclrs.loads("""variable "docker_ports" {
...   type = list(object({
...     internal = number
...     external = number
...     protocol = string
...   }))
...   default = [
...     {
...       internal = 8300
...       external = 8300
...       protocol = "tcp"
...     }
...   ]
... }""")
{'variable': {'docker_ports': {'type': '${list(object({ internal = number, external = number, protocol = string }))}', 'default': [{'internal': 8300, 'external': 8300, 'protocol': 'tcp'}]}}}
```