Name: Jiatong Li 
UNI: jl6565



1. One-hot encoding is a technique used to represent categorical data, such as class labels or categories, in a numerical format that can be easily processed by machine learning algorithms. It is important because many machine learning models, including neural networks, require input data to be in numerical form. For example, if we have input labels ["tree", "cat", "dog"] and the ground truth is "cat", then we can encode the input to [0, 1, 0]. One-hot encoding is particularly useful when dealing with categorical variables that do not have a natural ordinal relationship between their categories.
2. During training, for each mini-batch of data, dropout randomly deactivates (or "drops out") a fraction of neurons in the neural network. The fraction of neurons to drop out is a hyperparameter typically set between 0.2 and 0.5, but it can vary depending on the specific problem. The key idea behind dropout is that it forces the neural network to be more robust and prevents it from relying too heavily on any specific set of neurons.
3. For sigmoid, It outputs values between 0 and 1, mapping any real-valued number to a value within this range. This property makes it suitable for binary classification problems where you need a probability-like output. For RELU, It outputs 0 for any negative input and passes through any positive input unchanged. 
4. Since we are essentially predicting the probability of each label. This is different from regression problem since we are not trying to predict a numerical score.
5. 
we can use the following formulas:

For the convolution layer:

    Output width = (Input width - Kernel width + 2 * Padding) / Stride + 1
    Output height = (Input height - Kernel height + 2 * Padding) / Stride + 1

For the max-pooling layer:

    Output width = Input width / Pool size
    Output height = Input height / Pool size

Convolution Layer:

    Input width = 100
    Input height = 100
    Number of filters = 16
    Kernel size = (5,5)
    Stride (typically 1, unless specified otherwise) = 1
    Padding (typically 0, unless specified otherwise) = 0

Output width = (100 - 5 + 2 * 0) / 1 + 1 = 96
Output height = (100 - 5 + 2 * 0) / 1 + 1 = 96

So, the output dimensions of the convolution layer are 96x96x16, where 16 is the number of filters.

MaxPooling Layer:

    Input width = 96 (output width of the previous layer)
    Input height = 96 (output height of the previous layer)
    Pool size = (2,2)

Output width = 96 / 2 = 48
Output height = 96 / 2 = 48




Architecture choice:
The implementation is kind of intuitive. I sandwich convolution layer and max pool layer alternatively. 
I treat the collection of these two as the foundemental building block. We know that the y label has 25 unique value so 
we must set the last softmax layer to 25 units. After doing a bit research, I decided to add dropout layer in the middle to prevent 
overfitting. The result turns to be pretty good and I successfully achieve 90+ accuracy. 