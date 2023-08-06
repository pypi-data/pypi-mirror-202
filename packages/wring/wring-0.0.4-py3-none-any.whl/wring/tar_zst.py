# based on https://gist.github.com/scivision/ad241e9cf0474e267240e196d7545eca

import os
import tarfile
import tempfile
from pathlib import Path
from typing import Optional

import typer
import zstandard
from rich import console, print

from ._app import app


def extract_zst(archive: Path, out_path: Path):
    """
    extract .zst file
    works on Windows, Linux, MacOS, etc.

    Parameters
    ----------
    archive: pathlib.Path or str
      .zst file to extract
    out_path: pathlib.Path or str
      directory to extract files and directories to
    """
    c = console.Console()

    if zstandard is None:
        raise ImportError("pip install zstandard")

    archive = Path(archive).expanduser()
    out_path = Path(out_path).expanduser().resolve()
    # need .resolve() in case intermediate relative dir doesn't exist

    dctx = zstandard.ZstdDecompressor()

    if archive.exists() and archive.suffix != ".part000":
        c.print(f"extracting from {archive}")
        with c.status("decompressing..."):
            with tempfile.TemporaryFile(suffix=".tar") as ofh:
                with archive.open("rb") as ifh:
                    dctx.copy_stream(ifh, ofh)
                ofh.seek(0)
                with tarfile.open(fileobj=ofh) as z:
                    z.extractall(out_path)
        c.print(f"extracted to {out_path}")
        return

    if archive.suffix == ".part000":
        archive_part0 = archive
    else:
        archive_part0 = archive.with_name(archive.name + ".part000")

    if archive_part0.exists():
        c.print(f"extracting from {archive}")
        with c.status("decompressing multipart tar") as s:
            dobj = dctx.decompressobj()
            n = 0
            with tempfile.TemporaryFile(suffix=".tar") as ofh:
                while archive_part0.with_suffix(f".part{n:03}").exists():
                    with archive_part0.with_suffix(f".part{n:03}").open("rb") as ifh:
                        s.update(f"reading part{n:03}")
                        blob = dobj.decompress(ifh.read())
                        s.update(f"writing part{n:03} to temp.tar")
                        ofh.write(blob)
                    n += 1
                s.update(f"extracting from temp.tar to {out_path}")
                ofh.seek(0)
                with tarfile.open(fileobj=ofh) as z:
                    z.extractall(out_path)
        c.print(f"extracted to {out_path}")
        return
    raise FileNotFoundError(archive)


def compress_zst(in_path: Path, archive: Path):
    """
    Compress a directory into a .tar.zst file.

    Certain hidden files are excluded, including .git directories and
    macOS's .DS_Store files.

    Parameters
    ----------
    in_path: pathlib.Path or str
      directory to compress
    archive: pathlib.Path or str
      .tar.zst file to compress into
    """
    if zstandard is None:
        raise ImportError("pip install zstandard")
    dctx = zstandard.ZstdCompressor(level=9, threads=-1, write_checksum=True)
    with tempfile.TemporaryFile(suffix=".tar") as ofh:
        with tarfile.open(fileobj=ofh, mode="w") as z:
            for dirpath, dirnames, filenames in os.walk(in_path):
                if os.path.basename(dirpath) == ".git":
                    continue
                for n in range(len(dirnames) - 1, -1, -1):
                    if dirnames[n] == ".git" or dirnames[n].startswith("---"):
                        dirnames.pop(n)
                for f in filenames:
                    if f.startswith(".git") or f == ".DS_Store" or f.startswith("---"):
                        continue
                    finame = Path(os.path.join(dirpath, f))
                    arcname = finame.relative_to(in_path)
                    print(f"> {arcname}")
                    z.add(finame, arcname=arcname)
        ofh.seek(0)
        with archive.open("wb") as ifh:
            dctx.copy_stream(ofh, ifh)


def compress_zst_chunks(in_path: Path, archive: Path, chunksize=1_000_000_000):
    """
    Compress a directory into a .tar.zst file.

    Certain hidden files are excluded, including .git directories and
    macOS's .DS_Store files.

    Parameters
    ----------
    in_path: pathlib.Path or str
      directory to compress
    archive: pathlib.Path or str
      .tar.zst file to compress into
    """
    c = console.Console()

    if zstandard is None:
        raise ImportError("pip install zstandard")
    cctx = zstandard.ZstdCompressor(level=9, threads=-1, write_checksum=True)
    n = 0
    with tempfile.TemporaryFile(suffix=".tar") as ofh:
        with c.status("temp.tar <- writing...") as s:
            with tarfile.open(fileobj=ofh, mode="w") as z:
                for dirpath, dirnames, filenames in os.walk(in_path):
                    if os.path.basename(dirpath) == ".git":
                        continue
                    for n in range(len(dirnames) - 1, -1, -1):
                        if dirnames[n] == ".git" or dirnames[n].startswith("---"):
                            dirnames.pop(n)
                    for f in filenames:
                        if (
                            f.startswith(".git")
                            or f == ".DS_Store"
                            or f.startswith("---")
                        ):
                            continue
                        finame = Path(os.path.join(dirpath, f))
                        arcname = finame.relative_to(in_path)
                        s.update(f"temp.tar <- {arcname}")
                        z.add(finame, arcname=arcname)
        ofh.seek(0)

        def archive_part(i):
            archive_basename = archive.name.split(".")[0]
            return archive.with_name(f"{archive_basename}.tar.zst.part{i:03}")

        with c.status("compressing into ...") as s:
            chunker = cctx.chunker(chunk_size=chunksize)
            while True:
                in_chunk = ofh.read(32768)
                if not in_chunk:
                    break
                for out_chunk in chunker.compress(in_chunk):
                    s.update(f"compressing into {archive_part(n)}")
                    with archive_part(n).open("wb") as ifh:
                        ifh.write(out_chunk)
                    n += 1
            for out_chunk in chunker.finish():
                s.update(f"compressing into {archive_part(n)}")
                with archive_part(n).open("wb") as ifh:
                    ifh.write(out_chunk)
                n += 1


@app.command()
def tarzst(
    directory: Path,
    archive: Optional[Path] = None,
    chunkgigs: Optional[float] = typer.Option(None, "-c", "--chunk-gigs"),
):
    directory = Path(directory)
    name = directory.name
    if not archive:
        archive = directory.with_name(name + ".tar.zst")
    if directory.exists():
        if not archive.exists():
            print(f"compressing to tar.zst: {directory}")
            if chunkgigs:
                compress_zst_chunks(directory, archive, chunksize=int(chunkgigs * 1e9))
            else:
                compress_zst(directory, archive)
        else:
            print(f"not compressing, existing tar.zst: {directory}")
    else:
        print(f"not compressing, does not exist: {directory}")


@app.command()
def untarzst(
    archive: Path,
    outdir: Optional[Path] = None,
):
    name = archive.name
    if not outdir and name.endswith(".tar.zst"):
        outdir = archive.with_name(name[:-8])
    if not outdir and name.endswith(".tar.zst.part000"):
        outdir = archive.with_name(name[:-16])
    if not outdir:
        raise ValueError("must specify output dir")
    try:
        if not outdir.exists():
            extract_zst(archive, outdir)
        else:
            print(f"not extracting, existing target: {outdir}")
    except FileNotFoundError:
        print(f"not extracting, does not exist: {archive}")
    except Exception as err:
        print(f"not extracting, error: {err}")
