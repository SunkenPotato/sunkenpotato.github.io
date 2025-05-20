+++
title = "PSA: Avoid Abstractions"
date = "2025-05-20T15:27:11+02:00"
#dateFormat = "2006-01-02" # This value can be configured for per-post date formatting
author = ""
authorTwitter = "" #do not include @
cover = ""

keywords = ["", ""]
description = "My take on abstractions in programming"
showFullContent = false
readingTime = false
hideComments = false
+++
If you're reading this, you most likely know what abstractions are in programming.
We use them to make code compatible in different scenarios, often to avoid writing more code.

This is done by generalizing code to work with any class, structure, or value, be it through reflection, interfaces, or generics.

For example, you might have a function that takes an array of integers and modifies that array so that each number is multiplied by 2:
```rust
fn multiply_by_2(array: &mut [i32]) {
    for item in array {
        *item *= 2;
    }
}
```
But later, we find out we want to do this again, only this time, we need to do this with floats!
So, we generalize the code to work with any type that we want and add a parameter to tell the function what to multiply by:
```rust
use std::ops::MulAssign;

fn multiply_by_n<T>(array: &mut [T], n: T)
where
  T: MulAssign + Copy
{
    for item in array {
        *item *= n
    }
}
```

This example is harmless, and follows the [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) principle.

But the things I've caught myself abstracting would make your eyes bleed (unless you're an abstraction-enthusiast too).

Just to name a few:
- Error messages via an error registry.
- Player controller actions when there's only one possible action.[<sup>1</sup>](#abhorrent-abstraction-example)
- One-use functions, similar to the one above.

What I'm trying to say is: don't abuse DRY.

We're often told that we should always follow that principle. It's been around since 1999, so there's no reason not to.

Right?

People tend to abstract code thinking they'll avoid writing more of it later, which often ends up only being used in the original case.
You spend far too much time thinking of how to solve the problem in any situation, just to end up never **actually** using your new fancy solution. \
So in my opinion, you should stray from abstractions, rather than wandering towards them. \
It's like buying a mountain bike, just to use it in a city (this happens surprisingly often, by the way).

In conclusion: Please, just avoid abstracting your code unless you need to. You'll save yourself time, and probably be happier!

Anyway, thank you so much for reading.

### Notes
1. This article is based on the AHA principle by Kent C. Dodds & Sandi Metz.

#### Abhorrent abstraction example
```rust
pub struct Controller {
    action: Option<Box<dyn Action>>
}

trait Action {
    fn speed(&self) -> f32;
    fn direction(&self) -> Option<Dir3>; // normalized 3D vector, to either point somewhere or not at all
    fn acceleration(&self) -> f32;
}

struct WalkAction { // this ended up being the only struct that actually implemented `Action`
    speed: f32,
    direction: Option<Dir3>,
    acceleration: f32
}

impl Action for WalkAction {
    fn speed(&self) -> f32 {
        self.speed
    }

    fn direction(&self) -> Option<Dir3> {
        self.direction
    }

    fn acceleration(&self) -> f32 {
        self.acceleration
    }
}
```
