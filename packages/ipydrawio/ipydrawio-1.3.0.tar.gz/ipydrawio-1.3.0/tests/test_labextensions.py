"""minimal tests of metadata"""

# Copyright 2023 ipydrawio contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ipydrawio


def test_version():
    assert ipydrawio.__version__


def test_js():
    assert ipydrawio.__js__


def test_labextensions():
    assert len(ipydrawio._jupyter_labextension_paths()) == 4, "no labextensions"
