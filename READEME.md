# Markdown to Html Template

This is a small script meant to be used in the command line to take MD files and turn them into HTML files then mapping them to a template based on Jinja. It's main use is for my website. 

## Usage

1. Install required packages from `requirements.txt`
2. Run given these paramaters in CMD

```
usage: MD to Templated HTML [-h] [-v]
                            template_input output_location mark_down_input

Takes in markdown and outputs html in a template

positional arguments:
  template_input   The location of the html file used for input
  output_location  The location of the html file used for output
  mark_down_input  The location of the markdown file used for input

options:
  -h, --help       show this help message and exit
  -v, --verbose    The location of the markdown file used for input
```

### Future plans
If I revisit this it should be shiped as a CMD tool with pip and I will build a custom templating engine.

