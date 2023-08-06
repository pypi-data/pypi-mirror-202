# PEAnalyzer

A Python module to analyze Portable Executable (PE) files on Windows systems. It parses and extracts various details about the file header, optional header, sections, imports, and exports. The module provides an easy-to-use class, `PEAnalyzer`, which returns analysis data in JSON format and supports pretty-printing of the information when used with the `print()` function.

## Installation

To use PEAnalyzer, first, install the `pefile` library by running:

```
pip install pefile
```

Then, download or clone this repository to your project directory.

## Usage

To use the `PEAnalyzer` class, import it from the module and create an instance with the path to the PE file you want to analyze:

```python
from pe_analyzer import PEAnalyzer

file_path = "path/to/your/file.exe"
analyzer = PEAnalyzer(file_path)
```

To print the analysis data in a human-readable format, use the `print()` function:

```python
print(analyzer)
```

To get the analysis data as a JSON object, call the `analyze()` method:

```python
analysis_data = analyzer.analyze()
print(analysis_data)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.