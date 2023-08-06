from .Functions import human_readable_size, format_datetime, generate_snapshot_filename, snapshot_name_exists, extract_file_from_zip, is_flatpak_installed
from .Types import ExportedFileManifest, SnapshotDictEntry
from PyQt6.QtWidgets import QWidget, QMessageBox, QInputDialog
from .Constants import COMPRESSION_METHODS
from PyQt6.QtCore import QCoreApplication
from typing import TYPE_CHECKING
import traceback
import datetime
import zipfile
import json
import sys
import os


if TYPE_CHECKING:
    from .Environment import Environment


def _import_single_snapshot(env: "Environment", app_id: str, parent: QWidget, zf: zipfile.ZipFile):
    with zf.open("metadata.json", "r") as f:
        snapshot_info: SnapshotDictEntry = json.loads(f.read())

    for method in reversed(COMPRESSION_METHODS):
        if "data.tar" + method.suffix in zf.namelist():
            file_name = "data.tar" + method.suffix
            compression = method.name

    text = QCoreApplication.translate("ImportExport", "This includes the following Snapshot:") + "<br>"
    text += QCoreApplication.translate("ImportExport", "App: {{app}}").replace("{{app}}", app_id) + "<br>"
    text += QCoreApplication.translate("ImportExport", "Name: {{name}}").replace("{{name}}", snapshot_info["name"]) + "<br>"
    text += QCoreApplication.translate("ImportExport", "Compression: {{compression}}").replace("{{compression}}", compression) + "<br>"
    text += QCoreApplication.translate("ImportExport", "Size on disk: {{size}}").replace("{{size}}", human_readable_size(zf.getinfo(file_name).file_size)) + "<br>"
    text += QCoreApplication.translate("ImportExport", "Created on: {{datetime}}").replace("{{datetime}}", format_datetime(datetime.datetime.fromtimestamp(snapshot_info["timestamp"]), env.settings.get("datetimeFormat"))) + "<br><br>"
    text += QCoreApplication.translate("ImportExport", "Do you want to import it?")

    if QMessageBox.question(parent, QCoreApplication.translate("ImportExport", "Import"), text, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
        return

    if not is_flatpak_installed(app_id):
        if QMessageBox.question(parent, QCoreApplication.translate("ImportExport", "App not installed"), QCoreApplication.translate("ImportExport", "It looks like {{app}} is not installed. Are you really want to import the data?").replace("{{app}}", app_id), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
            return

    if snapshot_name_exists(env, app_id, snapshot_info["name"]):
        while True:
            new_name = QInputDialog.getText(parent, QCoreApplication.translate("ImportExport", "New name"), QCoreApplication.translate("ImportExport", "There is already a Snapshot with this Name for this App. Please enter a new one."))[0].strip()

            if new_name == "":
                return

            if snapshot_name_exists(env, app_id, new_name):
                QMessageBox.information(parent,  QCoreApplication.translate("ImportExport", "Name exists"),  QCoreApplication.translate("ImportExport", "This Name also exists. Please enter a new one."))
            else:
                snapshot_info["name"] = new_name
                break

    snapshot_path = generate_snapshot_filename(os.path.join(env.data_dir, "snapshots", app_id))

    extract_file_from_zip(zf, file_name, snapshot_path)

    if app_id not in env.snapshot_dict:
        env.snapshot_dict[app_id] = []

    snapshot_info["filename"] = os.path.basename(snapshot_path)
    env.snapshot_dict[app_id].append(snapshot_info)
    env.save_snapshot_dict()


def import_file(env: "Environment", path: str, parent: QWidget) -> None:
    try:
        zf = zipfile.ZipFile(path, "r")

        with zf.open("manifest.json", "r") as f:
            manifest: ExportedFileManifest = json.loads(f.read())

        if manifest["version"] != 1 or manifest["type"] != "single_snapshot":
            QMessageBox.critical(parent, QCoreApplication("ImportExport", "Unsuported version", "This Export was created by a newer version of jdFlatpakSnapshot. You need to update to use it."))
            return

        _import_single_snapshot(env, manifest["app_id"], parent, zf)
    except Exception:
        print(traceback.format_exc(),end="",file=sys.stderr)
        QMessageBox.critical(parent,QCoreApplication.translate("ImportExport", "Error"), QCoreApplication.translate("ImportExport", "An error occurred during import. Maybe the File is not valid."))
    finally:
        try:
            zf.close()
        except Exception:
            pass


def export_single_snapshot(env: "Environment", path: str, app_id: str, snapshot_info: SnapshotDictEntry,  parent: QWidget) -> None:
    try:
        with zipfile.ZipFile(path, "w") as zf:
            zf.write(os.path.join(env.data_dir, "snapshots", app_id, snapshot_info["filename"]), "data." + snapshot_info["filename"].split(".", 1)[1])
            zf.writestr("metadata.json", json.dumps(snapshot_info, ensure_ascii=False, indent=4))
            zf.writestr("manifest.json", json.dumps({
                "version": 1,
                "app_version": env.version,
                "type": "single_snapshot",
                "app_id": app_id
            }, ensure_ascii=False, indent=4))
    except Exception:
        print(traceback.format_exc(),end="",file=sys.stderr)
        QMessageBox.critical(parent, QCoreApplication.translate("ImportExport", "Export failed"), QCoreApplication.translate("ImportExport", "Cound not export {{name}}"). replace("{{name}}", snapshot_info["name"]))