import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cleanup import (
    get_backup_age, 
    handle_empty_or_single_backup, 
    classify_backups,
    delete_old_backups,
    check_old_backups
)


def test_get_backup_age(tmp_path):
    backup = tmp_path / "backup_teste.zip"
    backup.touch()

    age = get_backup_age(backup)

    assert isinstance(age, timedelta)


def test_get_backup_age_future_date(tmp_path):
    backup = tmp_path / "backup_futuro.zip"
    backup.touch()

    future_time = datetime.now().timestamp() + 86400
    os.utime(backup, (future_time, future_time))

    age = get_backup_age(backup)

    assert age is None


def test_handle_empty_backups():
    result = handle_empty_or_single_backup([], 30)

    assert result is True


def test_handle_single_recent_backup(tmp_path):
    backup = tmp_path / "backup_recente.zip"
    backup.touch()

    result = handle_empty_or_single_backup([backup], 30)

    assert result is True
    assert backup.exists()


def test_handle_single_old_backup(tmp_path):
    backup = tmp_path / "backup_antigo.zip"
    backup.touch()

    old_time = datetime.now().timestamp() - (40 * 86400)
    os.utime(backup, (old_time, old_time))

    result = handle_empty_or_single_backup([backup], 30)

    assert result is True
    assert backup.exists()


def test_classify_two_old_backups(tmp_path):
    older_backup = tmp_path / "backup_40_dias.zip"
    newer_backup = tmp_path / "backup_35_dias.zip"

    older_backup.touch()
    newer_backup.touch()

    old_time = datetime.now().timestamp() - (40 * 86400)
    newer_time = datetime.now().timestamp() - (35 * 86400)

    os.utime(older_backup, (old_time, old_time))
    os.utime(newer_backup, (newer_time, newer_time))

    old_backups = classify_backups([older_backup, newer_backup], 30)

    assert older_backup in old_backups
    assert newer_backup not in old_backups


def test_classify_two_recent_backups(tmp_path):
    backup_5_days = tmp_path / "backup_5_dias.zip"
    backup_10_days = tmp_path / "backup_10_dias.zip"

    backup_5_days.touch()
    backup_10_days.touch()

    time_5_days = datetime.now().timestamp() - (5 * 86400)
    time_10_days = datetime.now().timestamp() - (10 * 86400)

    os.utime(backup_5_days, (time_5_days, time_5_days))
    os.utime(backup_10_days, (time_10_days, time_10_days))

    old_backups = classify_backups([backup_5_days, backup_10_days], 30)

    assert old_backups == []


def test_classify_old_and_recent_backups(tmp_path):
    old_backup = tmp_path / "backup_antigo.zip"
    recent_backup = tmp_path / "backup_recente.zip"

    old_backup.touch()
    recent_backup.touch()

    old_time = datetime.now().timestamp() - (40 * 86400)
    recent_time = datetime.now().timestamp() - (5 * 86400)

    os.utime(old_backup, (old_time, old_time))
    os.utime(recent_backup, (recent_time, recent_time))

    old_backups = classify_backups([old_backup, recent_backup], 30)

    assert old_backup in old_backups
    assert recent_backup not in old_backups


def test_classify_future_and_old_backups(tmp_path):
    future_backup = tmp_path / "backup_futuro.zip"
    old_backup = tmp_path / "backup_antigo.zip"

    future_backup.touch()
    old_backup.touch()

    future_time = datetime.now().timestamp() + 86400
    old_time = datetime.now().timestamp() - (40 * 86400)

    os.utime(future_backup, (future_time, future_time))
    os.utime(old_backup, (old_time, old_time))

    old_backups = classify_backups([future_backup, old_backup], 30)

    assert old_backup in old_backups
    assert future_backup not in old_backups


def test_delete_old_backups(tmp_path):
    backup = tmp_path / "backup_antigo.zip"
    backup.touch()

    delete_old_backups([backup])

    assert not backup.exists()


def test_delete_missing_backup(tmp_path):
    backup = tmp_path / "backup_inexistente.zip"

    delete_old_backups([backup])

    assert not backup.exists()


def test_delete_empty_list():
    delete_old_backups([])


def test_cleanup_all_old_backups(tmp_path):
    days_list = [90, 80, 70, 60, 50, 40, 35, 32]

    backups = []

    for days in days_list:
        backup = tmp_path / f"backup_{days}_dias.zip"
        backup.touch()

        old_time = datetime.now().timestamp() - (days * 86400)
        os.utime(backup, (old_time, old_time))

        backups.append(backup)

    old_backups = classify_backups(backups, 30)
    delete_old_backups(old_backups)

    for backup, days in zip(backups, days_list):
        if days == 32:
            assert backup.exists()
        else:
            assert not backup.exists()


def test_check_old_backups_empty(monkeypatch):
    monkeypatch.setattr("cleanup.get_backups", lambda: [])

    monkeypatch.setattr(
        "cleanup.load_config",
        lambda: {"retention_days": 30, "cleanup_on_startup": False}
)

    result = check_old_backups()

    assert result is None


def test_check_old_backups_single_backup(monkeypatch, tmp_path):

    monkeypatch.setattr(
        "cleanup.load_config",
        lambda: {"retention_days": 30, "cleanup_on_startup": False}
    )

    backup = tmp_path / "backup_antigo.zip"
    backup.touch()

    old_time = datetime.now().timestamp() - (40 * 86400)
    os.utime(backup, (old_time, old_time))

    monkeypatch.setattr("cleanup.get_backups", lambda: [backup])
    check_old_backups()

    assert backup.exists()


def test_check_old_backups_mixed(monkeypatch, tmp_path):

    monkeypatch.setattr(
        "cleanup.load_config",
        lambda: {"retention_days": 30, "cleanup_on_startup": False}
    )

    old_backup = tmp_path / "backup_antigo.zip"
    recent_backup = tmp_path / "backup_recente.zip"

    old_backup.touch()
    recent_backup.touch()

    old_time = datetime.now().timestamp() - (40 * 86400)
    recent_time = datetime.now().timestamp() - (5 * 86400)

    os.utime(old_backup, (old_time, old_time))
    os.utime(recent_backup, (recent_time, recent_time))

    monkeypatch.setattr(
        "cleanup.get_backups",
        lambda: [old_backup, recent_backup]
    )

    check_old_backups()

    assert not old_backup.exists()
    assert recent_backup.exists()


def test_check_old_backups_missing_config(monkeypatch, tmp_path):
    backup = tmp_path / "backup_antigo.zip"
    backup.touch()

    monkeypatch.setattr("cleanup.load_config", lambda: None)
    monkeypatch.setattr("cleanup.get_backups", lambda: [backup])

    check_old_backups()

    assert backup.exists()


def test_check_old_backups_invalid_config(monkeypatch, tmp_path):
    backup = tmp_path / "backup_antigo.zip"
    backup.touch()

    def invalid_config():
        raise ValueError("Configuracao invalida")

    monkeypatch.setattr("cleanup.load_config", invalid_config)
    monkeypatch.setattr("cleanup.get_backups", lambda: [backup])

    check_old_backups()

    assert backup.exists()