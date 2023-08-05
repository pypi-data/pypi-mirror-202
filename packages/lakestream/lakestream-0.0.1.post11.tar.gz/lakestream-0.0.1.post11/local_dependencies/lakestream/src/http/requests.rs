
use std::collections::HashMap;
use std::error::Error;
use std::io::Read;

use ureq::Agent;

pub fn http_get_request(url: &str, headers: &HashMap<String, String>) -> Result<String, Box<dyn Error>> {
    let agent = Agent::new();
    let mut request_builder = agent.get(url);

    for (key, value) in headers.iter() {
        request_builder = request_builder.set(key, value);
    }
    let mut response = request_builder.call()?;

    let status = response.status();
    if !(200..300).contains(&status) {
        return Err(format!("Error: HTTP GET request failed with status code {}", status).into());
    }

    let mut body = String::new();
    response.into_reader().read_to_string(&mut body)?;
    Ok(body)
}
