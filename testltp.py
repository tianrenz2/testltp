import subprocess
import re

import os

# Path to the testcase file
testcase_file = "testcase"

base_dir = "/home/projects/qemu-tcg-kvm/build"

# Path to the qemu executable (adjust this if needed)
qemu_path = "{}/qemu-system-x86_64".format(base_dir)  # Replace with the actual path to your qemu executable
log_file = "{}/rec.log".format(base_dir)
run_log = "./LOG"

base_record_cmdline = """
{qemu_bin} -smp 1 -kernel /home/projects/linux-6.1.0/arch/x86/boot/bzImage \
-accel kvm -cpu host -m 2G -no-hpet \
-append  "root=/dev/sda rw init=/lib/systemd/systemd tsc=reliable console=ttyS0 mce=off test={test}" \
-hda /home/projects/kernel-utils/rootfs.img \
-object memory-backend-file,size=4096M,share,mem-path=/dev/shm/ivshmem,id=hostmem \
-device ivshmem-plain,memdev=hostmem -vnc :00 -D {log} -exit-record 1
"""

base_replay_cmdline = """
{qemu_bin} -accel tcg -smp 1 -cpu Broadwell -no-hpet -m 2G -kernel /home/projects/linux-6.1.0/arch/x86/boot/bzImage \
-append "root=/dev/sda rw init=/lib/systemd/systemd tsc=reliable console=ttyS0 mce=off test={test}" \
-hda /home/projects/kernel-utils/rootfs.img -device ivshmem-plain,memdev=hostmem \
-object memory-backend-file,size=4096M,share,mem-path=/dev/shm/ivshmem,id=hostmem \
-vnc :0 -monitor stdio -kernel-replay test1 -singlestep -D {log}
"""

class TimeoutException(Exception):
    pass

start_point = 16

def get_test_list() -> list:
    tests = []
    # Read the file and iterate through each line
    with open(testcase_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # Remove any trailing newline or whitespace

            if line:  # Only proceed if the line is not empty
                tests.append(line)

    return tests

def reload_rr():
    os.system("cd /home/projects/kernel-rr-linux/;sh replace.sh")


def run_program(cmdline, ignore_ret=True):
    try:
        process = subprocess.run(cmdline, shell=True, check=True, timeout=60)
    except subprocess.TimeoutExpired as e:
        raise TimeoutException("TIMEOUT")
    except subprocess.CalledProcessError as e:
        if not ignore_ret:
            if e.returncode != 0:  # Check the return code
                raise Exception(f"Error: Test '{cmdline}' failed with return code {e.returncode}")


def analyze_summary(log_file, output_file, test_name):
    # Initialize variables for storing counts
    passed_count = 0
    failed_count = 0
    broken_count = 0
    skipped_count = 0
    warnings_count = 0

    # Patterns to match each summary line
    patterns = {
        'passed': re.compile(r"passed\s+(\d+)"),
        'failed': re.compile(r"failed\s+(\d+)"),
        'broken': re.compile(r"broken\s+(\d+)"),
        'skipped': re.compile(r"skipped\s+(\d+)"),
        'warnings': re.compile(r"warnings\s+(\d+)")
    }

    # Read the log file and find the summary section
    with open(log_file, 'r') as file:
        for line in file.readlines():
            # Check and extract the numbers using the patterns
            if patterns['passed'].search(line):
                passed_count = int(patterns['passed'].search(line).group(1))
            elif patterns['failed'].search(line):
                failed_count = int(patterns['failed'].search(line).group(1))
            elif patterns['broken'].search(line):
                broken_count = int(patterns['broken'].search(line).group(1))
            elif patterns['skipped'].search(line):
                skipped_count = int(patterns['skipped'].search(line).group(1))
            elif patterns['warnings'].search(line):
                warnings_count = int(patterns['warnings'].search(line).group(1))

    # Write the result in one line to the output file
    result = (f"{test_name},passed={passed_count},failed={failed_count},"
              f"broken={broken_count},skipped={skipped_count},warnings={warnings_count}\n")

    with open(output_file, 'a+') as out_file:
        out_file.write(result)

    return

def LOG(msg):
    with open(run_log, "a+") as f:
        f.write("{}\n".format(msg))

def run_all_tests():
    tests = get_test_list()

    # tests = tests
    index = 0
    retry = 0

    while index < len(tests):
        if index < start_point:
            index += 1
            continue

        test = tests[index]
        test_dir = "/opt/ltp/testcases/bin/{}".format(test)
        LOG("index={}, test={}".format(index, test))

        record = base_record_cmdline.format(qemu_bin=qemu_path, test=test_dir, log=log_file)
        try:
            run_program(record)
        except TimeoutException as e:
            LOG("Test[{}] timeout".format(test))
            reload_rr()
            index += 1
            continue

        analyze_summary("./rr-result.txt", "./ltp-result", test)

        replay = base_replay_cmdline.format(qemu_bin=qemu_path, test=test_dir, log=log_file)
        try:
            run_program(replay, ignore_ret=False)
        except Exception as e:
            print("Failed to replay {}".format(test))
            if retry < 2:
                LOG("Failed test[{}]: {}, retry={}".format(test, str(e), retry))
                retry += 1
                continue
            else:
                LOG("Give up test {}".format(test))
        else:
            LOG("{} replay passed".format(test))

        index += 1
        retry = 0

reload_rr()
run_all_tests()
