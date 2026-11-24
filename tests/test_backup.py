import sys 
from zipfile import ZipFile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import backup
from backup import create_backup


def test_create_backup_directory_not_found(tmp_path):
    source = tmp_path / "diretorio_inexistente"

    with pytest.raises(FileNotFoundError):
        create_backup(source)


def test_create_backup_not_a_directory(tmp_path):
    source = tmp_path / "arquivo.txt"
    source.touch()

    with pytest.raises(NotADirectoryError):
        create_backup(source)


def test_create_backup_empty_directory(tmp_path):
    source = tmp_path / "diretorio_vazio"
    source.mkdir()

    with pytest.raises(ValueError):
        create_backup(source)


def test_create_backup_success(tmp_path):
    source = tmp_path / "arquivos"
    source.mkdir()

    arquivo = source / "documento.txt"
    arquivo.write_text("Conteudo de teste")

    backup = create_backup(source)

    assert backup.exists()
    assert backup.suffix == ".zip"


def test_create_backup_contains_files(tmp_path):
    source = tmp_path / "arquivos"
    source.mkdir()

    arquivo = source / "documento.txt"
    arquivo.write_text("Conteudo de teste")

    backup = create_backup(source)

    with ZipFile(backup, "r") as zip_file:
        assert "documento.txt" in zip_file.namelist()


def test_create_backup_preserves_directory_structure(tmp_path):
    source = tmp_path / "arquivos"
    subfolder = source / "documentos" / "relatorios"
    subfolder.mkdir(parents = True)

    arquivo = subfolder / "anual.txt"
    arquivo.write_text("Relatorio anual")

    backup = create_backup(source)

    with ZipFile(backup, "r") as zip_file:
        assert "documentos/relatorios/anual.txt" in zip_file.namelist()


def test_create_backup_error_cleanup(monkeypatch, tmp_path):
    source = tmp_path / "arquivos"
    source.mkdir()
    (source / "documento.txt").write_text("Teste")

    created_backup_paths = []

    def simulate_error(path, *args, **kwargs):
        path = Path(path)
        path.touch()
        created_backup_paths.append(path)

        raise OSError("Erro simulado")

    monkeypatch.setattr(backup, "ZipFile", simulate_error)

    with pytest.raises(OSError, match = "Erro simulado"):
        create_backup(source)

    assert len(created_backup_paths) == 1
    assert not created_backup_paths[0].exists()

    
    