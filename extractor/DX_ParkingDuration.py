#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '..')
from beehive_infra.common.FxBase import FxBase
from beehive_infra.common.vatvengers.custom_logging import simple_console_logger

logger = simple_console_logger(__name__)

class DX_ParkingDuration(FxBase):

    def __init__(self, name='ParkingDuration'):
        super().__init__(name=name)

    def extract(self, payload: dict) -> dict:
        pass


if __name__ == '__main__':
    pass
