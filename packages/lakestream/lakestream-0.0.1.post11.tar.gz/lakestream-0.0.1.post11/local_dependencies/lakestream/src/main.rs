use std::env;

mod http;
mod s3;

use s3::handler::{S3Client, Credentials};
use http::requests::http_get_request;

fn main() {
    let access_key = env::var("AWS_ACCESS_KEY_ID")
        .expect("Missing environment variable AWS_ACCESS_KEY_ID");
    let secret_key = env::var("AWS_SECRET_ACCESS_KEY")
        .expect("Missing environment variable AWS_SECRET_ACCESS_KEY");
    let region = env::var("AWS_REGION")
        .expect("Missing environment variable AWS_REGION");
    let bucket = env::var("AWS_BUCKET")
        .expect("Missing environment variable AWS_BUCKET");

    let credentials = Credentials::new(
        String::from(access_key),
        String::from(secret_key),
    );

    let endpoint_url = format!("https://{}.s3.{}.amazonaws.com:443", bucket, region);
    let s3_client = S3Client::new(
        String::from(endpoint_url),
        String::from(region),
        credentials,
    );
    let headers = s3_client.generate_headers("GET", None, None).unwrap();
    let body = http_get_request(&s3_client.url, &headers);
    println!("body: {:?}", s3_client.list_objects(&body.unwrap()));
    // match s3_client.list_objects(None) {
    //     Ok(objects) => println!("Objects in bucket {}: {:?}", bucket, objects),
    //     Err(err) => eprintln!("Error listing objects in bucket {}: {}", bucket, err),
    // }
}

