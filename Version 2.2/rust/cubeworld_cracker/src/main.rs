use serde_derive::{Serialize, Deserialize};
use serde_xml_rs::from_reader;
use std::fs;
use std::path::Path;
use reqwest;
use std::io::{Write, Read, Seek, stdin};
use flate2;

#[derive(Debug, Deserialize)]
struct CubeFile {
    destination: String,
    source: String,
    digest: String,
    cdigest: String,
}
impl CubeFile {
    pub fn download(&self, base_url: &String, path: &Path) {
        println!("Downloading {}", &self.destination);
        let mut compressed_data = download(&format!("{}{}", &base_url, &self.source));

        let mut decoder = flate2::read::ZlibDecoder::new(compressed_data.as_slice());
        let mut decompressed_data: Vec<u8> = Vec::new();
        decoder.read_to_end(&mut decompressed_data);

        let mut file = fs::File::create(path.join(&self.destination))
            .expect("Could not open file.");
        file.write_all(&decompressed_data);

        if self.destination == "Cube.exe" {
            println!("Patching Cube.exe");
            file.seek(std::io::SeekFrom::Start(0x5A18D));
            for i in 0..6 {
                file.write_all(b"\x90");
            }
        }
    }
}

#[derive(Debug, Deserialize)]
struct CubePackage {
    id: String,
    file: Vec<CubeFile>,
}
impl CubePackage {
    pub fn download(&self, base_url: &String, path: &Path) {
        for file in &(self.file) {
            if file.destination != "CubeLauncher.exe" {
                file.download(base_url, path);
            }
        }
    }
}


fn download(url: &String) -> Vec<u8> {
    let mut resp = reqwest::get(url)
        .expect("Unable to download file.");
    let mut file_data: Vec<u8> = Vec::new();
    resp.copy_to(&mut file_data);
    return file_data;
}

fn generate_db(path: &Path) {
    let mut file = fs::File::create(path.join(Path::new("db.dat")))
        .expect("Could not open db.dat.");
    for i in 0..32 {
        file.write_all(b"\x00");
    }
}

fn main() {
    let INSTALLATION_PATH = Path::new("Cube World");
    fs::create_dir(&INSTALLATION_PATH);

    let CWDOWNLOAD_AWS: String = "http://s3.amazonaws.com/picroma/cwdownload/".to_string();
    let PACKAGE_XML: String = format!("{}{}", &CWDOWNLOAD_AWS, "package.xml".to_string());

    let xml_data = String::from_utf8(
        download(&PACKAGE_XML))
        .expect("Unable to read xml file.");

    let package: CubePackage = from_reader(xml_data.as_bytes())
        .expect("Could not parse XML data.");

    package.download(&CWDOWNLOAD_AWS, &INSTALLATION_PATH);
    generate_db(&INSTALLATION_PATH);

    println!("Installation complete. Use Cube.exe to run the game. Press enter to exit.");
    stdin().read_line(&mut String::new());
}
