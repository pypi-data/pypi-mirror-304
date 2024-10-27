#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2021-2022 Luis López <luis@cuarentaydos.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.


import os
import unittest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

from globalomnium import Client, get_session, get_credentials
from globalomnium.client import _LOGIN_ENDPOINT

FIXTURES_DIR = os.path.dirname(__file__) + "/fixtures"


def read_fixture(fixture_name: str):
    with open(f"{FIXTURES_DIR}/{fixture_name}.bin", "rb") as fh:
        return fh.read()


class TestClient(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        u, p = get_credentials(credentials="credentials.json")
        self.sess = await get_session()
        self.client = Client(None, u, p)
        #self.client = Client(self.sess, u, p) 
        self.end = datetime.now().replace(hour=0, minute=0, second=0)
        self.start = self.end - timedelta(days=7)

    async def asyncTearDown(self):
        await self.sess.close()

    async def test_login_ok(self):
        with patch(
            "globalomnium.Client.request_bytes",
            new_class=AsyncMock,
            return_value=read_fixture("login-ok"),
        ) as fn:
            await self.client.login()

        fn.assert_awaited_once()

        args, kwargs = fn.call_args
        self.assertEqual(args, ("POST", _LOGIN_ENDPOINT))

    @patch("globalomnium.Client.is_logged", return_value=True)
    async def test_historical_consumption(self, _):
        with patch(
            "globalomnium.Client.request_bytes",
            new_class=AsyncMock,
            return_value=read_fixture("historical-consumption"),
        ):
            ret = await self.client.get_historical_consumption(self.start, self.end)

            self.assertEqual(ret["accumulated"], 97871.0)
            #self.assertEqual(ret["accumulated-co2"], 23586.91)


if __name__ == "__main__":
    unittest.main()
