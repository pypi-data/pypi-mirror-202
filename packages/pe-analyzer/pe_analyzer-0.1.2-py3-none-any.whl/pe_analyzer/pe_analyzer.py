import pefile
import json
import sys
import os


class PEAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path.replace('\\', '/')
        if not os.path.isfile(self.file_path):
            raise ValueError("Couldn't find the target file")
        else:
            self.pe = pefile.PE(file_path)

    def analyze(self):
        analysis = {
            "file_header": self._file_header(),
            "optional_header": self._optional_header(),
            "sections": self._sections(),
            "imports": self._imports(),
            "exports": self._exports(),
        }
        return json.dumps(analysis, indent=2)

    def _file_header(self):
        return {
            "Machine": self.pe.FILE_HEADER.Machine,
            "Number_of_Sections": self.pe.FILE_HEADER.NumberOfSections,
            "Time_Date_Stamp": self.pe.FILE_HEADER.dump_dict()["TimeDateStamp"]["Value"].split("[")[1][:-1],
            "Characteristics": hex(self.pe.FILE_HEADER.Characteristics),
        }

    def _optional_header(self):
        return {
            "Address_of_Entry_Point": hex(self.pe.OPTIONAL_HEADER.AddressOfEntryPoint),
            "Image_Base": hex(self.pe.OPTIONAL_HEADER.ImageBase),
            "Section_Alignment": self.pe.OPTIONAL_HEADER.SectionAlignment,
            "File_Alignment": self.pe.OPTIONAL_HEADER.FileAlignment,
            "Subsystem": self.pe.OPTIONAL_HEADER.Subsystem,
        }

    def _sections(self):
        sections = []
        for section in self.pe.sections:
            sections.append({
                "Name": section.Name.decode().rstrip("\x00"),
                "Virtual_Address": hex(section.VirtualAddress),
                "Virtual_Size": section.Misc_VirtualSize,
                "Raw_Data_Size": section.SizeOfRawData,
                "Characteristics": hex(section.Characteristics),
            })
        return sections

    def _imports(self):
        imports = []
        if hasattr(self.pe, "DIRECTORY_ENTRY_IMPORT"):
            for entry in self.pe.DIRECTORY_ENTRY_IMPORT:
                imports.append({
                    "DLL": entry.dll.decode(),
                    "Functions": [
                        {"Address": f"0x{imp.address:x}", "Name": imp.name.decode()}
                        for imp in entry.imports
                    ],
                })
        return imports

    def _exports(self):
        exports = []
        if hasattr(self.pe, "DIRECTORY_ENTRY_EXPORT"):
            exports.append({
                "DLL_Name": self.pe.DIRECTORY_ENTRY_EXPORT.dll.decode(),
                "Functions": [
                    {"Address": f"0x{exp.address:x}", "Name": exp.name.decode()}
                    for exp in self.pe.DIRECTORY_ENTRY_EXPORT.symbols
                ],
            })
        return exports

    def __str__(self):
        analysis = json.loads(self.analyze())
        result = []

        result.append("=== FILE HEADER ===")
        if not bool(analysis["file_header"].items()):
            result.append("[NO DATA]")
        for k, v in analysis["file_header"].items():
            result.append(f"{k}: {v}")

        result.append("\n=== OPTIONAL HEADER ===")
        if not bool(analysis["optional_header"].items()):
            result.append("[NO DATA]")
        for k, v in analysis["optional_header"].items():
            result.append(f"{k}: {v}")

        result.append("\n=== SECTIONS ===")
        if not bool(analysis["sections"]):
            result.append("[NONE FOUND]")
        for section in analysis["sections"]:
            result.append("\n")
            for k, v in section.items():
                result.append(f"{k}: {v}")

        result.append("\n=== IMPORTS ===")
        if not bool(analysis["imports"]):
            result.append("[NONE FOUND]")
        for imp in analysis["imports"]:
            result.append(f"\nDLL: {imp['DLL']}")
            for func in imp["Functions"]:
                result.append(f"{func['Address']} {func['Name']}")

        result.append("\n=== EXPORTS ===")
        if not bool(analysis["exports"]):
            result.append("[NONE FOUND]")
        for exp in analysis["exports"]:
            result.append(f"DLL Name: {exp['DLL_Name']}")
            for func in exp["Functions"]:
                result.append(f"{func['Address']} {func['Name']}")

        return "\n".join(result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pe_analyzer.py <file>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"Invalid file path: {file_path}")
        print("Usage: python3 pe_analyzer.py <file>")
        sys.exit(1)

    analyzer = PEAnalyzer(file_path)
    print(analyzer)  # Print the analysis in a human-readable format

    # To get the analysis data as a JSON object
    analysis_data = analyzer.analyze()
    print(analysis_data)

