use rayon::prelude::*;
use reqwest::blocking::Client;

fn main() {
    let urls = (0..25000).map(|_i| "http://localhost:5000/query?user=mingy".to_string()).collect::<Vec<_>>();

    let client = Client::new();
    urls.par_iter().for_each(|url| {
        let _ = client.get(url).send();
    });
}

