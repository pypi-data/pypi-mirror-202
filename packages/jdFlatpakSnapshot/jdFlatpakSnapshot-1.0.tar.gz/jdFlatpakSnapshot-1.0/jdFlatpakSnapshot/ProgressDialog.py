from .ui_compiled.ProgressDialog import Ui_ProgressDialog
from .Functions import list_files_recursive
from PyQt6.QtWidgets import QDialog
import tarfile
import os


class ProgressDialog(QDialog, Ui_ProgressDialog):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

    def create_tar_archive(self, tar_file: str, source_dir: str, mode: str):
        self.show()

        try:
            os.makedirs(os.path.dirname(tar_file))
        except Exception:
            pass

        tf = tarfile.open(tar_file, mode)
        for i in list_files_recursive(source_dir):
            self.progress_label.setText(i)
            self.repaint()
            self.update()
            tf.add(os.path.join(source_dir, i), arcname=i)
        tf.close()

        self.close()

    def extract_tar_archive(self, tar_file: str, out_dir: str):
        self.show()

        if tar_file.endswith(".tar"):
            mode = "r"
        elif tar_file.endswith(".tar.gz"):
            mode = "r:gz"
        elif tar_file.endswith(".tar.bz2"):
            mode = "r:bz2"
        elif tar_file.endswith(".tar.xz"):
            mode = "r:xz"

        os.makedirs(out_dir)

        tf = tarfile.open(tar_file, mode)
        for i in tf.getnames():
             tf.extract(i, out_dir)
        tf.close()

        self.close()
