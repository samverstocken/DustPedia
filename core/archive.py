#!/usr/bin/env python
# -*- coding: utf8 -*-
# **********************************
# **       DUSTPEDIA API          **
# **********************************

# Import standard modules
import os
import os.path
import zipfile
import StringIO
import shutil
import gzip
import bz2
import subprocess

# -----------------------------------------------------------------

def decompress_directory_in_place(filepath, remove=False, into_root=False):

    """
    This function ...
    :param filepath:
    :param remove:
    :param into_root:
    :return:
    """

    from .logging import log

    # Inform the user
    log.info("Decompressing '" + filepath + "' ...")

    # Tar.gz
    if filepath.endswith(".tar.gz"):

        # Determine the path of the directory
        new_path = filepath.split(".tar.gz")[0]
        dir_path = fs.directory_of(new_path)

        # Debugging
        log.debug("New path: '" + new_path + "'")
        log.debug("Decompressing in directory '" + dir_path + "' ...")

        # Decompress
        command = "tar -zxvf " + filepath + " --directory " + dir_path
        log.debug("Decompress command: '" + command + "'")
        subprocess.call(command, shell=True)

    else: raise NotImplementedError("Not implemented yet")

    if into_root:

        for path in fs.files_in_path(new_path):
            fs.move_file(path, dir_path)
        fs.remove_directory(new_path)
        new_path = dir_path

    # Remove the file
    if remove: fs.remove_file(filepath)

    # Return the new path
    return new_path

# -----------------------------------------------------------------

def decompress_file_in_place(path, remove=False):

    """
    This function ...
    :param path:
    :param remove:
    :return:
    """

    from .logging import log

    # Inform the user
    log.info("Decompressing '" + path + "' ...")

    # Check extension
    if path.endswith(".bz2"):
        new_path = path.rstrip(".bz2")
        decompress_bz2(path, new_path)
    elif path.endswith(".gz"):
        new_path = path.rstrip(".gz")
        if new_path.endswith(".tar"): new_path = new_path.split(".tar")[0]
        decompress_gz(path, new_path)
    elif path.endswith(".zip"):
        new_path = path.rstrip(".zip")
        decompress_zip(path, new_path)
    else: raise ValueError("Unrecognized archive type (must be bz2, gz [or tar.gz] or zip)")

    # Remove the original file if requested
    if remove: fs.remove_file(path)

    # Return the new path
    return new_path

# -----------------------------------------------------------------

def decompress_file(path, new_path):

    """
    This funtion ...
    :param path:
    :param new_path:
    :return:
    """

    if path.endswith(".bz2"): decompress_bz2(path, new_path)
    elif path.endswith(".gz"): decompress_gz(path, new_path)
    elif path.endswith(".zip"): decompress_zip(path, new_path)
    else: raise ValueError("Unrecognized archive type (must be bz2, gz or zip)")

# -----------------------------------------------------------------

def decompress_files(filepaths, remove=False):

    """
    This function ...
    :param filepaths:
    :param remove:
    :return:
    """

    # Initialize a list for the decompressed file paths
    new_paths = []

    # Loop over the files
    for filepath in filepaths:

        # Get the name of the file
        filename = fs.name(filepath)

        # Get directory of the file
        path = fs.directory_of(filepath)

        # Strip the bz2 extension
        newfilename = fs.strip_extension(filename)

        # Determine path to new file
        newfilepath = fs.join(path, newfilename)

        # Decompress this file
        decompress_file(filepath, newfilepath)

        # If succesful, add the new path to the list
        new_paths.append(newfilepath)

    # Remove original files if requested
    if remove: fs.remove_files(filepaths)

    # Return the list of new file paths
    return new_paths

# -----------------------------------------------------------------

def decompress_zip(zip_path, new_path):

    """
    This function decompresses a .zip file
    :param zip_path:
    :param new_path:
    :return:
    """

    with zipfile.ZipFile(zip_path, 'w') as myzip:
        myzip.write(new_path)

# -----------------------------------------------------------------

def decompress_gz(gz_path, new_path):

    """
    This function decompresses a .gz file
    :param gz_path:
    :param new_path:
    :return:
    """

    # Decompress the kernel FITS file
    with gzip.open(gz_path, 'rb') as f_in:
        with open(new_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# -----------------------------------------------------------------

def decompress_bz2(bz2_path, new_path):

    """
    This function decompresses a .bz2 file
    :param bz2_path:
    :param new_path:
    :return:
    """

    # Decompress, create decompressed new file
    with open(new_path, 'wb') as new_file, bz2.BZ2File(bz2_path, 'rb') as file:
        for data in iter(lambda: file.read(100 * 1024), b''):
            new_file.write(data)

# -----------------------------------------------------------------

## This function opens a text file in read-only mode. If a file exists at the specified path, it is simply opened.
# Otherwise, the function looks for a ZIP archive with the same name as the directory in which the file would have
# resided, but with the ".zip" extension added, and it attempts to open a file with the same name from the archive.
# In both cases, the function returns a read-only file-like object that offers sequential access, i.e. it provides
# only the following methods: read(), readline(), readlines(), \_\_iter\_\_(), next().
#
def opentext(filepath):
    # if the specified file exists, simply open it
    if os.path.isfile(filepath):
        return open(filepath, 'r')

    # otherwise, try a zip archive with the same name as the directory in which the file would have resided
    directory,filename = os.path.split(filepath)
    zippath = directory + ".zip"
    return zipfile.ZipFile(zippath,'r').open(filename,'r')

## This function opens a binary file in read-only mode. If a file exists at the specified path, it is simply opened.
# Otherwise, the function looks for a ZIP archive with the same name as the directory in which the file would have
# resided, but with the ".zip" extension added, and it attempts to open a file with the same name from the archive.
# In both cases, the function returns a read-only file-like object that offers full random access functionality.
#
# In case the file is opened from a ZIP archive, the complete file contents is loaded into a memory buffer. This is
# necessary to enable random access to the decompressed data stream.
#
def openbinary(filepath):
    # if the specified file exists, simply open it
    if os.path.isfile(filepath):
        return open(filepath, 'rb')

    # otherwise, try a zip archive with the same name as the directory in which the file would have resided
    directory,filename = os.path.split(filepath)
    zippath = directory + ".zip"
    return StringIO.StringIO(zipfile.ZipFile(zippath,'r').read(filename))

## This function returns True if the specified file exists at the specified path and/or inside a ZIP archive with
# the same name as the directory in which the file would have resided, but with the ".zip" extension added.
# Otherwise the function returns False.
#
def isfile(filepath):
    # if the specified file exists, we are done
    if os.path.isfile(filepath):
        return True

    # otherwise, try a zip archive with the same name as the directory in which the file would have resided
    directory,filename = os.path.split(filepath)
    zippath = directory + ".zip"
    if os.path.isfile(zippath):
        try:
            zipfile.ZipFile(zippath,'r').getinfo(filename)
            return True
        except KeyError:
            pass
    return False

## This function returns a sorted list of the names of the files in the specified directory and/or in the ZIP archive
# with the same name as the directory, but with the ".zip" extension added. If both the directory and the archive
# exist, the two lists are merged while removing duplicates. The returned list is optionally limited to
# filenames that end in the string (or strings) specified as the second argument to this function.
#
def listdir(dirpath, endswith=None):
    filenames = [ ]
    # if the specified directory exists, list its contents
    if os.path.isdir(dirpath):
        filenames += os.listdir(dirpath)
    # if the corresponding zip archive exists, list its contents as well
    zippath = dirpath + ".zip"
    if os.path.isfile(zippath):
        filenames += zipfile.ZipFile(zippath,'r').namelist()
    # if requested, filter the names
    if endswith != None:
        filenames = filter(lambda fn: fn.endswith(endswith), filenames)
    # remove duplicates and sort the list
    return sorted(list(set(filenames)))

# -----------------------------------------------------------------

