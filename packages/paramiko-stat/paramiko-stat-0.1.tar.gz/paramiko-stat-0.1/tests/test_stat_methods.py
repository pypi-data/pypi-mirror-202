# Copyright (C) 2003-2009  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.

"""
some unit tests to make sure sftp works.
a real actual sftp server is contacted, and a new folder is created there to
do test file operations in (so no existing files will be harmed).
"""

import pytest

from .util import slow

ARTICLE = """
Insulin sensitivity and liver insulin receptor structure in ducks from two
genera
T. Constans, B. Chevalier, M. Derouet and J. Simon
Station de Recherches Avicoles, Institut National de la Recherche Agronomique,
Nouzilly, France.
Insulin sensitivity and liver insulin receptor structure were studied in
5-wk-old ducks from two genera (Muscovy and Pekin). In the fasting state, both
duck types were equally resistant to exogenous insulin compared with chicken.
Despite the low potency of duck insulin, the number of insulin receptors was
lower in Muscovy duck and similar in Pekin duck and chicken liver membranes.
After 125I-insulin cross-linking, the size of the alpha-subunit of the
receptors from the three species was 135,000. Wheat germ agglutinin-purified
receptors from the three species were contaminated by an active and unusual
adenosinetriphosphatase (ATPase) contaminant (highest activity in Muscovy
duck). Sequential purification of solubilized receptor from both duck types on
lentil and then wheat germ agglutinin lectins led to a fraction of receptors
very poor in ATPase activity that exhibited a beta-subunit size (95,000) and
tyrosine kinase activity similar to those of ATPase-free chicken insulin
receptors. Therefore the ducks from the two genera exhibit an alpha-beta-
structure for liver insulin receptors and a clear difference in the number of
liver insulin receptors. Their sensitivity to insulin is, however, similarly
decreased compared with chicken.
"""


# Here is how unicode characters are encoded over 1 to 6 bytes in utf-8
# U-00000000 - U-0000007F: 0xxxxxxx
# U-00000080 - U-000007FF: 110xxxxx 10xxxxxx
# U-00000800 - U-0000FFFF: 1110xxxx 10xxxxxx 10xxxxxx
# U-00010000 - U-001FFFFF: 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
# U-00200000 - U-03FFFFFF: 111110xx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx
# U-04000000 - U-7FFFFFFF: 1111110x 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx
# Note that: hex(int('11000011',2)) == '0xc3'
# Thus, the following 2-bytes sequence is not valid utf8: "invalid continuation byte"
NON_UTF8_DATA = b"\xC3\xC3"

unicode_folder = "\u00fcnic\u00f8de"
utf8_folder = b"/\xc3\xbcnic\xc3\xb8\x64\x65"


@slow
class TestSFTP(object):
    def test_exists(self, sftp):
        filename = "exists.txt"
        symlink_name = "also_exists.txt"

        file_path = "{}/{}".format(sftp.FOLDER, filename)
        symlink_path = "{}/{}".format(sftp.FOLDER, symlink_name)

        try:
            sftp.open(file_path, "w")

            assert sftp.exists(file_path)

            try:
                sftp.symlink(filename, symlink_path)

                assert sftp.exists(file_path)
                assert sftp.exists(symlink_path)
            finally:
                sftp.remove(symlink_path)
        finally:
            sftp.remove(file_path)

        assert not sftp.exists(symlink_path)
        assert not sftp.exists(file_path)

    def test_lexists(self, sftp):
        filename = "exists.txt"
        symlink_name = "also_exists.txt"

        file_path = "{}/{}".format(sftp.FOLDER, filename)
        symlink_path = "{}/{}".format(sftp.FOLDER, symlink_name)

        try:
            sftp.open(file_path, "w")

            assert sftp.lexists(file_path)

            try:
                sftp.symlink(filename, symlink_path)

                assert sftp.lexists(file_path)
                assert sftp.lexists(symlink_path)
            finally:
                sftp.remove(symlink_path)
        finally:
            sftp.remove(file_path)

        assert not sftp.lexists(symlink_path)
        assert not sftp.lexists(file_path)

        try:
            sftp.symlink(filename, symlink_path)

            assert not sftp.lexists(file_path)
            assert sftp.lexists(symlink_path)
        finally:
            sftp.remove(symlink_path)

        assert not sftp.lexists(symlink_path)
        assert not sftp.lexists(file_path)

    def test_isfile(self, sftp):
        filename = "exists.txt"
        symlink_name = "also_exists.txt"

        file_path = "{}/{}".format(sftp.FOLDER, filename)
        symlink_path = "{}/{}".format(sftp.FOLDER, symlink_name)

        try:
            sftp.open(file_path, "w")

            assert sftp.isfile(file_path)

            try:
                sftp.symlink(filename, symlink_path)

                assert sftp.isfile(file_path)
                assert sftp.isfile(symlink_path)
            finally:
                sftp.remove(symlink_path)
        finally:
            sftp.remove(file_path)

        assert not sftp.isfile(symlink_path)
        assert not sftp.isfile(file_path)

    def test_islink(self, sftp):
        filename = "exists.txt"
        symlink_name = "also_exists.txt"

        file_path = "{}/{}".format(sftp.FOLDER, filename)
        symlink_path = "{}/{}".format(sftp.FOLDER, symlink_name)

        try:
            sftp.open(file_path, "w")

            assert not sftp.islink(file_path)

            try:
                sftp.symlink(filename, symlink_path)

                assert not sftp.islink(file_path)
                assert sftp.islink(symlink_path)
            finally:
                sftp.remove(symlink_path)
        finally:
            sftp.remove(file_path)

        assert not sftp.islink(symlink_path)
        assert not sftp.islink(file_path)

    def test_isdir(self, sftp):
        dirname = "exists"
        symlink_dirname = "also_exists"

        dir_path = "{}/{}".format(sftp.FOLDER, dirname)
        symlink_dir_path = "{}/{}".format(sftp.FOLDER, symlink_dirname)

        try:
            sftp.mkdir(dir_path)

            assert sftp.isdir(dir_path)

            try:
                sftp.symlink(dirname, symlink_dir_path)

                assert sftp.isdir(dir_path)
                assert sftp.isdir(symlink_dir_path)
            finally:
                sftp.remove(symlink_dir_path)
        finally:
            sftp.rmdir(dir_path)

        assert not sftp.isdir(symlink_dir_path)
        assert not sftp.isdir(dir_path)
