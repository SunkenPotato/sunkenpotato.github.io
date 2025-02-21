+++
title = "K-Means (in Rust)"
date = "2024-11-17T09:45:49+01:00"
author = "SunkenPotato"
authorTwitter = "" #do not include @
cover = ""
tags = ["rust", ""]
keywords = ["", ""]
description = "Writing the K-Means algorithm in Rust"
showFullContent = false
readingTime = true
hideComments = false
+++
I got an assignment for this week: write the K-Means algorithm, in any language you like. \
So, first, we have to understand what it does and how it works.

## What is K-Means?
> k-means clustering is a method of vector quantization, originally from signal processing, that aims to partition n observations into k clusters in which each observation belongs to the cluster with the nearest mean (cluster centers or cluster centroid), serving as a prototype of the cluster. <sup>[1]</sup>

That, is copied directly from wikipedia, and the first time I read it, I had **no idea** what it was talking about. \
In short, it's an algorithm that you give a bunch of datapoints, and it attempts to cluster them into groups.

It follows these steps:
1. Choose `k` random points from the dataset as centers for the individual clusters (centroids).
2. Associate each point with its nearest centroid. The distance is calculated with [Euclidean Distance](https://en.wikipedia.org/wiki/Euclidean_Distance)
3. Every centroid gets updated to match the average point in their respective cluster.
4. Steps 2 & 3 are repeated until the centroids no longer update (convergence)

So, how do we implement it?
## Implementation

### Setting up the project
Create a new project, and add the following crates:
* `glam` (for `Vec2`s and other math operations)
* `index_vec` (I'll explain why later),
and
* `rand` (so we can choose points and generate a dataset)

Let's define a type alias and an index (for `index_vec`):
```rust
pub type Point = Vec2;

index_vec::define_index_type! {
    pub struct PointIdx = usize;
}
```
### Generating a dataset

First, we'll have to make a dataset. This is optional, but I had to since it was homework and there was no dataset provided. \
In python, you would do this with `scikit`'s `make_blobs` function, but we can achieve something similar.

We need to take the arguments:
* `clusters` (how many clusters to generate)
* `n_samp` (how many points to generate overall)
* `std` (the standard distribution, i.e., how scattered the points can be from their centroid)

Let's define defaults and the function:
```rust
const DEFAULT_CLUSTERS: usize = 4;
const DEFAULT_N_SAMP: usize = 100;
const DEFAULT_STD: f32 = 0.8;
...

pub fn generate_datapoints(
    clusters: Option<usize>,
    n_samp: Option<usize>,
    std: Option<f32>
) -> IndexVec<PointIdx, Point> {
    todo!()
}
```

How do we generate these? \
I decided to randomly generate one point and then use `std` as a radius around that point for all the other points in that cluster.
That way, we get a random looking cluster.

```rust
pub fn generate_datapoints(
    clusters: Option<usize>,
    n_samp: Option<usize>,
    std: Option<f32>
) -> IndexVec<PointIdx, Point> {
    let clusters = match clusters {
        Some(v) => v,
        None => DEFAULT_CLUSTERS
    };

    let n_samp = match n_samp {
        Some(v) => v,
        None => DEFAULT_N_SAMP
    };

    let std = match std {
        Some(v) => v,
        None => DEFAULT_STD
    };

    let mut centroids: IndexVec<PointIdx, Point> = index_vec![Point::default(), clusters];
    // IndexVec doesn't provide a fill_with method, so we have to use this
    for el in &mut centroids {
        *el = random_point();
    }

    let mut points = index_vec![];

    for ctr in centroids.iter() {
        for _ in 0..n_samp / clusters {
            let mut point = random_point();

            while point.distance(*ctr) > std {
                point = random_point();
            }

            points.push(point);
        }
    }

    points.append(&mut centroids); // optional, this way the amount of points is always n_samp + clusters.

    points
}
```
Here, we're generating the centroids and then an equal amount of points for each of them respectively. We're kind of guessing where to put the points.

The utility function, `random_point` is defined as:
```rust
use rand::thread_rng;
...

fn random_point() -> Point {
    let mut rng = thread_rng();
    let (x, y) = (rng.gen_range(0_f32..20_f32), rng.gen_range(0_f32..20_f32));

    Point::new(x, y)
}
```
It generates a random point in a 20x20 coordinate grid, you can change the size though.

### Pick some centroids
This part is pretty easy. All we do is pick some random points and return them: \
We also have to define a `CentroidIdx` struct though (more on that later).

We're taking the arguments:
* `dataset`: the dataset we generated before
* `k`: the amount of centroids to pick. This defaults, like that other function, to `DEFAULT_CLUSTERS`

```rust
index_vec::define_index_type! {
    pub struct CentroidIdx = usize;
}

pub fn pick_centroids(
    dataset: &IndexVec<PointIdx, Point>,
    k: Option<usize>
) -> IndexVec<CentroidIdx, Point> {
    let k = match k {
        Some(v) => v,
        None => DEFAULT_CLUSTERS,
    };

    let mut thread_rng = thread_rng();

    let mut centroid_vec = index_vec![];

    for _ in 0..k {
        let random_centroid = dataset.raw.choose(&mut thread_rng).expect("non empty list");
        centroid_vec.push(random_centroid.clone());
    }

    centroid_vec    
}
```

Alright, cool! We've finished steps 1 & 2.

The next part &mdash; associating the centroids with points &mdash; was the hardest for me.
My original idea was to use a `HashMap<&Point, Vec<&Point>>` to show the associations. \
`HashMap<K, V>` however, requires:
```rust
K: Eq + Hash
```
This means that `K` needs to implement `Eq + Hash`. `Point` does *not* implement either of those, since it's defined as:
```rust
pub struct Vec2 {
    pub x: f32,
    pub y: f32
}
```
`f32` does not implement `Eq`, because `f32::NaN != f32::NaN` <sup>[2]</sup> \
Now, those mystical indices that we defined before come into play. Instead of returning that kind of `HashMap`, we can return: `HashMap<CentroidIdx, Vec<&Point>>`

We need to take the arguments:
* `dataset`: our original dataset, and
* `centroids`: the centroids that we chose earlier
So:
```rust
pub fn associate_centroids_to_points<'c, 'd>(
    dataset: &'d IndexVec<PointIdx, Point>,
    centroids: &'c IndexVec<CentroidIdx, Point>,
) -> HashMap<CentroidIdx, Vec<&'d Point>> {
    todo!()
}
```
Instead of mapping the points to an actual centroid point, we can map them to the index of that centroid in the `centroids` vec.

We have to iterate over each point, and then over each centroid. We then measure the distance to each centroid for that point and pick the smallest distance. Then, we can just associate that point with that centroid.
We're going to need a `CentroidDistance` structure to keep track of the distances, too.
```rust
struct CentroidDistance {
    idx: CentroidIdx,
    distance: f32
}

pub fn associate_centroids_to_points<'c, 'd>(
    dataset: &'d IndexVec<PointIdx, Point>,
    centroids: &'c IndexVec<CentroidIdx, Point>,
) -> HashMap<CentroidIdx, Vec<&'d Point>> {
    let mut associations = HashMap::new();

    for point in dataset {
        let mut distances: Vec<CentroidDistance> = vec![];

        for (idx, ctr) in centroids.iter_enumerated() {
            let cdist = CentroidDistance {
                idx,
                distance: point.distance(*ctr)
            };

            distances.push(cdist);
        }

        let smallest = distances
            .iter()
            .min_by(|x, y| x.distance.partial_cmp(&y.distance).unwrap()) // we can't use min here, since min requires `Ord`, which f32 doesn't implement.
            .expect("non-empty vec");

        associations.entry(smallest.idx).or_insert(vec![]).push(point);
        // if the centroid doesn't have any points yet, we just create a new vec
        // and then push the point to it.
    }

    associations
}
```
Our last step is to write a function to update those centroids.
This is fairly simple, all we do is calculate the average point for each cluster and return them.

```rust
pub fn update_centroids(assoc: &HashMap<CentroidIdx, Vec<&Point>>) -> IndexVec<CentroidIdx, Point> {
    let mut new_centroids: IndexVec<CentroidIdx, Point> = index_vec![];

    let centroid_indices = assoc.keys();

    for index in centroid_indices {
        let values = assoc.get(index).expect("valid indices returned by .keys()");
        new_centroids.push(calculate_average_point(values));
    }

    new_centroids
}

pub fn calculate_average_point(points: &Vec<&Point>) -> Point {
    let mut x: f32 = 0f32;
    let mut y: f32 = 0f32;

    let l = points.iter().len() as f32;

    for point in points {
        x += point.x;
        y += point.y;
    }

    x /= l;
    y /= l;

    Point::new(x, y)
}
```

And would you look at that, we're done! The only thing left to do is mash it all together and run it.
Also, when we compare the centroids, we have to make sure that the vectors are the same **regardless of order**.
```rust
// Smaller in this case is defined as closer to [0, 0]
fn sort_point_vec(v: &IndexVec<CentroidIdx, Vec2>) -> IndexVec<CentroidIdx, Vec2> {
    let mut vec_clone = v.clone();
    vec_clone.sort_by(|a, b| a.x.total_cmp(&b.x).cmp(&a.y.total_cmp(&b.y)));
    vec_clone
}

...

fn main() {
    let dataset = generate_datapoints(None, None, None);
    let mut old_centroids = pick_centroids(&dataset, None);

    let mut counter = 1u8;
    loop {
        ctr += 1;
        let associations = associate_centroids_to_points(&dataset, &old_centroids);
        let new_centroids = update_centroids(&assoc);

        if sort_point_vec(&new_centroids) == sort_point_vec(&old_centroids) {
            break;
        }
    }

    println!("K-Means completed with n={ctr} runs");
}

```
That's pretty much it. The next step would be removing the k from the equation and making the algorithm guess it, but I'm not covering that here.

You can find the full code [here](https://github.com/SunkenPotato/kmeans-rs)

Thanks for reading!
<hr>

References: 

* \[1]: https://en.wikipedia.org/wiki/K-means_clustering
* \[2]: https://doc.rust-lang.org/std/primitive.f32.html#nan-bit-patterns