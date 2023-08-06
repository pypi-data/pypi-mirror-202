# Inauconf


Inauconf is the script to hidden real Text 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install inauconf
```

## Usage

```python
from inauconf.shuffle import EncryptAll

# crypt function
EncryptAll.crypt('inauconf')
# output: ˫105ɒ110/97Ƞ117W99Ǻ111Ʀ110˯102 .... sample

# uncrypt function
EncryptAll.uncrypt('Ŷ105ǝ110a97ʙ11799à111̶110ƻ102')
# output: inauconf

# crypt & bloc file
EncryptAll.crypt_file('inauconf.txt')
#output: inauconf.inc 
```

## Contributing

Pull requests are welcome. For major changes, please open an [issue](https://github.com/ndjieudja/inauconf/issues) first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)