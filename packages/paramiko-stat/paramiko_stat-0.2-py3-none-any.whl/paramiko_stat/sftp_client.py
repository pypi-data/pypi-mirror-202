# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of Paramiko.
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
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.

import stat

from paramiko.common import DEBUG
from paramiko.sftp_client import SFTPClient as _SFTPClient


class SFTPClient(_SFTPClient):
    def exists(self, path):
        """
        Check a path to determine whether it exists, based on `stat`.
        This follows symlinks, so a broken symlink will return ``False``.
        :param str path: path to check
        :rtype: bool
        :return: ``True`` if the path exists and is not a broken symlink;
            ``False`` otherwise
        .. versionadded:: 2.5
        """
        path = self._adjust_cwd(path)
        self._log(DEBUG, "exists({!r})".format(path))

        try:
            self.stat(path)
        except (OSError, IOError) as e:
            self._log(
                DEBUG,
                "{}: {} ({!r})".format(
                    type(e).__name__,
                    e.strerror,
                    e.filename if e.filename is not None else path,
                ),
            )
            return False

        return True

    def lexists(self, path):
        """
        Check a path to determine whether it exists, based on `lstat`.
        This does not follow symlinks, so a broken symlink will return
        ``True``.
        :param str path: path to check
        :rtype: bool
        :return: ``True`` if the path exists;
            ``False`` otherwise
        .. versionadded:: 2.5
        """
        path = self._adjust_cwd(path)
        self._log(DEBUG, "exists({!r})".format(path))

        try:
            self.lstat(path)
        except (OSError, IOError) as e:
            self._log(
                DEBUG,
                "{}: {} ({!r})".format(
                    type(e).__name__,
                    e.strerror,
                    e.filename if e.filename is not None else path,
                ),
            )
            return False

        return True

    def isfile(self, path):
        """
        Check a path to determine whether it exists and is a file.
        :param str path: path to check
        :rtype: bool
        :return: ``True`` if the path exists and is a file;
            ``False`` otherwise
        .. versionadded:: 2.5
        """
        path = self._adjust_cwd(path)
        self._log(DEBUG, "isfile({!r})".format(path))

        try:
            path_stat = self.stat(path)
        except (OSError, IOError) as e:
            self._log(
                DEBUG,
                "{}: {} ({!r})".format(
                    type(e).__name__,
                    e.strerror,
                    e.filename if e.filename is not None else path,
                ),
            )
            return False

        return stat.S_ISREG(path_stat.st_mode)

    def islink(self, path):
        """
        Check a path to determine whether it exists and is a symlink.
        :param str path: path to check
        :rtype: bool
        :return: ``True`` if the path exists and is a symlink;
            ``False`` otherwise
        .. versionadded:: 2.5
        """
        path = self._adjust_cwd(path)
        self._log(DEBUG, "isfile({!r})".format(path))

        try:
            path_lstat = self.lstat(path)
        except (OSError, IOError) as e:
            self._log(
                DEBUG,
                "{}: {} ({!r})".format(
                    type(e).__name__,
                    e.strerror,
                    e.filename if e.filename is not None else path,
                ),
            )
            return False

        return stat.S_ISLNK(path_lstat.st_mode)

    def isdir(self, path):
        """
        Check a path to determine whether it exists and is a directory.
        :param str path: path to check
        :rtype: bool
        :return: ``True`` if the path exists and is a directory;
            ``False`` otherwise
        .. versionadded:: 2.5
        """
        path = self._adjust_cwd(path)
        self._log(DEBUG, "isfile({!r})".format(path))

        try:
            path_stat = self.stat(path)
        except (OSError, IOError) as e:
            self._log(
                DEBUG,
                "{}: {} ({!r})".format(
                    type(e).__name__,
                    e.strerror,
                    e.filename if e.filename is not None else path,
                ),
            )
            return False

        return stat.S_ISDIR(path_stat.st_mode)


class SFTP(SFTPClient):
    """
    An alias for `.SFTPClient` for backwards compatibility.
    """
