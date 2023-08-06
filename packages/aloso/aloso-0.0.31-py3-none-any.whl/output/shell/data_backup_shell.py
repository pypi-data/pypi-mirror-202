import logging
import os
import shutil
import time
import zipfile
from datetime import datetime

import schedule
from fabric import Connection, Config

import config
from domain.data_backup import Backup


class BackupShell(Backup):

    @staticmethod
    def connection() -> Connection:
        configuration = Config(overrides={'user': config.backup_username,
                                          'port': config.backup_port})
        try:
            conn = Connection(host=config.backup_host, config=configuration)
            return conn
        except Exception as e:
            logging.error(f"Erreur de connexion au serveur : {e}")

    @staticmethod
    def backup() -> None:
        conn: Connection = BackupShell.connection()
        date: str = datetime.now().strftime('%Y%m%d_%H%M%S')

        source_dir: str = f"{config.root_dir}"
        config_file: str = f"{config.root_dir}/conf_test.py"
        destination_dir: str = f"{config.backup_target_dir}"

        try:
            shutil.make_archive(base_name=date, format='zip', root_dir=source_dir, base_dir="data")

            with zipfile.ZipFile(f"{date}.zip", 'a') as zip_file:
                zip_file.write(config_file, os.path.basename(config_file))

            conn.put(f"{date}.zip", f"{destination_dir}/{date}.zip")

            os.remove(f"{date}.zip")

            logging.info(f"Backup effectué avec succès dans {destination_dir}")
        except Exception as e:
            logging.error(f"Erreur de backup : {e}")

    @staticmethod
    def schedule_backup() -> None:
        schedule.every().day.at(config.backup_hour).do(BackupShell.backup)
        while True:
            schedule.run_pending()
            time.sleep(1)
