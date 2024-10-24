# vfs.py
#
# LICENSE
#
# The MIT License
#
# Copyright (c) 2020 TileDB, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# DESCRIPTION
#
# Please see the TileDB documentation for more information:
#  https://docs.tiledb.com/main/how-to/virtual-filesystem
#
# This program explores the various TileDB VFS tools.
#

import os
import struct

import tiledb


def path(p):
    return os.path.join(os.getcwd(), p)


def dirs_files():
    # Create TileDB VFS
    vfs = tiledb.VFS()

    # Create directory
    if not vfs.is_dir("dir_A"):
        vfs.create_dir(path("dir_A"))
        print("Created 'dir_A'")
    else:
        print("'dir_A' already exists")

    # Creating an (empty) file
    if not vfs.is_file("dir_A/file_A"):
        vfs.touch(path("dir_A/file_A"))
        print("Created empty file 'dir_A/file_A'")
    else:
        print("'dir_A/file_A' already exists")

    # Getting the file size
    print("Size of file 'dir_A/file_A': {}".format(vfs.file_size(path("dir_A/file_A"))))

    # Moving files (moving directories is similar)
    print("Moving file 'dir_A/file_A' to 'dir_A/file_B'")
    vfs.move_file(path("dir_A/file_A"), path("dir_A/file_B"))

    # Deleting files and directories
    print("Deleting 'dir_A/file_B' and 'dir_A'")
    vfs.remove_file(path("dir_A/file_B"))
    vfs.remove_dir(path("dir_A"))


def write():
    # Create TileDB VFS
    vfs = tiledb.VFS()

    # Write binary data
    with vfs.open("tiledb_vfs.bin", "wb") as f:
        f.write(struct.pack("f", 153.0))
        f.write("abcd".encode("utf-8"))

    # Write binary data again - this will overwrite the previous file
    with vfs.open("tiledb_vfs.bin", "wb") as f:
        f.write(struct.pack("f", 153.1))
        f.write("abcdef".encode("utf-8"))

    # Append binary data to existing file (this will NOT work on S3)
    with vfs.open("tiledb_vfs.bin", "ab") as f:
        f.write("ghijkl".encode("utf-8"))


def read():
    # Create TileDB VFS
    vfs = tiledb.VFS()

    # Read binary data
    with vfs.open("tiledb_vfs.bin", "rb") as f:
        # Read the first 4 bytes (bytes [0:4])
        f1 = struct.unpack("f", f.read(4))[0]

        # Read the next 8 bytes (bytes [4:12])
        s1 = bytes.decode(f.read(8), "utf-8")

        print(f"Binary read:\n{f1}\n{s1}")


dirs_files()
write()
read()
