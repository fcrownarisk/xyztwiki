fn main() {
    // Using '=' for assignment
    let base: u32 = 10;
    let multiplier = 5;

    // Closure using '|' for parameters and '&' for reference
    let calculate = |x: &u32| -> u32 {
        // Pattern matching with '|' in match arms
        match *x {
            0 => 0,
            1 | 2 => x * base,  // '|' in pattern
            _ => x * multiplier,
        }
    };

    // Using '&' for references
    let numbers = vec![0, 1, 2, 3, 4];
    let mut results = Vec::new();

    // Using '&' in borrow and '|' in closure
    numbers.iter().for_each(|num| {
        // Using '=' for assignment
        let value = calculate(&num);
        results.push(value);
    });

    // Using '|' in bitwise OR and '&' in bitwise AND
    let flags = 0b0011;
    let mask = 0b1010;
    let combined = (flags | mask) & 0b1111;

    println!("Results: {:?}", results);
    println!("Flags: {:04b}", combined);
}