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

from abc import ABC
from typing import List, Optional, Tuple, Union

from lightning.fabric import Fabric
from lightning.fabric.connector import _PLUGIN_INPUT as _LITE_PLUGIN_INPUT
from lightning.fabric.connector import _PRECISION_INPUT
from lightning.fabric.plugins import CheckpointIO, ClusterEnvironment
from lightning.fabric.plugins import DeepSpeedPrecision as LiteDeepSpeedPrecision
from lightning.fabric.plugins import DoublePrecision as LiteDoublePrecision
from lightning.fabric.plugins import MixedPrecision as LiteMixedPrecision
from lightning.fabric.plugins import Precision as LitePrecision
from lightning.fabric.plugins import TPUBf16Precision as LiteTPUBf16Precision
from lightning.fabric.plugins import TPUPrecision as LiteTPUPrecision
from lightning.fabric.strategies import DataParallelStrategy as LiteDataParallelStrategy
from lightning.fabric.strategies import DDPStrategy as LiteDDPStrategy
from lightning.fabric.strategies import DeepSpeedStrategy as LiteDeepSpeedStrategy
from lightning.fabric.strategies import SingleDeviceStrategy as LiteSingleDeviceStrategy
from lightning.fabric.strategies import SingleTPUStrategy as LiteSingleTPUStrategy
from lightning.fabric.strategies import Strategy as LiteStrategy
from lightning.fabric.strategies import XLAStrategy
from lightning.pytorch.accelerators import Accelerator as PLAccelerator
from lightning.pytorch.plugins import DeepSpeedPrecisionPlugin as PLDeepSpeedPrecisionPlugin
from lightning.pytorch.plugins import DoublePrecisionPlugin as PLDoublePrecisionPlugin
from lightning.pytorch.plugins import MixedPrecisionPlugin as PLMixedPrecisionPlugin
from lightning.pytorch.plugins import PrecisionPlugin as PLPrecisionPlugin
from lightning.pytorch.plugins import TPUBf16PrecisionPlugin as PLTPUBf16PrecisionPlugin
from lightning.pytorch.plugins import TPUPrecisionPlugin as PLTPUPrecisionPlugin
from lightning.pytorch.strategies import DataParallelStrategy as PLDataParallelStrategy
from lightning.pytorch.strategies import DDPShardedStrategy as PLDDPShardedStrategy
from lightning.pytorch.strategies import DDPSpawnShardedStrategy as PLDDPSpawnShardedStrategy
from lightning.pytorch.strategies import DDPSpawnStrategy as PLDDPSpawnStrategy
from lightning.pytorch.strategies import DDPStrategy as PLDDPStrategy
from lightning.pytorch.strategies import DeepSpeedStrategy as PLDeepSpeedStrategy
from lightning.pytorch.strategies import SingleDeviceStrategy as PLSingleDeviceStrategy
from lightning.pytorch.strategies import SingleTPUStrategy as PLSingleTPUStrategy
from lightning.pytorch.strategies import Strategy as PLStrategy
from lightning.pytorch.strategies import TPUSpawnStrategy as PLTPUSpawnStrategy
from lightning.pytorch.utilities.rank_zero import rank_zero_deprecation, rank_zero_warn

_PL_PLUGIN = Union[PLPrecisionPlugin, ClusterEnvironment, CheckpointIO]
_PL_PLUGIN_INPUT = Union[_PL_PLUGIN, str]


class LightningLite(Fabric, ABC):
    """Lite accelerates your PyTorch training or inference code with minimal changes required.

    .. deprecated:: v1.9.0
        The `lightning.pytorch.lite.LightningLite` class was deprecated in v1.9.0 and will be renamed to
        `lightning.fabric.Fabric` in v2.0.0. It is no longer part of the pure `lightning.pytorch` package, and now
        lives in the main `lightning` package.

    - Automatic placement of models and data onto the device.
    - Automatic support for mixed and double precision (smaller memory footprint).
    - Seamless switching between hardware (CPU, GPU, TPU) and distributed training strategies
      (data-parallel training, sharded training, etc.).
    - Automated spawning of processes, no launch utilities required.
    - Multi-node support.

    Args:
        accelerator: The hardware to run on. Possible choices are:
            ``"cpu"``, ``"cuda"``, ``"mps"``, ``"gpu"``, ``"tpu"``, ``"auto"``.
        strategy: Strategy for how to run across multiple devices. Possible choices are:
            ``"dp"``, ``"ddp"``, ``"ddp_spawn"``, ``"deepspeed"``, ``"fsdp"``.
        devices: Number of devices to train on (``int``), which GPUs to train on (``list`` or ``str``), or ``"auto"``.
            The value applies per node.
        num_nodes: Number of GPU nodes for distributed training.
        precision: Double precision (``64``), full precision (``32``), half precision (``16``),
            or bfloat16 precision (``"bf16"``).
        plugins: One or several custom plugins
        gpus: Provides the same function as the ``devices`` argument but implies ``accelerator="gpu"``.

            .. deprecated:: v1.8.0
                ``gpus`` has been deprecated in v1.8.0 and will be removed in v2.0.0.
                Please use ``accelerator='gpu'`` and ``devices=x`` instead.

        tpu_cores: Provides the same function as the ``devices`` argument but implies ``accelerator="tpu"``.

            .. deprecated:: v1.8.0
                ``tpu_cores`` has been deprecated in v1.8.0 and will be removed in v2.0.0.
                Please use ``accelerator='tpu'`` and ``devices=x`` instead.
    """

    def __init__(
        self,
        accelerator: Optional[Union[str, PLAccelerator]] = None,
        strategy: Optional[Union[str, PLStrategy]] = None,
        devices: Optional[Union[List[int], str, int]] = None,
        num_nodes: int = 1,
        precision: _PRECISION_INPUT = 32,
        plugins: Optional[Union[_PL_PLUGIN_INPUT, List[_PL_PLUGIN_INPUT]]] = None,
        gpus: Optional[Union[List[int], str, int]] = None,
        tpu_cores: Optional[Union[List[int], str, int]] = None,
    ) -> None:

        rank_zero_deprecation(
            "The `lightning.pytorch.lite.LightningLite` class was deprecated in v1.9.0 and will be renamed to"
            " `lightning.fabric.Fabric` in v2.0.0."
        )

        if gpus is not None or tpu_cores is not None:
            devices, accelerator = _convert_deprecated_device_flags(
                accelerator=accelerator,
                devices=devices,
                gpus=gpus,
                tpu_cores=tpu_cores,
            )

        lite_plugins: Optional[Union[_LITE_PLUGIN_INPUT, List[_LITE_PLUGIN_INPUT]]]
        if isinstance(plugins, PLPrecisionPlugin):
            lite_plugins = _to_lite_precision(plugins)
        elif isinstance(plugins, list):
            lite_plugins = [
                _to_lite_precision(plugin) if isinstance(plugin, PLPrecisionPlugin) else plugin for plugin in plugins
            ]
        else:
            lite_plugins = plugins

        if type(strategy) in (PLDDPShardedStrategy, PLDDPSpawnShardedStrategy) or strategy in (
            "ddp_sharded",
            "ddp_sharded_spawn",
        ):
            spawn_message = ""
            if type(strategy) is PLDDPSpawnShardedStrategy or strategy == "ddp_sharded_spawn":
                spawn_message = ", start_method='spawn'"
            raise RuntimeError(
                "LightningLite's sharded implementation using FairScale has been removed in favor of PyTorch's FSDP."
                " You can try"
                f" `Fabric(strategy=FSDPStrategy(sharding_strategy=ShardingStrategy.SHARD_GRAD_OP{spawn_message}))`"
                " which implements optimizer-only sharding à la ZeRO-2. Or full sharding with `Fabric(strategy='fsdp')`"
            )

        super().__init__(
            accelerator=accelerator,
            strategy=(_to_lite_strategy(strategy) if isinstance(strategy, PLStrategy) else strategy),
            devices=devices,
            num_nodes=num_nodes,
            precision=precision,
            plugins=lite_plugins,
        )


def _convert_deprecated_device_flags(
    accelerator: Optional[Union[str, PLAccelerator]],
    devices: Optional[Union[List[int], str, int]],
    gpus: Optional[Union[List[int], str, int]],
    tpu_cores: Optional[Union[List[int], str, int]],
) -> Tuple[Optional[Union[List[int], str, int]], Optional[Union[str, PLAccelerator]]]:
    """Emit deprecation warnings for gpus and tpu_cores and translate them into the new accelerator and devices.

    Similar implementation as in ``lightning.pytorch.trainer.connectors.accelerator_connector``.
    """
    if gpus is not None:
        rank_zero_deprecation(
            f"Setting `Lite(gpus={gpus!r})` is deprecated in v1.8.0 and will be removed"
            f" in v2.0.0. Please use `Lite(accelerator='gpu', devices={gpus!r})` instead."
        )
    if tpu_cores is not None:
        rank_zero_deprecation(
            f"Setting `Lite(tpu_cores={tpu_cores!r})` is deprecated in v1.8.0 and will be removed"
            f" in v2.0.0. Please use `Lite(accelerator='tpu', devices={tpu_cores!r})` instead."
        )
    deprecated_devices_specific_flag = gpus or tpu_cores
    if deprecated_devices_specific_flag and deprecated_devices_specific_flag not in ([], 0, "0"):
        if devices:
            rank_zero_warn(
                f"The option `devices={devices}` will be ignored and the device specific number"
                f"{deprecated_devices_specific_flag} will be used instead."
            )

        if gpus is not None and tpu_cores is not None:
            rank_zero_warn(
                f"Both `Lite(gpus={gpus!r}, tpu_cores={tpu_cores!r})` were specified. Please choose only one of"
                " the two."
            )

        if accelerator is None:
            if tpu_cores:
                accelerator = "tpu"
            if gpus:
                accelerator = "cuda"

    return deprecated_devices_specific_flag, accelerator


def _to_lite_strategy(strategy: PLStrategy) -> LiteStrategy:
    """Re-instantiates a PL-Strategy as the corresponding Lite-Strategy."""
    strategy_cls = type(strategy)
    if strategy_cls is PLDDPStrategy:
        return LiteDDPStrategy(
            accelerator=strategy.accelerator,
            parallel_devices=strategy.parallel_devices,
            cluster_environment=strategy.cluster_environment,
            checkpoint_io=strategy.checkpoint_io,
            precision=_to_lite_precision(strategy.precision_plugin),
            process_group_backend=strategy.process_group_backend,
            timeout=strategy._timeout,
            **strategy._ddp_kwargs,
        )

    if strategy_cls is PLDDPSpawnStrategy:
        return LiteDDPStrategy(
            accelerator=strategy.accelerator,
            parallel_devices=strategy.parallel_devices,
            cluster_environment=strategy.cluster_environment,
            checkpoint_io=strategy.checkpoint_io,
            precision=_to_lite_precision(strategy.precision_plugin),
            process_group_backend=strategy.process_group_backend,
            timeout=strategy._timeout,
            start_method=strategy._start_method,
            **strategy._ddp_kwargs,
        )

    if strategy_cls is PLTPUSpawnStrategy:
        return XLAStrategy(
            accelerator=strategy.accelerator,
            parallel_devices=strategy.parallel_devices,
            checkpoint_io=strategy.checkpoint_io,
            precision=_to_lite_precision(strategy.precision_plugin),
        )

    if strategy_cls is PLDeepSpeedStrategy:
        return LiteDeepSpeedStrategy(
            accelerator=strategy.accelerator,
            parallel_devices=strategy.parallel_devices,
            cluster_environment=strategy.cluster_environment,
            precision=_to_lite_precision(strategy.precision_plugin),
            process_group_backend=strategy.process_group_backend,
            config=strategy.config,
            remote_device=strategy.remote_device,
            load_full_weights=strategy.load_full_weights,
            loss_scale=strategy.loss_scale,
            initial_scale_power=strategy.initial_scale_power,
            loss_scale_window=strategy.loss_scale_window,
            hysteresis=strategy.hysteresis,
            min_loss_scale=strategy.min_loss_scale,
        )

    if strategy_cls is PLDataParallelStrategy:
        return LiteDataParallelStrategy(
            accelerator=strategy.accelerator,
            parallel_devices=strategy.parallel_devices,
            checkpoint_io=strategy.checkpoint_io,
            precision=_to_lite_precision(strategy.precision_plugin),
        )

    if strategy_cls is PLSingleDeviceStrategy:
        return LiteSingleDeviceStrategy(
            device=strategy.root_device,
            accelerator=strategy.accelerator,
            checkpoint_io=strategy.checkpoint_io,
            precision=_to_lite_precision(strategy.precision_plugin),
        )

    if strategy_cls is PLSingleTPUStrategy:
        return LiteSingleTPUStrategy(
            device=strategy.root_device.index,
            accelerator=strategy.accelerator,
            checkpoint_io=strategy.checkpoint_io,
            precision=_to_lite_precision(strategy.precision_plugin),
        )
    raise NotImplementedError(f"Unsupported strategy: `{strategy_cls.__name__}`")


def _to_lite_precision(plugin: Optional[PLPrecisionPlugin]) -> LitePrecision:
    """Re-instantiates a PL-PrecisionPlugin as the corresponding Lite-Precision plugin."""

    if type(plugin) is PLPrecisionPlugin:
        return LitePrecision()

    if type(plugin) is PLMixedPrecisionPlugin:
        return LiteMixedPrecision(
            precision=plugin.precision, device=plugin.device, scaler=plugin.scaler  # type: ignore[arg-type]
        )

    if type(plugin) is PLDoublePrecisionPlugin:
        return LiteDoublePrecision()

    if type(plugin) is PLDeepSpeedPrecisionPlugin:
        return LiteDeepSpeedPrecision(
            precision=plugin.precision,  # type: ignore[arg-type]
        )

    if type(plugin) is PLTPUPrecisionPlugin:
        return LiteTPUPrecision()

    if type(plugin) is PLTPUBf16PrecisionPlugin:
        return LiteTPUBf16Precision()

    # No backward compatibility for custom plugins / subclasses, as we can't re-instantiate these plugins
    raise TypeError(
        "You passed an unsupported plugin as input to Lite(plugins=...) or to a strategy. If you built a custom plugin,"
        " please change it to subclass the `lightning_lite.plugins.precision.Precision` class. Otherwise, please open"
        " an issue on the Lightning GitHub repository with your use case."
    )
