# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
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
"""以下代码可以检测TensorFlow是否被正确安装到Windows中。
代码将会校验你的TensorFlow安装状态，并且给出修复建议。
--深黑团队祝你玩得愉快
"""

import ctypes
import imp
import sys

def main():
  try:
    import tensorflow as tf
    print("TensorFlow 已成功安装")
    if tf.test.is_built_with_cuda():
      print("已安装的 TensorFlow 版本支持 GPU")
    else:
      print("已安装的 TensorFlow 版本不支持 GPU")
    sys.exit(0)
  except ImportError:
    print("错误：载入 TensorFlow 模块失败")

  candidate_explanation = False

  python_version = sys.version_info.major, sys.version_info.minor
  print("\n- 已安装的 Python 版本是 %d.%d." % python_version)
  if not (python_version == (3, 5) or python_version == (3, 6)):
    candidate_explanation = True
    print("- Windows 版 TensorFlow 的安装官方需求是"
          "Python 版本 3.5 或 3.6")
  
  try:
    _, pathname, _ = imp.find_module("tensorflow")
    print("\n- TensorFlow 的安装路径是 %s" % pathname)
  except ImportError:
    candidate_explanation = False
    print("""
- 在此Python环境中没有安装名为 TensorFlow 的模块，您可以使用如下命令安装它
   `pip install tensorflow`""")

  try:
    msvcp140 = ctypes.WinDLL("msvcp140.dll")
  except OSError:
    candidate_explanation = True
    print("""
- 无法载入 'msvcp140.dll'。 TensorFlow 需要此.DLL文件被安装在 %PATH% 这个环境变量定义的路径下。
  想安装此.DLL文件，可以从以下URL下载并安装 Microsoft Visual C++ 2015 Redistributable Update 3
  https://www.microsoft.com/en-us/download/details.aspx?id=53587""")

  try:
    cudart64_80 = ctypes.WinDLL("cudart64_80.dll")
  except OSError:
    candidate_explanation = True
    print("""
- 无法载入 'cudart64_80.dll'。GPU版本的 TensorFlow 需要此.DLL文件被安装在 %PATH% 这个环境变量定义的路径下。
  想安装此DLL文件，可以从以下URL下载并安装CUDA 8.0:
  https://developer.nvidia.com/cuda-toolkit""")

  try:
    nvcuda = ctypes.WinDLL("nvcuda.dll")
  except OSError:
    candidate_explanation = True
    print("""
- 无法载入 'nvcuda.dll'。 GPU版本的 TensorFlow 需要此.DLL文件被安装在 %PATH% 这个环境变量定义的路径下。
  通常它被安装在 'C:\Windows\System32'。
  如果没有，请确认你的GPU支持CUDA，并且已经正确安装驱动程序。""")

  cudnn5_found = False
  try:
    cudnn5 = ctypes.WinDLL("cudnn64_5.dll")
    cudnn5_found = True
  except OSError:
    candidate_explanation = True
    print("""
- 无法载入 'cudnn64_5.dll'。 GPU版本的 TensorFlow 需要此.DLL文件被安装在 %PATH% 这个环境变量定义的路径下。
  请注意cuDNN不会随同CUDA一起安装，而是需要单独安装。而且cuDNN的.DLL文件也不在CUDA文件夹中。
  想安装此.DLL文件，可以从以下URL下载并安装cuDNN 5.1:
  https://developer.nvidia.com/cudnn""")

  cudnn6_found = False
  try:
    cudnn = ctypes.WinDLL("cudnn64_6.dll")
    cudnn6_found = True
  except OSError:
    candidate_explanation = True

  if not cudnn5_found or not cudnn6_found:
    print()
    if not cudnn5_found and not cudnn6_found:
      print("- 找不到 cuDNN")
    elif not cudnn5_found:
      print("- 找不到 cuDNN 5.1")
    else:
      print("- 找不到 cuDNN 6")
      print("""
  GPU版本的 TensorFlow 需要 cuDNN 的.DLL文件被正确安装在 %PATH% 这个环境变量定义的路径下。
  请注意 cuDNN 不会随同 CUDA 一起安装，而是需要单独安装。而且 cuDNN 的.DLL文件也不在 CUDA 文件夹中。
  请为你的 TensorFlow 选择对应版本的 cuDNN：
  
  * TensorFlow 1.2.1 或更早版本需要 cuDNN 5.1 ('cudnn64_5.dll')
  * TensorFlow 1.3 或更新版本需要 cuDNN 6 ('cudnn64_6.dll')
    
  想安装此.DLL文件，可以从以下URL下载并安装 cuDNN：
  https://developer.nvidia.com/cudnn""")
    
  if not candidate_explanation:
    print("""
- 所有必需的.DLL文件似乎都齐备了。你仍可以进入 TensorFlow 官方 GitHub 提出你的问题：
  https://github.com/tensorflow/tensorflow/issues""")

  sys.exit(-1)

if __name__ == "__main__":
  main()