# Parameter `p` in Fingerprinting

The following two loops are the most important pieces of code for fingerprinting, and the parameter `p` is the key to controlling the time and effect of fingerprinting.

GPU fingerprinting code:

```c
float stall_function()
{
    float res = 0.01;
    for(int i = 1; i < GPU_P; i++)
    {
        res = sinh(res);
    }
    return res;
}     
```

CPU fingerprinting code:

```javascript
function stall_function_cpu(arg) {
    var array = new Uint32Array(arg);
    var start = performance.now();
    for (var k = 1; k <= CPU_P; k++) {
        crypto.getRandomValues(array);
    }
    var end = performance.now();
    return end - start;
}
```

## Settings of `p`

| Settings | `GPU_P` | `CPU_P` |
| :------  | :-----------: | :-----------: |
| Windows | `0xfffff` | `20000` |
| MacOS | `0xffff` | `5000` |
