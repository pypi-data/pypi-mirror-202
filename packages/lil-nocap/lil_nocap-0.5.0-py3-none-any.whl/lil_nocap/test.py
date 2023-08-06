#!/usr/bin/env 
import pandas as pd
import numpy as np
import dask
from dask.distributed import Client, progress
import multiprocessing as mp
import time
import timeit
import os
import click

client = Client(threads_per_worker=4, n_workers=mp.cpu_count())
def t(i):
  return "test"

for i in range(4):
  print(f'{t(i)}\n')

