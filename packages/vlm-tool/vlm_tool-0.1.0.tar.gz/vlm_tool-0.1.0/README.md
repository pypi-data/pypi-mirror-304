python call for C/C++

vlm_utils is a library for tracing function calls with depth control and filtering.

# Installation
    pip install vlm_utils
    
# Usage 1

    from vlm_utils.module import tracer

    def add_one(n):
        return n+1
    
    def add_two(n):
        n = add_one(n)
        n = add_one(n)
        return n

    @tracer
    def main():
        n = add_two(4)

    main()
    
# Usage 2
    
    to use c++ lib function
        
    from vlm_utils import lib_tools

# Install Requires

    python>=3.6.0



    