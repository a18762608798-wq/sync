# MATLAB Foundation

## Special

### Explanation

```matlab
%This a explanation
%% Noice there is a blank
%{ 
I will explain multiple rows.
%}
```

### Interval range

```matlab
%Casse:
randi([1,2],2,3); %[1,2] cover the start and end, meaning 1 and 3.
```



## Desktop

### Command function

```matlab
clear %clear memory
clear all %clear all the variables
clc %clear all the display in desktop
```

### Format

```matlab
format compact %Compact the distance of rows
```

## Operator

### relational operator

```matlab
>=,<=
~= %unequal
```

### logic operator

```matlab
& && %and, doubt operators reflect a super spid speed
| || %or
~ %not
xor(a,b) %One true and one false. 
```

## Data format 

### Matrix

#### Input

* Direct input

```matlab
A=[1,2;3,4];
B=[];
C=[NaN,Inf;1,2];
```

* Instruction generation

```matlab
%Row
linspace(2,3,10); %General 10 equidistant numbers between 2 and 3(include 2 and 3)
logspace(2,3,3); %General:10^2,10^2.5,10^3;

%Matrix
zeros(2,3);
ones(2,3);
eye(5); %unit matrix
rand(2,3); %random range0-1, consist a matrix 2 * 3
1+(2-1)*rand(2,3); %random range1-2
randi([1,10],2,3); % random integers, range:1-10, consist a matrix format: 2*3
randn(2,3); %Nomal random range:[-Inf,Inf]

magic(3); 
%     8     1     6
%     3     5     7
%     4     9     2
diag([1,2,3;4,5,6;7,8,9]) %Input:square matrix,Output:A column vector consisting of diagonal elements
ans =
     1
     5
     9
```

#### Index

```matlab
A(4); %the 4th element in One dimensional column consisting of matrix A.
A(1,2);
A(1,:); %Row 1
A(1,2:end); %Row 1,element 2-end
```

#### Transform

```matlab
A=[1,2;3,4]; A(3,3)=1; %If you add a element out of a matrix, martix will extent its format.
A =
     1     2     0
     3     4     0
     0     0     1
     
A(:,1)=[]; %delete column 1
A =
     2     0
     4     0
     0     1
     
C=[[1,2;3,4],[5,6;7,8]]; B=[[1,2;3,4];[5,6;7,8]]; %The combination of matrix.

repmat(A,[1,2]); %regard A as a element, arrange accord format:1*2
ans =
     2     0     2     0
     4     0     4     0
     0     1     0     1

% Note: A even can be a multi-way Matrix
reshape(A,[1,6]); %reshape the format of a matrix: 1*6
reshape(A,[],6); %reshape the format of a matrix: column 6
ans =
     2     4     0     0     0     1

flipud(A); fliplr(A); rot90(A); %Filp upside down; Flip side to side; Rotate 90 degrees
flipdim(A,2); %Filp the elements of any rows to keep them away from they primary position. Meaning flip columns.
```

#### Arithmetic Operation

##### Instruction

```matlab
sin(A); 

max(A,[],2); %The maximum of every row
max(A,[],'all')
max(A,[],2,'omitnan') %ingore NaN
[maximum,sequence]=max(A,[],2,'omitnan'); %Get the sequences of maximum in every volumn.'all' can not be used.
[minimum,sequence]=min(A,[],1) %The minimum of every column

sum(A,'all'); %summation of all the elements.
sum(A,1,'omitnan') %ingore NaN
prod(A,2,'omitnan'); %Product of every column
mean(A,2,'omitnan') %even of every column,ignore NaN
median(A,1,'omitnan') %mediant of every column, ingore NaN
cumsum(A,2,'omitnan'); %Cumulative sum, ignore NaN.
cumprod(A,2,'omitnan'); %Cumulative product, ignore NaN.

std(A,[],1,'omitnan'); %standard deviation
std(A,[],'all');
%[] is the weight, default w=0

B = sort(A,2,)
B = sort(A,2,'descend')% sort to every row,Sequence: descend

inv(A); %inverse of matrix
trace(A); %Trace of matrix
rank(A); %Rank of matrix
det(A); %det
eig(A); %eigenvalue
```

* Standard deviation 

$$
S=\sqrt{\frac{1}{N-1}\sum_{i=1}^n\abs{A_i-\mu}^2}\\
Therein:\mu=\frac{1}{N}\sum_{a=1}^nA_i, w=0
$$

##### Operation between Matrix

|                  | inverse               | addition/subtraction | product | rightdivision | left division | power |
| ---------------- | --------------------- | -------------------- | ------- | ------------- | ------------- | ----- |
|                  | $(A^T)^*$(+conjugate) | $A+B$                | $A*B=C$ | $A=C*B^{-1}$  | $B=A^{-1}*C$  | $A^n$ |
| Matrix operation | A'                    | + \| -               | *       | /             | \             | ^     |
| Array operation  | A.'                   | + \| -               | .*      | ./            | .\            | .^    |

### Array

#### Input

* Direct input

```matlab
A(:,:,1)=[1,2;3,4]; %from dimension 3, Input matrixs.
A(:,:,2)=[5,6;7,8];
A(:,:,1) =
     1     2
     3     4
A(:,:,2) =
     5     6
     7     8
```

* Instruction generation

​	Partial instruction of matrix can be used. 

```matlab
zeros(2,3,4);
ones(2,3,4);
rand(2,3,4); %random range0-1
randn(2,3,4); %Nomal random range:[-Inf,Inf]
```

#### Index

​	Likewise, Partial index of matrix can be used. 

```matlab
A(4); %the 4th element in One dimensional column consisting of matrix A.
ans
	=4
%Because the (3 dimansion to 2 dimension)consisting of the two matrix is along rows.
A(1,2);
A(1,:); %Row 1
A(1,2:end); %Row 1,element 2-end
```

<!--NOTE: consisting of the one dimensional column follows this rules: from the lowest dimension to top dimension. Meaning the process of 3 dimension to 2 dimension is along rows, so A(4)==4 -->

#### Transform

​	Likewise, **All transform of matrix can be used**. 

### Date Network

* Use to plot picture of function. 

```matlab
%Case:
x=[1,2];
y=[2,3];
[X,Y]=meshgrid(x,y); %meaning ther are four points on the plane:(1,2)&&(2,2)&&(1,3)&&(2,3)
X =
     1     2
     1     2
Y =
     2     2
     3     3
```

