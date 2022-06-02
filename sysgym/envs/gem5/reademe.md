
# Installation
```bash
docker pull xyzsam/gem5-aladdin

Run it:
docker run -it --rm --mount source=gem5-aladdin-workspace,target=/workspace xyzsam/gem5-aladdin

cd gem5-aladdin && git pull origin master && git submodule update --init --recursive && cd ..
cd LLVM-Tracer && git pull origin master && cd ..


cd /workspace/gem5-aladdin
python2.7 `which scons` build/X86/gem5.opt PROTOCOL=MESI_Two_Level_aladdin -j2
```
## Smaug

Pull the image and execute it
```bash
docker run -it --rm --mount source=smaug-workspace,target=/workspace xyzsam/smaug:latest
```

Update the image

```bash
cd gem5-aladdin && git pull origin master && git submodule update --init --recursive && cd ..
cd LLVM-Tracer && git pull origin master && cd ..
cd smaug && git pull origin master && git submodule update --init --recursive && cd ..
```

Build gem5-aladdin 
```bash
python2.7 `which scons` build/X86/gem5.opt PROTOCOL=MESI_Two_Level_aladdin -j2
```

First, we need to build the SMAUG tracer, which is an instrumented binary that will be executed to generate the dynamic trace.

```bash
make tracer -j4

```
