# CPU settings
core = 'A15'  # Choose 'A15' (big) or 'A7' (LITTLE) took A7 instead of A15
frequency = 1500 # CPU clock frequency [MHz] changed from 1500


# L1 data cache settings
l1d_size = 32 * 1024  # Size (in bytes)
l1d_assoc = 2  # Associativity
l1d_memory_type = "hp"  # Memory cell type ("lop", "lstp" or "hp")


# L1 instruction cache settings
l1i_size = 32 * 1024  # Size (in bytes)
l1i_assoc = 16  # Associativity
l1i_memory_type = "hp"  # Memory cell type ("lop", "lstp" or "hp")


# L2 cache settings
l2_enable = True  # Enable cache? (true/false)
l2_prefetch = False  # Enable prefetching from system memory? (true/false)
l2_size = 2 * 1024 * 1024  # Size (in bytes) changed from 2
l2_assoc = 16  # Associativity
l2_memory_type = "hp"  # Memory cell type ("lop", "lstp" or "hp")


# Advanced settings below (you don't have to change these for the assignment)

# Write statistics to 'stats.txt' every 'log_interval' seconds.
# Increase me if the stats.txt file becomes too large to handle.
log_interval = 1e-3

# Number of CPU cores. Change me if you want to play around with
# GEM5 multicore. Note, however, that applications must be
# single-threaded and are always bound to a single core in syscall
# emulation mode! So you can only use this to run multiple non-interacting
# applications at the same time.
num_cores = 1
