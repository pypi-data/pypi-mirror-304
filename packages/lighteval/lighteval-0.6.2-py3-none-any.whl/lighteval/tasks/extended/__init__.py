# MIT License

# Copyright (c) 2024 The HuggingFace Team

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from lighteval.utils.imports import can_load_extended_tasks


if can_load_extended_tasks():
    import lighteval.tasks.extended.ifeval.main as ifeval
    import lighteval.tasks.extended.mix_eval.main as mix_eval
    import lighteval.tasks.extended.mt_bench.main as mt_bench
    import lighteval.tasks.extended.tiny_benchmarks.main as tiny_benchmarks

    AVAILABLE_EXTENDED_TASKS_MODULES = [ifeval, tiny_benchmarks, mt_bench, mix_eval]

else:
    AVAILABLE_EXTENDED_TASKS_MODULES = []
