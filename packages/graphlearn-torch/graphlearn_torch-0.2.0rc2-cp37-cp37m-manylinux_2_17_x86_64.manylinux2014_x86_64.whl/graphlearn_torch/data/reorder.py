# Copyright 2022 Alibaba Group Holding Limited. All Rights Reserved.
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
# ==============================================================================

import torch


def sort_by_in_degree(cpu_tensor, shuffle_ratio, csr_topo):
  if csr_topo is None:
    return cpu_tensor, None
  row_count = csr_topo.row_count
  new_idx = torch.arange(row_count, dtype=torch.long)
  perm_range = torch.randperm(int(row_count * shuffle_ratio))
  _, old_idx = torch.sort(csr_topo.degrees, descending=True)
  old2new = torch.zeros_like(old_idx)
  old_idx[:int(row_count * shuffle_ratio)] = old_idx[perm_range]
  cpu_tensor = cpu_tensor[old_idx]
  old2new[old_idx] = new_idx
  return cpu_tensor, old2new
