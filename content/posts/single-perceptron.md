+++
title = "Classification with a single Perceptron"
date = "2026-01-04T15:28:02+01:00"
#dateFormat = "2006-01-02" # This value can be configured for per-post date formatting
author = ""
authorTwitter = "" #do not include @
cover = ""
tags = ["rust", "ml"]
keywords = ["", ""]
description = ""
showFullContent = false
readingTime = false
hideComments = false
+++

# Introduction

It's been quite some time since I last made a post regarding anything, but I've been given another machine-learning assignment.
It's also about data classification this time, like the last post where I described the implementation of the k-means algorithm
in Rust.

The assignment in this case was to build a single perceptron capable of learning any "learnable" dataset. Before I begin with the 
implementation, it'd probably be better to explain what a perceptron is, what it does, and what it can classify. If you're already 
familiar and interested nonetheless, I suggest you skip to [](#)

## Definitions

### Perceptron 

You can think of a perceptron as an artificial neuron, which fires or not depending on its inputs. The perceptron is capable of
learning a linearily separable boolean function, i.e., one which returns `1` or `0`. For example, it could decide whether or not
an object is a "rectangle" or a "circle", depending on its attributes (corner radius, side lengths, ...). It could decide whether or
not some flower, based upon its measurements, is a certain type of flower. It does however, have a limitation: it can only learn
functions which are "linearily separable". One very famous and very simple function the perceptron cannot learn is the XOR logic
gate.

The XOR logic gate is defined as:
|Input A |Input B |Output |
|--------|--------|-------|
|0       |0       |0      |
|1       |0       |1      |
|0       |1       |1      |
|1       |1       |0      |

We can nicely plot this:
![XOR logic gate plot](/img/single-perceptron-boolean-function-0.png)
Red represents `0`, or `false`.
Green represents `1`, or `true`.
The coordinates of each point are the input values.

What a perceptron would try to do now is find a linear function which separates the "true" values from the "false" values. 
This is impossible here, since the function would have to be on the values.

So, how does a perceptron actually work? 

A perceptron is comprised of a vector of weights `w` and a bias `b`, which are combined to form the following function:

w ϵ R<sup>n</sup> \
p: x ϵ R<sup>n</sup> -> w * x + b 

If the value of p is then greater than `0`, the perceptron returns `1`, or `true`, otherwise, it returns `0` or `false`.

# Implementation 
I've decided to implement this in Rust since I've been working quite a bit in it in the past few weeks.

First, let's model a perceptron:
```rust
use ndarray::Array1;

#[derive(Debug)]
struct Perceptron {
    weights: Array1<f64>,
    bias: f64
}
```

We can simplify this, however. If we think back to the activation function of a perceptron:

> `p(x) = w * x + b`

We can include the bias in the weights vector since the dot product of two vectors is defined as:

<code>
w * x = sum(i=1..n, w<sub>i</sub>x<sub>i</sub>)
</code>

And therefore we can include the bias as the first element of the weight vector 
and add `1` as the first of element of the input vector.

So, revised, with an activation function:
```rust
use ndarray::Array1;

#[derive(Debug)]
struct Perceptron {
    weights: Array1<f64>
}

impl Perceptron {
    const fn new(weights: Array1<f64>) -> Self {
        Self { weights }
    }

    fn eval(&self, x: &Array1<f64>) -> f64 {
        self.weights.dot(x)
    }
}
```

This is great! We have a model perceptron, but it's not much use like this. 
You'll rarely ever have an adjusted perceptron, rather it's going to learn from a dataset.

So how does a perceptron learn?

The best way to show this is probably to use an example, in this case a perceptron learning 
the AND gate. 

Let's start with an empty weights vector: 
```rust
w = {0, 0, 0}
```
The weights vector has a length of `3` because we have 
- the bias
- the weights for each input (in this case two)

So given our training data, which in this case is quite sparse since the `AND` gate 
has only four possible combinations, the algorithm will go iterate through the samples
until it can predict every sample correctly. 

Iteration `1`:

`(0, 0)`:
```rust 
w' = {0, 0, 0}
x' = {0, 0, 0}

w' * x' = 0 (correct)
```

`(0, 1)` & `(1, 0)`:
```rust
w' = {0, 0, 0}
x' = {0, 0, 1} // or {0, 1, 0}

w' * x' = 0 (correct)
```

`(1, 1)`:
```rust
w' = {0, 0, 0}
x' = {0, 1, 1}

w' * x' = 0 (incorrect)
```

Okay... our perceptron has mispredicted the output for `(1, 1)`, so we obviously have to change something.

The fix is quite simple, and a bit naive: we rotate the weights vector point towards the misclassified sample.

<pre><code>w<sub>new</sub> = w + y<sub>i</sub>x<sub>i</sub></code></pre>

This would make the algorithm run wild, so let's add a learning rate `l`.

<pre><code>w<sub>new</sub> = w + l * y<sub>i</sub>x<sub>i</sub></code></pre>

There's a good chance however, that even the perceptron will encounter a dataset that might not be perfectly linearly seperable.
The algorithm will continue forever, since it only interrupts when it can perfectly predict 
every sample from the training dataset. This can be easily fixed by adding either a constant limit
or a dynamically computed limit which is based on the dataset for the number of times 
the algorithm can iterator. The dynamically computed one could be, for example,
half of the amount of samples.

We can now finally implement our PLA (Perceptron Learning Algorithm) for our model perceptron.

```rust 
struct Sample {
    x: Array1<f64>,
    // this could also be a bool, but an f64 is used for simplicity purposes.
    y: f64
}

// -- snip
impl Perceptron {
    // -- snip 
    fn learn(d: &[Sample], learning_rate: f64, max_iters: usize) -> Self {
        let dim = d.data[0].x.len();
        // a default vector of weights (all zeros).
        let mut perceptron = Self::new(Array1::zeros(dim));
        
        for _ in 0..max_iters {
            let mut any_fail = false;
        
            for sample in d {
                // check if the perceptron mispredicted
                // multiply by s.y because a negative sample would otherwise
                // need the opposite check (>= 0) 
                if s.y * p.eval(&s.x) <= 0 {
                    any_fail = true;
                    perceptron.weights = perceptron.weights + 
                                        (lr * sample.y * &sample.x);
                }
            }
        
            // perfect predictions
            if !any_fail {
                break;
            }
        }
    
        perceptron
    }
}
```

That's pretty much it. This is not a perfect algorithm, in fact, it's the worst.

It's also however the simplest. You may for example, find a case where the perceptron performs better,
but because it wasn't perfect and wasn't the last iteration, it went to the next and worsened.
You could record the performance and pick out the best instead.

I hope this post was useful to any readers. If you have any feedback suggestions, feel free to reach out to me.

Happy New Year!