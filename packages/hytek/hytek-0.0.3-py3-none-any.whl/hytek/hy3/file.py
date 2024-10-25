import zipfile
from logging import warning

from .records import Hy3Record, RECORD_TYPES


__all__ = ("Hy3File",)


class Hy3File:
    def __init__(self, fp: str | None = None):
        self.records: list[Hy3Record] = []
        self.filepath: str | None = fp
        self.file = None

    def read_zip(self, fp: str, *, pwd: bytes | None = None) -> None:
        file = zipfile.ZipFile(fp)
        if self.filepath is None:
            for f in file.infolist():
                if f.filename.endswith(".hy3"):
                    if self.filepath is not None:
                        self.filepath = None
                        raise ValueError("Must specify .hy3 file name.")
                    self.filepath = f
            warning(f"Defaulting to first .hy3 file in zip: {fp}")
        if self.filepath is None:
            raise ValueError("No .hy3 file found in zip.")
        self.file = file.open(self.filepath, pwd=pwd)
        self.read()

    def read(self) -> None:
        if self.file is None:
            self.file = open(self.filepath, "rb")
        parents = []
        last_record = None
        records = []
        data = self.file.read()
        for i, line in enumerate(data.splitlines()):
            record_type = line[:2].decode(errors="ignore")
            try:
                record = RECORD_TYPES.get(record_type, Hy3Record).parse_record(line)
            except Exception as e:
                raise Exception(f"Parsing failed for line {i + 1} type {record_type}: {e}") from e
            if type(record) is Hy3Record:
                warning(f"Unknown record type {record_type}")
                records.append(record)
                continue

            if last_record:
                # Hy3RecordGroup
                if last_record.record_type[0] == record.record_type[0] and last_record.record_type[1] < record.record_type[1]:
                    last_record = last_record.add_to_group(record)
                    if parents:
                        parent = parents[-2]
                        parent.children[-1] = last_record
                        parents[-1] = last_record
                    else:
                        parents.append(last_record)
                        records.append(last_record)
                    continue
            last_record = record

            while parents:
                parent = parents[-1]
                if parent.record_type >= record.record_type:
                    parents.pop()
                else:
                    break
            if parents:
                parent = parents[-1]
                parent.append_child(record)
                parents.append(record)
            else:
                records.append(record)
                parents.append(record)
        self.records = records
        self.file.close()
        self.file = None

    def print_tree(self):
        for record in self.records:
            record.print_tree()

    def to_json(self) -> dict:
        return {"records": [record.to_json() for record in self.records]}