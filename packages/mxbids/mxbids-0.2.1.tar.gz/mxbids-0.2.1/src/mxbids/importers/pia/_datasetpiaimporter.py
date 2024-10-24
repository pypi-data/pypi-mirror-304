"""_datasetpiaimporter.py
"""
from mxbids.header import __author__, __credits__, __email__, __maintainer__

__author__ = __author__
__maintainer__ = __maintainer__
__credits__ = __credits__
__email__ = __email__

import json
from pathlib import Path
from typing import Any, List, Optional

import pandas as pd

from mxbids.datasets import Dataset
from mxbids.datasets.importers import DatasetImporter
from mxbids.subjects import Subject
from mxbids.subjects.importers.pia import SubjectPiaImporter

DEFAULT_DESC = {
    "Name": "Default name, should be updated",
    "BIDSVersion": "1.6.0",
    "DatasetType": "raw",
}
DEFAULT_PARTICIPANT_JSON = {
    "UPenn-ID": {"Description": "Patient ID used for the collaboration with UPenn. Usually a number, like 0000"}
}
DEFAULT_PARTICIPANT_COLS = [
    "participant_id",
    "upenn_id",
]


def _update_json(path, json_data):
    if path.is_file():
        with open(path, "r") as f:
            desc_prev = json.load(f)

        desc_prev.update(json_data)

        with open(path, "w") as f:
            json.dump(desc_prev, f)
    else:
        with open(path, "w") as f:
            json.dump(json_data, f)


def _update_ignore(path, entries):
    with open(path, "a") as f:
        f.writelines(entries)


class DatasetPiaImporter(DatasetImporter):
    def _process_subjects(self, subjects: list[str]):
        assert self.dataset is not None

        for subject in subjects:
            if subject not in self.dataset.subjects:
                self.dataset.create_new_subject(Subject, subject)
            self.dataset.subjects[subject].add_importer("Pia", SubjectPiaImporter)

    def construct(
        self,
        dataset: Optional[Dataset] = None,
        src_root: Optional[Path] = None,
        subjects: List[str] = [],
        process: bool = True,
        **kwargs: Any,
    ) -> None:
        if dataset is not None:
            self.dataset = dataset

        if src_root is not None:
            self.src_root = src_root

        if process:
            self._process_subjects(subjects)
        super().construct(process=False, **kwargs)

    def import_subjects(self, path: Path, source_patients: list[str], overwrite: bool = False):
        assert self.dataset is not None

        participants_tsv_path = path / "participants.tsv"
        if participants_tsv_path.is_file():
            participants_tsv_data = pd.read_csv(participants_tsv_path, sep="\t")
        else:
            participants_tsv_data = pd.DataFrame(columns=["participant_id"])

        for subject, source_patient in zip(self.dataset.subjects.values(), source_patients):
            if subject in participants_tsv_data["participant_id"].values and not overwrite:
                continue
            subject.create_importer("Pia", self.src_root).execute_import(path, source_patient)
            subject_frame = pd.DataFrame(data=[subject.name], columns=["participant_id"])
            participants_tsv_data = pd.concat(
                [participants_tsv_data, subject_frame],
                ignore_index=True,
            )

        participants_tsv_data.to_csv(participants_tsv_path, sep="\t")

    def execute_import(
        self,
        path: Optional[Path] = None,
        source_patients: list[str] = [],
        name: Optional[str] = None,
        desc: dict = DEFAULT_DESC,
        ignore_entries: list[str] = ["ct\n"],
        participants_json_data: dict = DEFAULT_PARTICIPANT_JSON,
    ) -> None:
        assert self.dataset is not None
        if name is None:
            name = self.dataset.name
        if path is None:
            assert self.dataset.path is not None
            path = self.dataset.path.parent
        assert path is not None
        assert name is not None

        new_path = path / name
        new_path.mkdir(exist_ok=True)

        desc_path = new_path / "dataset_description.json"
        ignore_path = new_path / ".bidsignore"
        participants_json_path = new_path / "participants.json"

        _update_json(desc_path, desc)
        _update_ignore(ignore_path, ignore_entries)
        _update_json(participants_json_path, participants_json_data)

        self.import_subjects(path=new_path, source_patients=source_patients)
