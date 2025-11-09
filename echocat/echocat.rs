use clap::Parser;
use std::{
    fs::File,
    io::{self, BufRead, BufReader},
    path::Path,
};

/// Echo input lines multiple times
#[derive(Parser, Debug)]
#[command(version, about)]
struct Args {
    /// Files to process (use '-' for stdin)
    #[arg(default_value = "-")]
    files: Vec<String>,

    /// Number of times to repeat each line
    #[arg(short, long, default_value_t = 2)]
    repeat: usize,
}

fn main() -> anyhow::Result<()> {
    let args = Args::parse();

    for filename in &args.files {
        // Open reader for file or stdin
        let reader: Box<dyn BufRead> = match filename.as_str() {
            "-" => Box::new(BufReader::new(io::stdin())),
            path => {
                let file = File::open(Path::new(path))
                    .map_err(|e| anyhow::anyhow!("Error opening {}: {}", path, e))?;
                Box::new(BufReader::new(file))
            }
        };

        // Process lines
        for line in reader.lines() {
            let line = line.map_err(|e| anyhow::anyhow!("Read error: {}", e))?;
            for _ in 0..args.repeat {
                println!("{}", line);
            }
        }
    }

    Ok(())
}