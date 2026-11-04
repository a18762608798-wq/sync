# broadcasting operators

```{julia}
matrix1 = [1 2];
matrix2 = [[1 2], [3 4]];
matrix3 = [[5 6], [7 8]];
vec1 = [1, 2];

matrix1 .+ 1
matrix2 .+ matrix3
3vec1
3 .* vec1 # it is equal to 3vec1
vec1.^2
# matrix2 .^ matrix3 is wrong
```
