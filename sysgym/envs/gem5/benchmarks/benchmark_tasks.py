from typing import Dict

from sysgym.utils.enum import BenchmarkTask


class SmaugTask(BenchmarkTask):
    MINERVA = "minerva"
    LSTM = "lstm"
    # other models: https://github.com/yaoyuannnn/experiments/tree/master/models
    LENET5 = "lenet5"
    CNN_CIFAR10 = "cifar10-cnn"
    VGG_CIFAR10 = "cifar10-vgg"
    ELU_CIFAR100 = "cifar100-elu"
    ELU_LARGE_CIFAR100 = "cifar100-large-elu"
    RESNET = "imagenet-resnet"


class MachSuiteTask(BenchmarkTask):
    #  BOA uses: FFT_TRANSPOSE< STENCIL_STENCIL3D,
    # Benchmarks explained in
    # http://vlsiarch.eecs.harvard.edu/wp-content/uploads/2016/08/shao_micro2016.pdf
    # https://breagen.github.io/MachSuite/
    AES = "aes_aes"  # very fast env
    NW = "nw_nw"
    GEMMA_NCUBED = "gemm_ncubed"
    GEMMA_BLOCKED = "gemm_blocked"  # used in paper
    STENCIL_2D = "stencil_stencil2d"  # used in paper
    STENCIL_3D = "stencil_stencil3d"  # used in paper
    MD_KNN = "md_knn"
    MD_GRID = "md_grid"
    FFT_TRANSPOSE = "fft_transpose"  # used in paper
    FFT_STRIDED = "fft_strided"  # used in paper
    BFS = "bfs_bulk"
    KMP = "kmp_kmp"
    SORT_MERGE = "sort_merge"
    SORT_RADIX = "sort_radix"
    SPMV_CRS = "spmv_crs"  # used in paper
    SPMV_ELLPACK = "spmv_ellpack"  # used in paper
    VITERBI = "viterbi_viterbi"


# Map between the task and its maximum running time (sometime the task will freeze)
TASK_TO_TIMEOUT_SECONDS: Dict[BenchmarkTask, int] = {
    # The maximum is set to x5 the average execution time
    # For now it doesn't make sense to make this configurable
    # but can easily be overriden
    MachSuiteTask.AES: 60,
    MachSuiteTask.FFT_TRANSPOSE: 250,
    MachSuiteTask.MD_KNN: 250,
    MachSuiteTask.SPMV_CRS: 250,
    MachSuiteTask.SPMV_ELLPACK: 400,
    MachSuiteTask.FFT_STRIDED: 500,
    MachSuiteTask.STENCIL_2D: 910,
    MachSuiteTask.STENCIL_3D: 1500,
    MachSuiteTask.GEMMA_NCUBED: 2500,
}
