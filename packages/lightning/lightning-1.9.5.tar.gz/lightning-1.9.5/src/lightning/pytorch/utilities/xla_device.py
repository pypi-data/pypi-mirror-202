# Copyright The PyTorch Lightning team.
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

from multiprocessing import Queue
from typing import Any, Callable

from lightning.pytorch.utilities import rank_zero_deprecation


def inner_f(queue: Queue, func: Callable, *args: Any, **kwargs: Any) -> None:  # pragma: no cover
    rank_zero_deprecation(
        "`lightning.pytorch.utilities.xla_device.inner_f` has been deprecated in v1.8.0 and will be"
        " removed in v2.0.0. This class is internal but you can copy over its implementation."
    )
    from lightning.fabric.accelerators.tpu import _inner_f

    return _inner_f(queue, func, *args, **kwargs)


def pl_multi_process(func: Callable) -> Callable:
    rank_zero_deprecation(
        "`lightning.pytorch.utilities.xla_device.pl_multi_process` has been deprecated in v1.8.0 and will be"
        " removed in v2.0.0. This class is internal but you can copy over its implementation."
    )
    from lightning.fabric.accelerators.tpu import _multi_process

    return _multi_process(func)


class XLADeviceUtils:
    def __init__(self) -> None:
        rank_zero_deprecation(
            "`lightning.pytorch.utilities.xla_device.XLADeviceUtils` has been deprecated in v1.8.0 and will be"
            " removed in v2.0.0. This class is internal."
        )

    @staticmethod
    def xla_available() -> bool:
        rank_zero_deprecation(
            "`lightning.pytorch.utilities.xla_device.XLADeviceUtils.xla_available` has been deprecated in v1.8.0 and"
            " will be removed in v2.0.0. This method is internal."
        )
        from lightning.pytorch.accelerators.tpu import _XLA_AVAILABLE

        return bool(_XLA_AVAILABLE)

    @staticmethod
    def tpu_device_exists() -> bool:
        rank_zero_deprecation(
            "`lightning.pytorch.utilities.xla_device.XLADeviceUtils.tpu_device_exists` has been deprecated in v1.8.0"
            " and will be removed in v2.0.0. Please use `lightning.pytorch.accelerators.TPUAccelerator.is_available()`"
            " instead."
        )
        from lightning.pytorch.accelerators.tpu import TPUAccelerator

        return TPUAccelerator.is_available()
