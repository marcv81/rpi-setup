# Benchmarks

## xHPL

Install dependencies.

    sudo apt install build-essential libopenmpi-dev libopenblas-dev

Download and build xHPL.

    wget http://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz
    tar xvf hpl-2.3.tar.gz
    cd hpl-2.3/
    ./configure
    make -j4

Copy `~/hpl-2.3/HPL.dat from the files directory. It was generated at https://www.advancedclustering.com/act_kb/tune-hpl-dat-file/.

Run xHPL.

    ./testing/xhpl

## Storage

Sequential read.

    sudo hdparm -t /dev/sda

Random 4K I/O.

    sudo apt install iozone3
    iozone -e -I -r 4K -s 100M -i 0 -i 1 -i 2

# Stress tests

## stress-ng

    sudo apt install stress-ng
    stress-ng --cpu 0 --cpu-method fft
