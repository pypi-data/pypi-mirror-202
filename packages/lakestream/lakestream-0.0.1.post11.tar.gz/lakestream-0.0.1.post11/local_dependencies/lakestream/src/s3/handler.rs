
use std::collections::HashMap;

use url::Url;
use sha2::{Sha256, Digest};
use hex;
use hmac::{Hmac, Mac, NewMac};

use time::OffsetDateTime;

use percent_encoding::{utf8_percent_encode, AsciiSet, CONTROLS};
use itertools::Itertools;

use serde::Deserialize;
use serde_xml_rs;


#[derive(Debug, Deserialize)]
struct ListBucketResult {
    Contents: Vec<Content>,
}

#[derive(Debug, Deserialize)]
pub struct Content {
    Key: String,
    Size: u64,
}


fn sign(key: &[u8], msg: &[u8]) -> Vec<u8> {
    let mut hmac = Hmac::<Sha256>::new_from_slice(key).expect("HMAC can take key of any size");
    hmac.update(msg);
    let result = hmac.finalize();
    result.into_bytes().as_slice().to_vec()
}

pub struct Credentials {
    pub access_key: String,
    pub secret_key: String,
}

impl Credentials {
    pub fn new(access_key: String, secret_key: String) -> Self {
        Self {
            access_key,
            secret_key,
        }
    }
}

pub struct S3Client {
    pub url: String,
    pub resource: String,
    pub query_string: String,
    pub region: String,
    pub credentials: Credentials,
    endpoint_url: String,
    utc_now: OffsetDateTime,
}

impl S3Client {

    pub fn new(endpoint_url: String, region: String, credentials: Credentials) -> S3Client {
        // let mut base_headers = HashMap::new();
        // base_headers.insert("content-type".to_string(), "application/xml".to_string());

        let resource = "".to_string();
        let utc_now = OffsetDateTime::now_utc();
        let prefix: Option<String> = None;
        let query_string = prefix
            .map(|p| format!("list-type=1&max-keys=1000&prefix={}", p))
            .unwrap_or_default();

        let url = format!("{}/{}?{}", endpoint_url, &resource, &query_string);

        S3Client {
            url,
            resource,
            query_string,
            region,
            credentials,
            endpoint_url,
            utc_now,
        }

    }

    fn get_canonical_headers(&self, headers: &HashMap<String, String>) -> String {
        let mut canonical_headers = String::new();
        let mut headers_vec: Vec<(&String, &String)> = headers.iter().collect();
        headers_vec.sort_by(|a, b| a.0.to_lowercase().cmp(&b.0.to_lowercase()));

        for (header_name, header_value) in headers_vec {
            let header_name = header_name.trim().to_lowercase();
            if header_name.starts_with("x-amz-") && header_name != "x-amz-client-context" || header_name == "host" || header_name == "content-type" || header_name == "date" {
                canonical_headers += &format!("{}:{}\n", header_name, header_value.trim());
            }
        }

        canonical_headers
    }

    fn generate_signing_key(&self) -> Vec<u8> {
        let date_stamp = format!("{:04}{:02}{:02}", self.utc_now.year(), self.utc_now.month() as u8, self.utc_now.day());

        let k_date = sign(
            format!("AWS4{}", self.credentials.secret_key).as_bytes(),
            date_stamp.as_bytes(),
            );
        let k_region = sign(&k_date, self.region.as_bytes());
        let k_service = sign(&k_region, b"s3");
        let signing_key = sign(&k_service, b"aws4_request");
        signing_key
    }


    pub fn list_objects(&self, body: &str) -> Result<Vec<Content>, Box<dyn std::error::Error>> {
        let list_bucket_result: ListBucketResult = serde_xml_rs::from_str(&body)?;
        Ok(list_bucket_result
           .Contents
           .into_iter()
           .collect())
    }

    fn initiate_headers(
        &self,
        headers: Option<HashMap<String, String>>,
        x_amz_date: &str,
        payload_hash: Option<&str>,
        ) -> Result<HashMap<String, String>, Box<dyn std::error::Error>> {
        let mut headers = headers.unwrap_or_default();
        headers.insert("x-amz-date".to_string(), x_amz_date.to_string());
        headers.insert("x-amz-content-sha256".to_string(), payload_hash.unwrap_or("UNSIGNED-PAYLOAD").to_string());
        Ok(headers)
    }

    fn get_canonical_uri(&self, url: &Url, resource: &str) -> String {
        const CUSTOM_ENCODE_SET: &AsciiSet = &CONTROLS.add(b'/');
        let canonical_resource = utf8_percent_encode(resource.trim_end_matches('/'), CUSTOM_ENCODE_SET).to_string();
        let endpoint_path = url.path().trim_start_matches('/').trim_end_matches('/');

        if endpoint_path.is_empty() {
            canonical_resource
        } else {
            format!(
                "{}/{}",
                utf8_percent_encode(endpoint_path, CUSTOM_ENCODE_SET).to_string(),
                canonical_resource
                )
        }
    }

    fn get_canonical_query_string(&self) -> Result<String, Box<dyn std::error::Error>> {
        if self.query_string.is_empty() {
            Ok(String::new())
        } else {
            let mut parts: Vec<(String, String)> = self.query_string.split('&')
                .filter_map(|p| {
                    let mut split = p.splitn(2, '=');
                    match (split.next(), split.next()) {
                        (Some(k), Some(v)) => Some((k.to_string(), v.to_string())),
                        _ => None,
                    }
                })
            .collect();

            parts.sort();

            let encoded_parts: Vec<String> = parts.into_iter()
                .map(|(k, v)| format!("{}={}", k, utf8_percent_encode(&v, &CONTROLS).to_string()))
                .collect();

            Ok(encoded_parts.join("&"))
        }
    }

    pub fn generate_headers(
        &self,
        method: &str,
        headers: Option<HashMap<String, String>>,
        payload_hash: Option<&str>,
        ) -> Result<HashMap<String, String>, Box<dyn std::error::Error>> {
        let date_stamp = format!("{:04}{:02}{:02}", self.utc_now.year(), self.utc_now.month() as u8, self.utc_now.day());
        let x_amz_date = format!("{}T{:02}{:02}{:02}Z", &date_stamp, self.utc_now.hour(), self.utc_now.minute(), self.utc_now.second());

        let credential_scope = format!("{}/{}/s3/aws4_request", date_stamp, self.region);
        let mut headers = self.initiate_headers(headers, &x_amz_date, payload_hash)?;

        let url = Url::parse(&self.endpoint_url)?;
        let host = url.host_str().ok_or("Missing host")?.to_owned();
        let host = match url.port() {
            Some(port) => host.replace(&format!(":{}", port), ""),
            None => host,
        };
        headers.insert("host".to_string(), host);

        let canonical_uri = self.get_canonical_uri(&url, &self.resource);

        let canonical_headers = self.get_canonical_headers(&headers);
        let signed_headers = headers.keys().cloned().sorted().collect::<Vec<String>>().join(";");
        let canonical_query_string = self.get_canonical_query_string()?;

        let canonical_request = format!(
            "{}\n/{}\n{}\n{}\n{}\n{}",
            method,
            canonical_uri,
            canonical_query_string,
            canonical_headers,
            signed_headers,
            payload_hash.unwrap_or("UNSIGNED-PAYLOAD")
            );

        let string_to_sign = format!(
            "AWS4-HMAC-SHA256\n{}\n{}\n{}",
            x_amz_date,
            credential_scope,
            format!("{:x}", Sha256::digest(canonical_request.as_bytes()))
            );

        let signing_key = self.generate_signing_key();
        let signature = sign(&signing_key, string_to_sign.as_bytes());

        let authorization_header = format!(
            "AWS4-HMAC-SHA256 Credential={}/{}, SignedHeaders={}, Signature={}",
            self.credentials.access_key,
            credential_scope,
            signed_headers,
            hex::encode(signature)
            );

        headers.insert("Authorization".to_string(), authorization_header);
        Ok(headers)
    }
}

