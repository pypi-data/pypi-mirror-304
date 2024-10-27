# Sphinx download link replacer

This script allows you to replace the download links on the generated [Jupyter book](https://jupyterbook.org/en/stable/intro.html) pages.

## Usage

````markdown
```{custom_download_link} <link_target>
:text: "Custom text"
:replace_default: "True"
```
````

Replace `<link_target>` with the download location. It can either be a remote link (`http`, `https`, or `ftp`), or a local path (relative to the location of the file containing the directive). Local files must be located within or below the source folder of the book (i.e. the folder containing `_config.yml`).

The `replace_default` key is optional. When set to `True`, the default download link will be replaced with the custom one. When set to `False`, the default download link will be kept, and the custom one will be added below it. If the key is not set, the default behavior is to add the link to the list, without changing the default one.

The directive can appear multiple times in a single file.
