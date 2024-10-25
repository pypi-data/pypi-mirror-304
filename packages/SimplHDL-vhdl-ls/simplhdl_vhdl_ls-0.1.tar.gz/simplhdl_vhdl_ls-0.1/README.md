VHDL\_LS plugin for SimplHDL
---------------------------

SimplHDL-vhdl-ls is a backend plugin for the SimplHDL framework.
From the SimplHDL project model, it generates the necessary config file (.vhdl_ls.toml) that allows
the VHDL_LS language server to properly understand your VHDL code, especially references across files.


## Installation
### Latest release
To install the latest release of the plugin, use pip:
```
$ pip install SimplHDL-vhdl_ls
```

### Development version
To install the development version of the plugin, simply clone the repository to a location of your choice, and install the plugin with pip:
```
$ pip install -e <path-to-your-local-clone>
```


## Usage
The plugin makes a new flow, `vhdl_ls`, available in SimplHDL. This flow simply outputs the generated VHDL_LS configuration
to `stdout`. To run it, simply type:
```
$ simpl vhdl_ls
```

You can of course redirect the output to a file in a location where VHDL_LS expects to find it.
