#! /bin/bash


cast=tool-test.cast
master_dir=test-master-casts
tmp_dir=test-tmp-casts

# Print Deltas Test
grep -q $( ./asciinema-tool.py --print ${cast} | sha256sum | cut -d ' ' -f 1 ) ${master_dir}/master.sha256 \
    && echo "Delta Passed" \
    || echo "Delta Failed"



# Add delay frame
grep -q $( ./asciinema-tool.py --add-delay 10 30 --frame ${cast} | sha256sum | cut -d ' ' -f 1 ) ${master_dir}/master.sha256 \
    && echo "Delay Frame Passed" \
    || echo "Delay Frame Failed"



# Add delay timestamp
grep -q $( ./asciinema-tool.py --add-delay 10 8 ${cast} | sha256sum | cut -d ' ' -f 1 ) ${master_dir}/master.sha256 \
    && echo "Delay Timestamp Passed" \
    || echo "Delay Timestamp Failed"

# Change delta frame fuzzy
grep -q $( ./asciinema-tool.py --change .2 30 40 --frame ${cast} | sha256sum | cut -d ' ' -f 1 ) ${master_dir}/master.sha256 \
    && echo "Change Delta Frame Passed" \
    || echo "Change Delta Frame Failed"

# Change delta frame nofuzzy
grep -q $( ./asciinema-tool.py --change .2 30 40 --frame --nofuzzy ${cast} | sha256sum | cut -d ' ' -f 1 ) ${master_dir}/master.sha256 \
    && echo "Change Delta Frame NoFuzzy Passed" \
    || echo "Change Delta Frame NoFuzzy Failed"

# Change delta timestamp fuzzy
grep -q $( ./asciinema-tool.py --change .2 8 12.7 ${cast} | sha256sum | cut -d ' ' -f 1 ) ${master_dir}/master.sha256 \
    && echo "Change Delta Timestamp Passed" \
    || echo "Change Delta Timestamp Failed"

# Change delta timestamp nofuzzy
grep -q $( ./asciinema-tool.py --change .2 8 12.7 --nofuzzy ${cast} | sha256sum | cut -d ' ' -f 1 ) ${master_dir}/master.sha256 \
    && echo "Change Delta Timestamp NoFuzzy Passed" \
    || echo "Change Delta Timestamp NoFuzzy Failed"

# Cut frame
grep -q $( ./asciinema-tool.py --cut 30 40 --frame ${cast} | sha256sum | cut -d ' ' -f 1 ) ${master_dir}/master.sha256 \
    && echo "Cut Frame Passed" \
    || echo "Cut Frame Failed"

# Cut timestamp
grep -q $( ./asciinema-tool.py --cut 8 12.7 ${cast} | sha256sum | cut -d ' ' -f 1 ) ${master_dir}/master.sha256 \
    && echo "Cut Timestamp Passed" \
    || echo "Cut Timestamp Failed"







