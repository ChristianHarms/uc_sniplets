#include <unistd.h>
#include <stdio.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>

#define MAX_BIT_VEC 100000000
#define BIT_VEC_PAGE_SIZE 12500992

void rmdup(char* file) 
{
    int fd = open(file, O_RDONLY);
    struct stat buffer;
    fstat(fd, &buffer);    
    size_t length = buffer.st_size;
    
    char* min = mmap(NULL, length, PROT_READ, MAP_SHARED/*MAP_PRIVATE*/, fd, 0);
    char* in = min;
    char* end = in + length;
    int num = 0;
    unsigned char* bitvec = mmap(NULL, BIT_VEC_PAGE_SIZE, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    for (;in < end; ++in)
    {
        if (*in == '\n') 
        {
            int bvadr = (num / 8);
            unsigned char bvb = 1 << (num % 8);
            if ((bitvec[bvadr] & bvb) == 0) 
            {
                bitvec[bvadr] |= bvb;
                //printf("%d\n", num);
            }
            num = 0;
        }
        else
        {
            num *= 10;
            num += (*in - '0');
        }
    }
    munmap(bitvec, BIT_VEC_PAGE_SIZE);
    munmap(min, length);
}

int main(int argc, char** argv) 
{
    rmdup(argv[1]);
}

