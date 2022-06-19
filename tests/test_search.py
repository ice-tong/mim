# Copyright (c) OpenMMLab. All rights reserved.
import os.path as osp
import shutil
import sys

from click.testing import CliRunner

from mim.commands.install import cli as install
from mim.commands.search import cli as search
from mim.commands.uninstall import cli as uninstall
from mim.utils import DEFAULT_CACHE_DIR


def test_search(tmp_path):
    sys.path.append(str(tmp_path))
    runner = CliRunner()
    result = runner.invoke(install, ['mmcls', '--yes', '-t', str(tmp_path)])
    assert result.exit_code == 0

    # mim search mmcls
    result = runner.invoke(search, ['mmcls'])
    assert result.exit_code == 0

    # mim search mmcls --remote
    # search master branch
    result = runner.invoke(search, ['mmcls', '--remote'])
    assert result.exit_code == 0
    # mim search mmsegmentation --remote
    result = runner.invoke(search, ['mmsegmentation', '--remote'])
    assert result.exit_code == 0
    # mim search mmaction2 --remote
    result = runner.invoke(search, ['mmaction2', '--remote'])
    assert result.exit_code == 0

    # mim search mmcls==0.11.0 --remote
    result = runner.invoke(search, ['mmcls==0.11.0', '--remote'])
    assert result.exit_code == 0
    # the metadata of mmcls==0.11.0 will be saved in cache
    assert osp.exists(osp.join(DEFAULT_CACHE_DIR, 'mmcls-0.11.0.pkl'))

    # always test latest mmcls
    result = runner.invoke(uninstall, ['mmcls', '--yes'])
    assert result.exit_code == 0

    result = runner.invoke(install, ['mmcls', '--yes', '-t', str(tmp_path)])
    assert result.exit_code == 0

    # mim search mmcls --model res
    # invalid model
    result = runner.invoke(search, ['mmcls', '--model', 'res'])
    assert result.exit_code == 1
    # mim search mmcls --model resnet
    result = runner.invoke(search, ['mmcls', '--model', 'resnet'])
    assert result.exit_code == 0

    # mim search mmcls --valid-config
    result = runner.invoke(search, ['mmcls', '--valid-config'])
    assert result.exit_code == 0

    # mim search mmcls --config resnet18_b16x8_cifar1
    # invalid config
    result = runner.invoke(search,
                           ['mmcls', '--config', 'resnet18_b16x8_cifar1'])
    assert result.exit_code == 1
    # mim search mmcls --config resnet18_b16x8_cifar10
    result = runner.invoke(search,
                           ['mmcls', '--config', 'resnet18_8xb16_cifar10'])
    assert result.exit_code == 0

    # mim search mmcls --dataset cifar-1
    # invalid dataset
    result = runner.invoke(search, ['mmcls', '--dataset', 'cifar-1'])
    assert result.exit_code == 1

    # mim search mmcls --dataset cifar-10
    result = runner.invoke(search, ['mmcls', '--dataset', 'cifar-10'])
    assert result.exit_code == 0

    # mim search mmcls --condition 'batch_size>45,epochs>100'
    result = runner.invoke(
        search, ['mmcls', '--condition', 'batch_size>45,epochs>100'])
    assert result.exit_code == 0

    # mim search mmcls --condition 'batch_size>45 epochs>100'
    result = runner.invoke(
        search, ['mmcls', '--condition', 'batch_size>45 epochs>100'])
    assert result.exit_code == 0

    # mim search mmcls --condition '128<batch_size<=256'
    result = runner.invoke(search,
                           ['mmcls', '--condition', '128<batch_size<=256'])
    assert result.exit_code == 0

    # mim search mmcls --sort epoch
    result = runner.invoke(search, ['mmcls', '--sort', 'epoch'])
    assert result.exit_code == 0
    # mim search mmcls --sort epochs
    result = runner.invoke(search, ['mmcls', '--sort', 'epochs'])
    assert result.exit_code == 0

    # mim search mmcls --sort batch_size epochs
    result = runner.invoke(search, ['mmcls', '--sort', 'batch_size', 'epochs'])
    assert result.exit_code == 0

    # mim search mmcls --field epoch
    result = runner.invoke(search, ['mmcls', '--field', 'epoch'])
    assert result.exit_code == 0
    # mim search mmcls --field epochs
    result = runner.invoke(search, ['mmcls', '--field', 'epochs'])
    assert result.exit_code == 0

    shutil.rmtree(tmp_path)
